
#%%
import lib
import requests
import json
import pint
import csv
import re

# Minimum viable product

macro_food_dict = {
    "protein": ["milk", "egg", "chicken", "beef", "pork", "sardine", "bean", "almond", "chia"],
    "carb": ["rice", "wholewheat-bread", "oat", "potato", "quinoa", "pasta", "corn"],
    "fat": ["avocado", "olive-oil", "peanut-butter", "greek-yoghurt", "cheese", "salmon", "tuna", "sardine", "almond"],
    #"fruit": ["berry", "banana", "apple", "orange", "grape", "pear", "kiwi", "lemon", \
    #          "watermelon", "pineapple", "mango"],
    #"vegetable": ["spinach", "cabbage", "lettuce", "brocolli", "cauliflower", "tomato", "carrot", "capsicum", \
    #              "zucchini", "mushroom", "choy buk"]
}
nutri_code_dict = { "protein": 878, "carb": 705, "fat": 764}

ureg = pint.UnitRegistry()
Q_ = ureg.Quantity

#%%
s = requests.Session()
init = {
    "url": "https://www.woolworths.com.au/",
    "headers": {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "accept-language": "en-GB,en;q=0.6",
        "priority": "u=0, i",
        "sec-ch-ua": '"Chromium";v="124", "Brave";v="124", "Not-A.Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "sec-gpc": "1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }
}
s.get(init["url"], headers=init["headers"])

#%%
#Debug: small case
#macro_food_dict = { "fat": ["olive-oil"] }

macro_pcu_df = [] #macro per unit currency
for macro in macro_food_dict:
    for food in macro_food_dict[macro]:
        url = "https://www.woolworths.com.au/apis/ui/Search/products"
        payload = {
            "Location": f"/shop/search/products?searchTerm{food}",
            "SearchTerm": f"{food}",
            "PageSize": 10,
            "Filters": [],
            "IsSpecial": False,
            "SortType": "TraderRelevance",
            "IsRegisteredRewardCardPromotion": None,
            "ExcludeSearchTypes": ["UntraceableVendors"],
            "GpBoost": 0,
            "GroupEdmVariants": True,
            "EnableAdReRanking": False
        }
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-GB,en;q=0.9",
            "content-type": "application/json",
            "origin": "https://www.woolworths.com.au",
            "priority": "u=1, i",
            "referer": f"https://www.woolworths.com.au/shop/search/products?searchTerm={food}",
            "request-id": "|74c2518bb1bc4a87ba7373a72de2499f.436c2500f7a54854",
            "sec-ch-ua": '"Chromium";v="124", "Brave";v="124", "Not-A.Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Linux"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "sec-gpc": "1",
            "traceparent": "00-74c2518bb1bc4a87ba7373a72de2499f-436c2500f7a54854-01",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        }
        response = s.post(url, json=payload, headers=headers)
        #print(response.json())

        data = response.json()
        mpcus = []
        for subdata in data["Products"]:
            prod = subdata["Products"][0]
            try:
                price = Q_(prod["InstoreCupPrice"])
                size = Q_(prod["CupMeasure"].lower())
                ratio = None
                nutri = json.loads(prod["AdditionalAttributes"]["nutritionalinformation"])
                for obj in nutri["Attributes"]:
                    if obj["Id"] == nutri_code_dict[macro]:
                        ratio_fmt = re.match(r"^(Approx.)?([0-9.]+)([A-Za-z]+)$",obj["Value"])
                        ratio_num = ratio_fmt.groups()[1]
                        ratio_unit = ratio_fmt.groups()[2]
                        if ratio_unit:
                            ratio = Q_(ratio_num + ratio_unit.lower())/Q_("100g")
                if not ratio: # the macro is not listed on the spec
                    continue
            except:
                continue
            
            # Determine the single item's macro rate
            #   if liquid, convert the unit from volume to mass
            mpcu = ratio * size / price
            if mpcu.check("[volume]"):
                mpcu *= Q_("1000 gram/liter")
            mpcus.append(mpcu)
                                        
        # Average from all items
        res = sum(mpcus)/len(mpcus)
        macro_pcu_df.append([macro, food, str(res.to("gram"))])

# TOT 30s

# %%
# Append to
with open('woolies_out.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(macro_pcu_df)
