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
        "Location": f"/shop/search/products?searchTerm{food}&pageNumber1",
        "PageNumber": 1,
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
        # the bm_sv cookie expires in 15 mins
        # the bm_szcookie expires in 2:15 hrs
        "cookie": "EnableLandingPageVideosContentService=true; EnableLandingPageIdeasContentService=true; bff_region=syd2; ai_user=kPh5vamjorsgTXCOnVyMmj|2024-05-16T03:40:54.478Z; akaalb_woolworths.com.au=~op=www_woolworths_com_au_ZoneA:PROD-ZoneA|www_woolworths_com_au_BFF_SYD_Launch:WOW-BFF-SYD2|~rv=59~m=PROD-ZoneA:0|WOW-BFF-SYD2:0|~os=43eb3391333cc20efbd7f812851447e6~id=fe10e758f65623b90951cb55a3b57c48; INGRESSCOOKIE=1715830855.768.1742.124094|37206e05370eb151ee9f1b6a1c80a538; at_check=true; AMCVS_4353388057AC8D357F000101%40AdobeOrg=1; s_cc=true; dtCookie=v_4_srv_5_sn_E86957BB17A9F4F1D708914D90CA01E5_perc_100000_ol_0_mul_1_app-3Af908d76079915f06_1_rcs-3Acss_0; bm_sz=120EB4F718A7601DE1354F4DB6E9B22E~YAAQrEnVy3ZLPXWPAQAAigUcgRcNQE64iZW+rdJqzFS2cEF1vBNIZxLt3PHzNrx97HaSxMEAKizaIC4pTY/FYwcBklQEjXjuStyknIuJKYp+jvtTp+VrkN0ZojWWQ6JwLJP0aszTmB1hqeVUwXQmZaLzAZgbeRCxnUSSegsK0Vrf5UU/XKkPS7PpDYnpVDPlQ7s3PfL/NJVldx2GgsDzcV0K50ZfnUy3CQUSkuyKCL3Yhjmi6aMWODxsTOPqcDUyFdU72ivm6TE3SPNWt/d89HXcAVAUz37yIfCnCAcq+HdStFvG/hjW01hCxGhQqhc14YtY1U8LPOW0P1OifVeLSy15VtaI7JoPCybWVr0JYMaDiqdiikKV5eIjuBpmIOY43mxRltPL7guevYgVVJJ9oFRYNQEojZ/OXXmuXySnwfCoT8hkqiPs9WGzTE+8gSzlJJ+eiPtU7M9e40BG5+u15biFNGRkog4dgrK5Xzxavw==~4404547~3289397; BVImplmain_site=14865; fullstoryEnabled=false; w-rctx=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYmYiOjE3MTU4NjE4ODksImV4cCI6MTcxNTg2NTQ4OSwiaWF0IjoxNzE1ODYxODg5LCJpc3MiOiJXb29sd29ydGhzIiwiYXVkIjoid3d3Lndvb2x3b3J0aHMuY29tLmF1Iiwic2lkIjoiMCIsInVpZCI6IjlmNjNiNTFjLWY3OGYtNGJjNi04Yzk1LWM5NmI5MjcyNWRjOCIsIm1haWQiOiIwIiwiYXV0IjoiU2hvcHBlciIsImF1YiI6IjAiLCJhdWJhIjoiMCIsIm1mYSI6IjEifQ.TtISoLMjR6_0ZGs2Fp1cFmj-1V92595OZiO9eJvaznqxLo0piomx79-HEZoWc8qNlqJIfAI0ly6uo5P4XhPOJw_Mb6lrBzkwrkeLNUDOfEBNhAwGsVA4Vg7f2NQW5OId61Hqn569bZLI5OJcUaD2Iv9axTZnaSb4ncpDLRCaJVNakDGj9AnGSzzy8A9ytM8mIA1JYAlcFMaPKdIp30Pcsp9dVtaz7QyI3aPdkUDPCSjPy8dVR-imEYDll91OSiRUNgPY5CV4N7zMUbBjxwhSn4DDOwA86LvkyWIT6pbjpQ3CciJeKQftU2AWsUUHWtehhHfaGI_Uy7stiEcOdY-e_Q; wow-auth-token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYmYiOjE3MTU4NjE4ODksImV4cCI6MTcxNTg2NTQ4OSwiaWF0IjoxNzE1ODYxODg5LCJpc3MiOiJXb29sd29ydGhzIiwiYXVkIjoid3d3Lndvb2x3b3J0aHMuY29tLmF1Iiwic2lkIjoiMCIsInVpZCI6IjlmNjNiNTFjLWY3OGYtNGJjNi04Yzk1LWM5NmI5MjcyNWRjOCIsIm1haWQiOiIwIiwiYXV0IjoiU2hvcHBlciIsImF1YiI6IjAiLCJhdWJhIjoiMCIsIm1mYSI6IjEifQ.TtISoLMjR6_0ZGs2Fp1cFmj-1V92595OZiO9eJvaznqxLo0piomx79-HEZoWc8qNlqJIfAI0ly6uo5P4XhPOJw_Mb6lrBzkwrkeLNUDOfEBNhAwGsVA4Vg7f2NQW5OId61Hqn569bZLI5OJcUaD2Iv9axTZnaSb4ncpDLRCaJVNakDGj9AnGSzzy8A9ytM8mIA1JYAlcFMaPKdIp30Pcsp9dVtaz7QyI3aPdkUDPCSjPy8dVR-imEYDll91OSiRUNgPY5CV4N7zMUbBjxwhSn4DDOwA86LvkyWIT6pbjpQ3CciJeKQftU2AWsUUHWtehhHfaGI_Uy7stiEcOdY-e_Q; prodwow-auth-token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYmYiOjE3MTU4NjE4ODksImV4cCI6MTcxNTg2NTQ4OSwiaWF0IjoxNzE1ODYxODg5LCJpc3MiOiJXb29sd29ydGhzIiwiYXVkIjoid3d3Lndvb2x3b3J0aHMuY29tLmF1Iiwic2lkIjoiMCIsInVpZCI6IjlmNjNiNTFjLWY3OGYtNGJjNi04Yzk1LWM5NmI5MjcyNWRjOCIsIm1haWQiOiIwIiwiYXV0IjoiU2hvcHBlciIsImF1YiI6IjAiLCJhdWJhIjoiMCIsIm1mYSI6IjEifQ.TtISoLMjR6_0ZGs2Fp1cFmj-1V92595OZiO9eJvaznqxLo0piomx79-HEZoWc8qNlqJIfAI0ly6uo5P4XhPOJw_Mb6lrBzkwrkeLNUDOfEBNhAwGsVA4Vg7f2NQW5OId61Hqn569bZLI5OJcUaD2Iv9axTZnaSb4ncpDLRCaJVNakDGj9AnGSzzy8A9ytM8mIA1JYAlcFMaPKdIp30Pcsp9dVtaz7QyI3aPdkUDPCSjPy8dVR-imEYDll91OSiRUNgPY5CV4N7zMUbBjxwhSn4DDOwA86LvkyWIT6pbjpQ3CciJeKQftU2AWsUUHWtehhHfaGI_Uy7stiEcOdY-e_Q; AKA_A2=A; ak_bmsc=1FEE63DCB7FBE3E780ACD411125D9ABB~000000000000000000000000000000~YAAQogUgF0WlMXyPAQAAIn55gRcYPuBAbUKpXzuRHPQgULSnKHuiZu/Upqsw11quMiedluXNsXRLN++HArRnrOwjBS/d3b+n0LeQZ5yO3l7TgugGKrrcztJcZL3CG439EQybmP82899M4KoqXR39AqK06jYaGxvDOnH5hbG6X97zoLCQCBkRPB5x9RioJnDrlhoO6yw0kzWS1kG/wpaPNRQQ7O1b5MT5nNrwCcgMBZc+1K3Eje8di+d/y+Juj1uOevRLmjOriONhG/b2I11XO8G8E6EwB9TEfmDwVMNAmU6Y2IV1+1JsOtXph4CqwiPhgv+EifPhZ3OrzOfaLQcFF6ODYbbX8l3TpKoKuwA3pkyvGKne1JJ8oRloesypzVTiQwfjHbCCvzzzDOHzj7U1k4h5Lg==; mbox=PC#caed45cb24fb4461bf934c9418f17cb5.36_0#1779075657|session#5dd7b8e893dc4092abbf9270c81eee02#1715866035; AMCV_4353388057AC8D357F000101%40AdobeOrg=179643557%7CMCIDTS%7C19860%7CMCMID%7C13945814881315684679185098284510855405%7CMCOPTOUT-1715871374s%7CNONE%7CvVersion%7C5.5.0; utag_main=v_id:018f7f7d2637004c8230cc5d67c804065001e05d008d7$_sn:5$_se:30$_ss:0$_st:1715865976007$vapi_domain:woolworths.com.au$dc_visit:5$ses_id:1715862537045%3Bexp-session$_pn:6%3Bexp-session$dc_event:6%3Bexp-session; ai_session=wsSOZ04sFDyYML1VXwed+Q|1715852199700|1715864176449; _abck=17C5C9351EF6A7F72E9F99B927A103EE~-1~YAAQogUgF9mlMXyPAQAAu4d5gQth0fcGg+8bcEzw6STuI5eeMQ0norKJYcu4wAq1e+q8gaDetuYNZgfXT9B4mRvBaCjCJeajcq6A1DstN7XYOPtT5Gp2bJcARZogonMAykfwkBr0ZJSDX40bh9+CJPFYE8jESN64hrZrRnG+pikf7/mLjy/2I8vy9T+9G1rAImBRxpTzhb3KEI0TpupGksB+FbIymjyuEHL+3bBO0x8oYbTGsjLuPzHGZmCZd6A5uZN0a6BStpCrBicgKc11xUV1lD9zcpTwbbmOuH2fwLlu+sV3kP5WfcBITJ2l6Y0kEUILHkWvDDzKmxh0kF2uSPrpM+XrNWubIYgv4DgPhfEpB3DtRVfFdPuQnLUWxcDK3Lxd+v0=~-1~-1~1715866831; bm_mi=1B03158CB7B642B30782970783311C90~YAAQogUgF9qlMXyPAQAAu4d5gRfQUXt0xqrKTJJ8pa5s2RvsdIeTa/fuhHG69tL2mmRdRJcn3DLriY6Zva/iqB8mCeZ4TUkJZvV4eqnXYTt8HhUt9LJuO/JNTj4RFZML1CiLZ6kW6OAFjCrCz9qCPOM3dP1/YFjUKqRktFnWwlZJfl0xzzoWmwoKRzyt89sUE/eUwzDvVPCzNoA6ABtSNFF9+7H3Zp62EaEcyPaNFGWwxqSoCT9gZN+u/3zbVn3I9Rz1Lu06Tx+iut4p9cNCVV+oLaPEdTOMPXEUk0EUIkQ28IS2NPnXn9iNg9OTHIRIEq+4DSluL3xVbTB6Ji7T7pWRUFl3/giGbMxUhkT+~1; bm_sv=6B9E4DD519EBB83D9FD07C2A5B3DD268~YAAQogUgF9ulMXyPAQAAu4d5gRdNQvspP1eXL4RF2fSmPv8n1SDg2EGtapl+lFB5Mtkxp06Ymeb93CTcePtQYzZpMzKnOdycJ/FrnXUmXA+WhUQYEqgv1eHCLigeRZoFIj+zxigW4nEaprOJLvt0HTBWKVhIoDEIiDq5uG/lpvjiqo/Ws//uCsG9Ae7x2qvWGQNl0H1G1azx+6YLa5Te2tluQuYvhz9hsQ7ozW9p8GCPDDbTy56DGen5S8adOoVZ5w6/jneQyMw=~1",
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-GB,en;q=0.9",
        "content-type": "application/json",
        "origin": "https://www.woolworths.com.au",
        "priority": "u=1, i",
        "referer": f"https://www.woolworths.com.au/shop/search/products?searchTerm={food}&pageNumber=1",
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

    #=== 

    data = response.json()
    prices = []
    sizes = []
    macro_ratios = []
    for subdata in data["Products"]:
        prod = subdata["Products"][0]
        price = prod["InstorePrice"]
        size = prod["PackageSize"]
        try:
            nutri = json.loads(prod["AdditionalAttributes"]["nutritionalinformation"]) 
            for obj in nutri["Attributes"]:
                if obj["Id"] == 878: # protein
                    macro_ratio = obj["Value"]
                    if not macro_ratio[0].isdigit():
                        macro_ratio = None
                    break
        except:
            macro_ratio = None
        
        if not (price and size and macro_ratio):
            continue
        prices.append(Quantity(float(price), ""))
        sizes.append(Quantity(size.lower()))
        macro_ratios.append(Quantity(macro_ratio)/Quantity("100g"))
                                    
    # Averagely (sum price)/(sum ratio * size)
    res = np.dot(macro_ratios, sizes) / np.sum(prices)
    # Convert liquid size
    if res.base_unit == BaseSet(meter=3):
        res *= Quantity(1000, "gram/liter")

    protein_per_dollar[food] = res

# Milk = 13g per dollar
# Egg = 10.33g per dol;ar
