
#
# Library for web scraping
# 

import pint
import random

# Food options and constants
macro_foods = {
    "protein": ["milk", "egg", "chicken", "beef", "pork", "sardine", "bean", "almond", "chia"],
    "carb": ["rice", "wholewheat-bread", "oat", "potato", "quinoa", "pasta", "corn"],
    "fat": ["avocado", "olive-oil", "peanut-butter", "greek-yoghurt", "cheese", "salmon", "tuna", "sardine", "almond"],
    "fruit": ["berry", "banana", "apple", "orange", "grape", "pear", "kiwi", "lemon"],
    "vegetable": ["spinach", "cabbage", "lettuce", "brocolli", "cauliflower", "tomato", "carrot", "capsicum", \
                  "zucchini", "mushroom", "choy buk"]
}

# Objects to handle units
ureg = pint.UnitRegistry()
Q_ = ureg.Quantity

# Randomised user agent
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 14.5; rv:126.0) Gecko/20100101 Firefox/126.0',
    'Mozilla/5.0 (X11; Linux i686; rv:126.0) Gecko/20100101 Firefox/126.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/124.0.2478.109'
]
weights = [0.59, 0.05, 0.15, 0.03, 0.02, 0.01, 0.15]

# The long request's url, payload, header etc
requests_kwargs = {
    "supa_init": {
        "url": "https://www.woolworths.com.au/",
        "headers": {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "user-agent": random.choices(user_agents, weights=weights)[0]
        }
    },
    "supa_search": lambda var: {
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
            "user-agent": random.choices(user_agents, weights=weights)[0]
        }
    },
    "supb_init": {
        "url": "https://www.coles.com.au/",
        "headers": {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8",
            "accept-language": "en-GB,en;q=0.5",
            "user-agent": random.choices(user_agents, weights=weights)[0]
        },
        "verify": False
    },
    "supb_search": lambda var, date_version: {
        "url": f"https://www.coles.com.au/_next/data/{date_version}/en/search/products.json",
        "params": { "q": var, "page": "1" },
        "headers": {
            "accept": "*/*",
            "accept-language": "en-GB,en;q=0.5",
            "referer": f"https://www.coles.com.au/search/products?q={var}",
            "user-agent": random.choices(user_agents, weights=weights)[0]
        },
        "verify": False
    },
    "supb_spec": lambda var, date_version, q: {
        "url": f"https://www.coles.com.au/_next/data/{date_version}/en/{var}.json",
        "params": { "slug": var },
        "headers": {
            "accept": "*/*",
            "accept-language": "en-GB,en;q=0.5",
            "referer": f"https://www.coles.com.au/search/products?q={q}",
            "user-agent": random.choices(user_agents, weights=weights)[0]
        },
        "verify": False
    }
}