
# Minimum viable product:
# MILK, EGG, CHICKEN BREAST, BEEF, SALMON, BEAN, (SARDINE, CHEESE, YOGHURT)
# RICE, WW BREAD, OAT, POTATO, QUINOA, PASTA, CORN
# PB, AVODACO, OLIVE OIL, ALMOND, CHIA, BUTTER
# BERRIES, BANANA, APPLE, ORANGE, GRAPE, (PEAR, KIWI, WATERMELON, MANGO)
# SPINACH, BROCOLLI, TOMATO, CABBAGE, CARROT, PEA, (CAPSICUM, ZUCHINNI, SPROUT)


import requests
import json
from unitpy import Quantity
from unitpy.definitions.unit_base import BaseSet
import numpy as np

protein_foods = ["milk", "egg", "chicken", "beef", "salmon", "bean"]
protein_per_dollar = {}

for food in protein_foods:
    
    url = "https://www.woolworths.com.au/apis/ui/Search/products"

    payload = {
        "Filters": [],
        "IsSpecial": False,
        "Location": f"/shop/search/products?searchTerm{food}",
        "PageSize": 10,
        "SearchTerm": f"{food}",
        "SortType": "TraderRelevance",
        "IsRegisteredRewardCardPromotion": None,
        "ExcludeSearchTypes": ["UntraceableVendors"],
        "GpBoost": 0,
        "GroupEdmVariants": True,
        "EnableAdReRanking": False
    }
    headers = {
        # the _abck cookies expire easily
        "cookie": "EnableLandingPageVideosContentService=true; EnableLandingPageIdeasContentService=true; bff_region=syd2; ai_user=kPh5vamjorsgTXCOnVyMmj|2024-05-16T03:40:54.478Z; akaalb_woolworths.com.au=~op=www_woolworths_com_au_ZoneA:PROD-ZoneA|www_woolworths_com_au_BFF_SYD_Launch:WOW-BFF-SYD2|~rv=59~m=PROD-ZoneA:0|WOW-BFF-SYD2:0|~os=43eb3391333cc20efbd7f812851447e6~id=fe10e758f65623b90951cb55a3b57c48; INGRESSCOOKIE=1715830855.768.1742.124094|37206e05370eb151ee9f1b6a1c80a538; at_check=true; AMCVS_4353388057AC8D357F000101%40AdobeOrg=1; s_cc=true; dtCookie=v_4_srv_5_sn_E86957BB17A9F4F1D708914D90CA01E5_perc_100000_ol_0_mul_1_app-3Af908d76079915f06_1_rcs-3Acss_0; BVImplmain_site=14865; fullstoryEnabled=false; AKA_A2=A; w-rctx=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYmYiOjE3MTU4NzM1MjAsImV4cCI6MTcxNTg3NzEyMCwiaWF0IjoxNzE1ODczNTIwLCJpc3MiOiJXb29sd29ydGhzIiwiYXVkIjoid3d3Lndvb2x3b3J0aHMuY29tLmF1Iiwic2lkIjoiMCIsInVpZCI6ImY0NzA3ZmZhLTUyMzktNGRjOS05ZWZjLTczZWQ4YmVlOWEwYSIsIm1haWQiOiIwIiwiYXV0IjoiU2hvcHBlciIsImF1YiI6IjAiLCJhdWJhIjoiMCIsIm1mYSI6IjEifQ.Uq377pgBDrWUz6N3JtO2GSfZFzR9IDVOs2nei30Ockhz_zNCjXxVmHN70ITIDuA9yI8cBzhH-YaFBPQkhmHa4MDgW6RezKrqweFQG67KLDL8e2FTi112yR3qlop9JVVjJHeVfpc5MlgjPrecLVTVGI9bT-o-q1SFsdoiNypxW6ATkG7leu-7i9aQx2jluGCcn8eZSlJoYxXL9-xpgGmIBkTlpEmDt5pnqaJ1MvrLrn1Mv9DVN552vwqffhZOFoAn_9ichd3fqOh4Dc4vJy1dmhUoCqIRMcnhIiF14seSCFdwEn1ciH-HKDQIntSxUrEX5xrcjSWFBAPD3ZSI1dWUAA; wow-auth-token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYmYiOjE3MTU4NzM1MjAsImV4cCI6MTcxNTg3NzEyMCwiaWF0IjoxNzE1ODczNTIwLCJpc3MiOiJXb29sd29ydGhzIiwiYXVkIjoid3d3Lndvb2x3b3J0aHMuY29tLmF1Iiwic2lkIjoiMCIsInVpZCI6ImY0NzA3ZmZhLTUyMzktNGRjOS05ZWZjLTczZWQ4YmVlOWEwYSIsIm1haWQiOiIwIiwiYXV0IjoiU2hvcHBlciIsImF1YiI6IjAiLCJhdWJhIjoiMCIsIm1mYSI6IjEifQ.Uq377pgBDrWUz6N3JtO2GSfZFzR9IDVOs2nei30Ockhz_zNCjXxVmHN70ITIDuA9yI8cBzhH-YaFBPQkhmHa4MDgW6RezKrqweFQG67KLDL8e2FTi112yR3qlop9JVVjJHeVfpc5MlgjPrecLVTVGI9bT-o-q1SFsdoiNypxW6ATkG7leu-7i9aQx2jluGCcn8eZSlJoYxXL9-xpgGmIBkTlpEmDt5pnqaJ1MvrLrn1Mv9DVN552vwqffhZOFoAn_9ichd3fqOh4Dc4vJy1dmhUoCqIRMcnhIiF14seSCFdwEn1ciH-HKDQIntSxUrEX5xrcjSWFBAPD3ZSI1dWUAA; prodwow-auth-token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYmYiOjE3MTU4NzM1MjAsImV4cCI6MTcxNTg3NzEyMCwiaWF0IjoxNzE1ODczNTIwLCJpc3MiOiJXb29sd29ydGhzIiwiYXVkIjoid3d3Lndvb2x3b3J0aHMuY29tLmF1Iiwic2lkIjoiMCIsInVpZCI6ImY0NzA3ZmZhLTUyMzktNGRjOS05ZWZjLTczZWQ4YmVlOWEwYSIsIm1haWQiOiIwIiwiYXV0IjoiU2hvcHBlciIsImF1YiI6IjAiLCJhdWJhIjoiMCIsIm1mYSI6IjEifQ.Uq377pgBDrWUz6N3JtO2GSfZFzR9IDVOs2nei30Ockhz_zNCjXxVmHN70ITIDuA9yI8cBzhH-YaFBPQkhmHa4MDgW6RezKrqweFQG67KLDL8e2FTi112yR3qlop9JVVjJHeVfpc5MlgjPrecLVTVGI9bT-o-q1SFsdoiNypxW6ATkG7leu-7i9aQx2jluGCcn8eZSlJoYxXL9-xpgGmIBkTlpEmDt5pnqaJ1MvrLrn1Mv9DVN552vwqffhZOFoAn_9ichd3fqOh4Dc4vJy1dmhUoCqIRMcnhIiF14seSCFdwEn1ciH-HKDQIntSxUrEX5xrcjSWFBAPD3ZSI1dWUAA; bm_mi=2B3BADB7852CD3EC6D9D13B80B211971~YAAQPAUgF/s7tnmPAQAAPbMIghd/tfCbZDgEa18FeKfbzIjU4qrwUiJW7dBJuzQFSsJ5QKQMVPVYpTJM23G16yHZoCuYY5UJP6lgTuz7deeXK3hV3A8BBBuhy2A9VWeo1Zbd1Abn/JSsNL845NRpNBONErfSTdKgPD4g/Zi3v8Ia3vyoGqbt3Qm/gXCPLDdm1pptzxT2Vly1fZysZm/zXf2vuShimgv03knD1+lKCWfAlrRXeUXtTlRVuhy1Mzy2mkmwE2dC2HVBhtlkoilIbLZEaW57PY+ShSmsiN96EbgA9sIWHyuxcwtn+Y06R/sGQOeE0WgxxdCv2ndPqManxeXXsCExYCQqVA==~1; bm_sv=A39FD3C67B5C9119696BA29CA3221498~YAAQPAUgF508tnmPAQAAnsgIghde5Vdq2jUl20aDcDePWUOatFmClWFcNnTPlTaye8tT7FmKuNTM0OaPaqbyn/zfY9oH2TJ2Q6rxfQj0O1V611SXrWP73zyj+lNE8RJfxR0VO5qsCHOpJVVQ9hKkhY3+M4uolKSk2oflk++AyYE2QRyiEWIKhLh5Wq65oeEjabs2tn+JYbqyBWlDtpAA5UazcAm4G8gMcMQ8TWHoMy6NAC7lZTGyY2o4TaiY/oBfhOZ1t+yQuGA=~1; ak_bmsc=CF8AA80564606E74A3554A710901401C~000000000000000000000000000000~YAAQPAUgF5lktnmPAQAAp5sMghcwHCu+BnKd0UqPjFfUTYP490THXajL9E80cC375X3zV8Vbt4Z+18aRiwGfJrdE66hQWot2jYgZkSdx8/Tx4cgx2ZXhfE3lRjjfAKCXad/HxWHzCH48qP1XAjOPlpRt47873G6ZnZ7s0gcTyYDPp31P6ShVFV8dr2NDXv5cfA0eD2BxQHSKmPVg85qlNlbUoiRVbWZRT/ojuBiQMtADf7++bn32kDWqhcENioGtBkhq3FzbGKuCBYrAZg9Hs9zhNNAGI6rIF0xdJwX/rlh06cu6WwV0aK9EJr5sL4+ZhKC32FetPzqxjZoiqN3kKgro4yTIXElvfZM4CEwct/C8MM6MBKCwJi4LUDNseZ2yquroNTQMVqcIMmu9SltDLF3F2PDZUrNF03YBZuz+Ee9hC8ukrE/ftHI4v7ZGa5wY/Kl/yWzHc/dhtVXp; bm_sz=655EA0B5345290DE399584B96D5034B3~YAAQPAUgF2pltnmPAQAAjasMghdn15ItX+xIO+AiHg7OdI+wgH0Al1eWAfiaYKk7jdGCL6nt6q90m0nIttMn7q6PkrVyP2VMR7Q+kJs1qt2T2IbLOwxItw4GryWYs3SGpKFY4cQ9E3aoeuN6bQOUK2q6cmqioVMHXAAc/Vwiw0D7ORUx5VI5oJf9Sxst0Peefqs/kuZyMpw2VOWKou6s2gz3xJkpUGjwiZsSlVTLvTaxRPY1MLL2hCSBP3mwb68pnml4V7YXBFV/UspOzG2GdiXPOOou9YW2L92LeJnq/ynwBbL8ELyDFCh7LzB5ccsDPDg4dKxz3+yeXgnWy8xuZRVs62nAa0PgkDOOWSqh9AQa95Rf5ore7KixcBhWHrGDB1soTWJNMHIkj+qGCMR8Z8gzsi7XB5Fuq+lk1g9mBwNjlHcPlT4RpMPp~3621941~4405313; mbox=PC#caed45cb24fb4461bf934c9418f17cb5.36_0#1779075657|session#279825d2270d488e89d95db478321914#1715875681; AMCV_4353388057AC8D357F000101%40AdobeOrg=179643557%7CMCIDTS%7C19860%7CMCMID%7C13945814881315684679185098284510855405%7CMCOPTOUT-1715881020s%7CNONE%7CvVersion%7C5.5.0; ai_session=AvoakL30rO8ER3llfw8i9X|1715873520493|1715873821358; utag_main=v_id:018f7f7d2637004c8230cc5d67c804065001e05d008d7$_sn:6$_se:19$_ss:0$_st:1715875621374$vapi_domain:woolworths.com.au$dc_visit:6$ses_id:1715873521611%3Bexp-session$_pn:4%3Bexp-session$dc_event:2%3Bexp-session; _abck=17C5C9351EF6A7F72E9F99B927A103EE~-1~YAAQPAUgF+pltnmPAQAAwbMMggvf9EhTynIay1p2snixZwhkNwoc3liDipWkRO1qfcbW/ZGcgxDYEjtR9f/6IkY0CDkmWlLbDVIe+GLGVPc+gwDkLhHG0Ea2LVnagVGx7Xf7xfOiwASPqxp3Utwl+93gH8uK24ktDcEtUILhTKWecqNSJ25klni+yaLtpu/evRYcPfsbqdG+7AsvhY+LPs6jt0Kez2qaHFDts8no1flEMakaFKWHIuYmUAbMLHVIQz7Xfsp4f2qcVrZYJJXYE93XbtJYiyONCki39F1JCOe1iUBTmhMj8tIYnRg7yWSdzQoeQCTfWgzKQibNxZTJJKwuvkbGLBVI/TD0aZ++gmzeLosbQQsGi8aNlXYx21wT6ipmKCj42jpx/EWW/ZlfR6RgmCP/gcjl8+WNwwaFAA==~-1~||0||~1715877121",
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

    response = requests.request("POST", url, json=payload, headers=headers)

    #print(response.json())
    print("yay")
    #=== 

    data = response.json()
    macro_avgs = []
    for subdata in data["Products"]:
        prod = subdata["Products"][0]
        price = prod["InstoreCupPrice"]
        size = prod["CupMeasure"]
        try:
            nutri = json.loads(prod["AdditionalAttributes"]["nutritionalinformation"]) 
            for obj in nutri["Attributes"]:
                if obj["Id"] == 878: # protein
                    ratio = obj["Value"]
                    if not ratio[0].isdigit():
                        ratio = None
                    break
        except:
            ratio = None
        
        if not (price and size and ratio):
            continue
        price = Quantity(float(price), "")
        size = Quantity(size.lower())
        ratio = Quantity(ratio)/Quantity("100g")
        macro_avgs.append(ratio * size / price)
                                    
    # Average of the how many macros per weight
    res = np.sum(macro_avgs)/len(macro_avgs)
    # Convert liquid size
    if res.base_unit == BaseSet(meter=3):
        res *= Quantity(1000, "gram/liter")

    protein_per_dollar[food] = res

# Milk is cheap, but bean is apparently cheaper
