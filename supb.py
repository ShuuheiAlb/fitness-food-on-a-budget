
#%%

import lib
from selenium import webdriver
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import requests
import re
import pandas as pd
import csv

macro_food_dict = lib.macro_foods
nutri_key_dict = { "protein": "Protein", "carb": "Carbohydrate", "fat": "Total Fat", "fruit": None, "vegetable": None }
ureg = lib.ureg
Q_ = lib.Q_
afcd = pd.read_excel(lib.acfd_path, "All solids & liquids per 100g")

#%%
# No initialised session: extract user_agent + cookies pair from Selenium,
#   then jump to requests.get

# But before: Ubuntu env - need to specify gecko path into Selenium's webdriver
geckodriver_path = "/snap/bin/geckodriver"
driver_service = webdriver.FirefoxService(executable_path=geckodriver_path)
options = webdriver.FirefoxOptions()
options.headless = True  # Run in headless mode
options.set_preference("dom.webdriver.enabled", False)
options.set_preference("useAutomationExtension", False)
driver = webdriver.Firefox(service=driver_service, options=options)

driver.get(lib.requests_kwargs["supb_init"]("")["url"])
user_agent = driver.execute_script("return window.navigator.userAgent;")
cookies = {cookie["name"]: cookie["value"] for cookie in driver.get_cookies()}
driver.quit()

# Suppress warning from not verifying 
warnings.filterwarnings("ignore", category=InsecureRequestWarning)

# Quirk: find a specified date_version to access API url path
init = lib.requests_kwargs["supb_init"]
init_r = requests.request("GET", **init(user_agent))
date_version = re.search(r'src="/_next/static/([0-9\.]+_v[0-9\.]+)/.+.js"', init_r.text). \
    groups()[0]

# %%
# Debug: small case
#macro_food_dict = {"protein": ["egg"]}

# Throttle request check
from ratelimit import limits, sleep_and_retry
@sleep_and_retry
@limits(calls=5, period=1)
def supb_call(kwargs):
    response = requests.request("GET", **kwargs)
    if response.status_code != 200:
        raise Exception('API response: {}'.format(response.status_code))
    return response
print("Note: it might take a while, due to request rate limiting.")

macro_per_AUD_df = []
for macro in macro_food_dict:
    for food in macro_food_dict[macro]:
        print(f"Processing {macro} contained in {food}...")

        srch = lib.requests_kwargs["supb_search"]
        srch_r = supb_call(srch(user_agent, food, date_version))
        #print(srch_r.json())

        # For each item, find the nutritional info in the table
        data = srch_r.json()["pageProps"]["searchResults"]["results"]
        for item in data:
            if item["_type"] in ["PRODUCT", "PRODUCT_ASSOCIATION"]:
                try:
                    if not item["availability"]:
                        continue
                    price = Q_(item["pricing"]["now"])
                    size = Q_(re.sub('((^approx. )|( each$))', '', item["size"].lower()))
                    if not (size.check("[volume]") or size.check("[mass]")):
                        continue # size is not litre nor gram, throw away
                    
                    if macro in ["fruit", "vegetable"]:
                        ratio = 1
                    elif food in ["chicken", "potato"]:
                        # These products do not have nutrition info. Matching AFCD dataset ...
                        food_keys = {"chicken": "F002806", "potato": "F007325"}
                        macro_keys = {"protein": "Protein \n(g)", "fat": "Fat, total \n(g)", "carb": "Available carbohydrate, without sugar alcohols \n(g)" }
                        n_value = afcd.loc[afcd["Public Food Key"] == food_keys[food], macro_keys[macro]].values[0]
                        ratio = Q_(n_value)/Q_("100")
                    else:
                        ratio = None

                        # Get nutiriton info
                        spec = lib.requests_kwargs["supb_spec"]
                        sub_url = "/product/" + "-".join(re.split(r"[^A-Za-z0-9]+", item["description"].lower())) + "-" + str(item["id"])
                        spec_r = supb_call(spec(user_agent, sub_url, date_version, food))
                        subdata = spec_r.json()

                        # Retry if sub_url is redirected
                        if not "product" in subdata["pageProps"]:
                            sub_url = subdata["pageProps"]["__N_REDIRECT"]
                            spec_r = supb_call(spec(user_agent, sub_url, date_version, food))
                            subdata = spec_r.json()

                        nutri_percentage = subdata["pageProps"]["product"]["nutrition"]["breakdown"][0]
                        assert nutri_percentage["title"] == "Per 100g/ml"
                        for n in nutri_percentage["nutrients"]:
                            #print(n, sub_url)
                            if n["nutrient"] == nutri_key_dict[macro]:
                                ratio = Q_(n["value"])/Q_("100")
                                if ratio.check("[mass]"):
                                    ratio /= Q_("1g")
                                elif not ratio.check(""):
                                    ratio = None
                        if not ratio:
                            continue
                except:
                    continue
                
                mpaud = ratio * (size/Q_("1g")) / price

                # If liquid, convert the unit from volume to mass
                if size.check("[volume]"):
                    mpaud *= Q_("1000 gram/liter")
                
                macro_per_AUD_df.append([macro, food, format(mpaud.to(""), "~")])

        # Placeholder for product with empty rows
        if len(data) == 0:
            macro_per_AUD_df.append([macro, food, ""])

# %%
# Append to csv
with open(lib.supb_out_path, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows([["Category", "Food", "Amount"]])
    writer.writerows(macro_per_AUD_df)


# %%
