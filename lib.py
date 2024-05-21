
#
# Library for web scraping
#

import pint

# Food options and constants
macro_foods = {
    "protein": ["milk", "egg", "chicken", "beef", "pork", "sardine", "bean", "almond", "chia"],
    "carb": ["rice", "wholewheat-bread", "oat", "potato", "quinoa", "pasta", "corn"],
    "fat": ["avocado", "olive-oil", "peanut-butter", "greek-yoghurt", "cheese", "salmon", "tuna", "sardine", "almond"],
    #"fruit": ["berry", "banana", "apple", "orange", "grape", "pear", "kiwi", "lemon", \
    #          "watermelon", "pineapple", "mango"],
    #"vegetable": ["spinach", "cabbage", "lettuce", "brocolli", "cauliflower", "tomato", "carrot", "capsicum", \
    #              "zucchini", "mushroom", "choy buk"]
}

ureg = pint.UnitRegistry()
Q_ = ureg.Quantity

# The long request's url, payload, header etc
requests_kwargs = {
    "woolies_init": {
        "url": "https://www.woolworths.com.au/",
        "headers": {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "sec-ch-ua": '"Chromium";v="124", "Brave";v="124", "Not-A.Brand";v="99"',
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        }
    },
    "woolies_search": lambda var: {
        "url": "https://www.woolworths.com.au/apis/ui/Search/products",
        "json": {
            "Location": f"/shop/search/products?searchTerm{var}",
            "SearchTerm": f"{var}",
            "PageSize": 10,
            "Filters": []
        },
        "headers": {
            "accept": "application/json, text/plain, */*",
            "content-type": "application/json",
            "origin": "https://www.woolworths.com.au",
            "referer": f"https://www.woolworths.com.au/shop/search/products?searchTerm={var}",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        }
    },
    "coles_init": {
        "url": "https://www.coles.com.au/",
        "headers": {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8",
            "accept-language": "en-GB,en;q=0.5",
            "sec-ch-ua": '"Chromium";v="124", "Brave";v="124", "Not-A.Brand";v="99"',
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        },
        "verify": False
    },
    "coles_search": lambda var, date_version: {
        "url": f"https://www.coles.com.au/_next/data/{date_version}/en/search/products.json",
        "params": { "q": var, "page": "1" },
        "headers": {
            "accept": "*/*",
            "accept-language": "en-GB,en;q=0.5",
            "referer": f"https://www.coles.com.au/search/products?q={var}",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        },
        "verify": False
    },
    "coles_spec": lambda var, date_version, q: {
        "url": f"https://www.coles.com.au/_next/data/{date_version}/en/{var}.json",
        "params": { "slug": var },
        "headers": {
            "accept": "*/*",
            "accept-language": "en-GB,en;q=0.5",
            "sec-ch-ua": '"Chromium";v="124", "Brave";v="124", "Not-A.Brand";v="99"',
            "referer": f"https://www.coles.com.au/search/products?q={q}",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        },
        "verify": False
    }
}