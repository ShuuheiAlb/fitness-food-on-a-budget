
import lib
import requests

macro_food_dict = {
    "protein": ["milk", "egg", "chicken", "beef", "pork", "sardine", "bean", "almond", "chia"],
    "carb": ["rice", "wholewheat-bread", "oat", "potato", "quinoa", "pasta", "corn"],
    "fat": ["avocado", "olive-oil", "peanut-butter", "greek-yoghurt", "cheese", "salmon", "tuna", "sardine", "almond"],
    #"fruit": ["berry", "banana", "apple", "orange", "grape", "pear", "kiwi", "lemon", \
    #          "watermelon", "pineapple", "mango"],
    #"vegetable": ["spinach", "cabbage", "lettuce", "brocolli", "cauliflower", "tomato", "carrot", "capsicum", \
    #              "zucchini", "mushroom", "choy buk"]
}

# prev = [20230510.01_v3.87.0, ]
url = "https://www.coles.com.au/_next/data/20240514.01_v3.88.0/en/browse/dairy-eggs-fridge/long-life-milk.json"

querystring = {"slug":["dairy-eggs-fridge","long-life-milk"]}

headers = {
    "cookie": "visid_incap_2800108=2lMoUVo8R4SVuO+0cVtfPzOHRGYAAAAAQUIPAAAAAACepBFFUqLMtDii9zlWzo11; AMCVS_0B3D037254C7DE490A4C98A6%40AdobeOrg=1; nlbi_2800108_2670698=cyIacuG0Pz3b/ep5vDjrSQAAAACk7r4lgnIIhljIjkplg9Cd; ld_user=d3766965-4c2d-4f3c-bfc4-e00600c82618; sessionId=d320f128-0491-44b8-9ee7-4f29a2df9e07; visitorId=904a466e-c644-4240-b8fe-778d62389ec1; ai_user=6j28BCbrPMMjTLQHachD4Y|2024-05-15T09:58:13.793Z; ApplicationGatewayAffinityCORS=ce1dd33cb7cfcf721c38e4c63f5c6894; ApplicationGatewayAffinity=ce1dd33cb7cfcf721c38e4c63f5c6894; nlbi_2800108=/tN7NhXYcX9JAtDuvDjrSQAAAAAEbpWuiR8dr8TYr8hg5Pfe; analyticsIsLoggedIn=false; at_check=true; dsch-visitorid=51dec869-4d45-4986-803b-35dd38692704; incap_ses_414_2800108=adC/avfWeD7NDmPG3tK+BWmhRGYAAAAAKtcQXCiUWoBaoiy3Rd9wqQ==; incap_ses_606_2800108=0QZeCVJyYRrWc94C3/FoCEpwRWYAAAAAR0tLRILe9bZrr/eX4L9iQA==; dsch-sessionid=4ffb0010-40dc-42c2-afa6-2d438434337c; x-jsession-id=0000FmNvo2iN85t_qdIeCE13xMl:1edavhs7p; reese84=3:dWUoahcSGbeIGktxKIkeGQ==:ghglLfKMYk6jWf6XZBclwJSUA5XRFpkdF1GVwuH9KGqcZE7KQEHBgnszP4Py6pe76VD/1+wfgo73g/JE96ZYERYU+gNBN6xeSGVAG8bK1V/psFH920ztnyui2EdrJ5ByBm4G4Urdg3bhBe9jmZNlgJ/M0K2p4SSBG3UgHAnpNPZifduKSh1k2J/3JfZt9hykTopHO00jdZromLZLTp+59BsvPpudKss/EqBaCAUSY/SreSc2ASEKSDAP8HlIinyqviNc1elYpWpJ/jpVkkU9yWAXeC7GdOZFrNOe5AZL4+LyZP/jCWIUFYwMk+kn58D21umPKuZPs2cvLj100ZN/fIuXSNn0dYQOksB4UBUDRexyPmchJcZhqBuh0QdrvUsGS0ZT34tYB6GQ795ed0B5FFqTjh1ClCtxPC5vx6KsDamSGr0fgZEoLaiWkKWyrHVou15pjfbhsob0v3dKQgyFdA==:r9ot4lrCfx9gfjbc5MHOyJ98lDcz2bH+4qXOtlHWRM0=; ad-memory-token=WTKojqs2988gfy8%2BRkXWKtI2tgwKmQEKDBIKCgg0MTYzOTAzUAoMEgoKCDkzMjEwNzBQCgwSCgoIOTMxNzkzNVAKDBIKCgg0NDkwMzMxUAoLEgkKBzQzOTY5M1AKDBIKCgg5NDExNzg0UAoMEgoKCDMyNjk2OTFQCgwSCgoINjI1NTM2NVAKDBIKCggzNzYyNjczUAoMEgoKCDM4OTcyNjRQEgwIgOmVsgYQtMSAggMaAggCIgA%3D; AMCV_0B3D037254C7DE490A4C98A6%40AdobeOrg=179643557%7CMCIDTS%7C19859%7CMCMID%7C07729037016612716601645457208853128120%7CMCAID%7CNONE%7CMCOPTOUT-1715835042s%7CNONE%7CvVersion%7C5.5.0; nlbi_2800108_2147483392=JVNMTCWeckNEG5TAvDjrSQAAAABRxXMks+sphseUqxrktT6y; ai_session=/SUdb7x3DzuU30hP1wBtiT|1715826940418|1715827844620; mbox=PC#22a58cbb0d3f46b292a054652d801fc1.36_0#1779072646|session#22a58cbb0d3f46b292a054652d801fc1#1715829706",
    "accept": "*/*",
    "accept-language": "en-GB,en;q=0.8",
    "baggage": "sentry-environment=prod,sentry-release=20240510.01_v3.87.0,sentry-transaction=%2Fbrowse%2F%5B...slug%5D,sentry-public_key=fe929b0cab4a4e3694d4ce2c52b13210,sentry-trace_id=1616ca2157e14fc09880f7724268f4dc,sentry-sample_rate=0.6",
    "priority": "u=1, i",
    "referer": "https://www.coles.com.au/browse/dairy-eggs-fridge/long-life-milk",
    "request-id": "|5a9eb2a066a14a78a097a961e39e83ba.ac1848acdebc4afb",
    "sec-ch-ua": '"Chromium";v="124", "Brave";v="124", "Not-A.Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Linux"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "sec-gpc": "1",
    "sentry-trace": "1616ca2157e14fc09880f7724268f4dc-bc5a8bf933528aaf-1",
    "traceparent": "00-5a9eb2a066a14a78a097a961e39e83ba-ac1848acdebc4afb-01",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "x-nextjs-data": "1"
}

response = requests.request("GET", url, headers=headers, params=querystring, verify=False)

response.raise_for_status()  # raises exception when not a 2xx response
if response.status_code != 204:
    print(response.json())
