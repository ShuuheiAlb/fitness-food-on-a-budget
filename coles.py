
#%%

import lib
import requests
import re
import csv
from bs4 import BeautifulSoup

macro_food_dict = lib.macro_foods
ureg = lib.ureg
Q_ = lib.Q_

#%%
# Initialise session
# Quirk: find a specified date_version to access API url path
s = requests.Session()
init_r = s.get(**lib.requests_kwargs["coles_init"])
date_version = re.search(r'src="/_next/static/([0-9\.]+_v[0-9\.]+)/.+.js"', init_r.text). \
    groups()[0]

# %%
# Debug: small case
#macro_food_dict = { "protein": ["milk"] }

macro_per_AUD_df = []
for macro in macro_food_dict:
    for food in macro_food_dict[macro]:
        srch = lib.requests_kwargs["coles_search"]
        srch_r = s.get(**srch(food, date_version))
        #print(srch_r.json())

        # For each item, find the nutritional info in the table
        data = srch_r.json()["pageProps"]["searchResults"]["results"]
        data = data[:min(len(data), 10)]
        mpauds = []
        for item in data:
            if item["_type"] in ["PRODUCT", "PRODUCT_ASSOCIATION"]:
                try:
                    if not item["availability"]:
                        continue
                    price = Q_(item["pricing"]["now"])
                    size = Q_(item["size"].lower())
                    
                    # Get nutiriton info
                    spec = lib.requests_kwargs["coles_spec"]
                    sub_url = "/product/" + "-".join(re.split(r"[^A-Za-z0-9]+", item["description"].lower())) + "-" + str(item["id"])
                    spec_r = s.get(**spec(sub_url, date_version, food))
                    subdata = spec_r.json()

                    # Retry if sub_url is redirected
                    if not "product" in subdata["pageProps"]:
                        sub_url = subdata["pageProps"]["__N_REDIRECT"]
                        spec_r = s.get(**spec(sub_url, date_version, food))
                        subdata = spec_r.json()

                    nutri_percentage = subdata["pageProps"]["product"]["nutrition"]["breakdown"][0]
                    assert nutri_percentage["title"] == "Per 100g/ml"
                    
                    if macro in ["fruit", "vegetable"]:
                        ratio = 1
                    else:
                        ratio = None
                        for n in nutri_percentage["nutrients"]:
                            if n["nutrient"].lower() == macro:
                                ratio = Q_(n["value"])/Q_("100g")
                                #print(ratio)
                                if not ratio.check(""):
                                    ratio = None
                        if not ratio:
                            continue
                except:
                    continue
                
                mpaud = ratio * size / price

                # If liquid, convert the unit from volume to mass
                if mpaud.check("[volume]"):
                    mpaud *= Q_("1000 gram/liter")
                
                mpauds.append(mpaud)

        # Average from all items
        macro_per_AUD_overall = sum(mpauds)/len(mpauds)
        macro_per_AUD_df.append([macro, food, str(macro_per_AUD_overall.to("gram"))])

# %%
# Append to csv
with open('coles_out.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows([["Category", "Food", "Amount/$"]])
    writer.writerows(macro_per_AUD_df)

