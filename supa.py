
#%%
import lib
import requests
import json
import csv
import re

# Setups
macro_food_dict = lib.macro_foods
nutri_code_dict = { "protein": 878, "carb": 705, "fat": 764, "fruit": None, "vegetable": None }
ureg = lib.ureg
Q_ = lib.Q_

# Initialise session
s = requests.Session()
init = lib.requests_kwargs["supa_init"]
s.get(**init)

#%%
# Debug: small case
#macro_food_dict = { "vegetable": ["cabbage"] }

# Search items for each macro-food pair, then collect their info
macro_per_AUD_df = []
for macro in macro_food_dict:
    for food in macro_food_dict[macro]:
        print(f"Processing {macro} contained in {food}...")
        # Skip first: weight not in catalog and varied
        if food in ["cabbage"]:
            macro_per_AUD_df.append([macro, food, ""])
            continue
    
        srch =  lib.requests_kwargs["supa_search"]
        response = s.post(**srch(food))
        #print(response.json())

        data = response.json()
        mpauds = []
        for subdata in data["Products"]:
            prod = subdata["Products"][0]
            try:
                if not prod["IsInStock"]:
                    continue
                price = Q_(prod["InstoreCupPrice"])
                size = Q_(re.sub('ea$', '', prod["CupMeasure"].lower()))
                
                if macro in ["fruit", "vegetable"]:
                    ratio = 1
                else:
                    ratio = None
                    nutri = json.loads(prod["AdditionalAttributes"]["nutritionalinformation"])
                    for obj in nutri["Attributes"]:
                        if obj["Id"] == nutri_code_dict[macro]:
                            ratio_fmt = re.match(r"^(Approx.)?([0-9.]+)([A-Za-z]+)$", obj["Value"]) # regex check
                            ratio_num = ratio_fmt.groups()[1]
                            ratio_unit = ratio_fmt.groups()[2]
                            if ratio_unit:
                                ratio = Q_(ratio_num + ratio_unit.lower())/Q_("100g")
                    if not ratio: # the macro is not listed on the spec
                        continue
            except:
                continue
            mpaud = ratio * (size/Q_("1g")) / price

            # If liquid, convert the unit from volume to mass
            if mpaud.check("[volume]"):
                mpaud *= Q_("1000 gram/liter")
            
            mpauds.append(mpaud)
        
        # Average from all items
        if len(mpauds) == 0:
            continue
        macro_per_AUD_overall = sum(mpauds)/len(mpauds)
        macro_per_AUD_df.append([macro, food, format(macro_per_AUD_overall.to(""), "~")])

# %%
# Append to csv
with open(lib.supa_out_path, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows([["Category", "Food", "Amount"]])
    writer.writerows(macro_per_AUD_df)
