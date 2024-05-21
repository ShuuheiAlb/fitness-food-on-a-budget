
#%%

import lib
import requests
import re
from bs4 import BeautifulSoup

macro_food_dict = lib.macro_foods
ureg = lib.ureg
Q_ = lib.Q_

# Initialise session
# Quirk: find a specified date_version to access API url path
s = requests.Session()
init_r = s.get(**lib.requests_kwargs["coles_init"])
date_version = re.search(r'src="/_next/static/([0-9\.]+_v[0-9\.]+)/.+.js"', init_r.text). \
                    groups()[0]

# %%

food = "milk"
macro = "protein"
srch = lib.requests_kwargs["coles_search"]
srch_r = s.get(**srch(food, date_version))
#print(srch_r.json())

#%%

#Try Selenium

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

profile = webdriver.FirefoxProfile('../snap/firefox/common/.mozilla/firefox/profiles.ini')

PROXY_HOST = "12.12.12.123"
PROXY_PORT = "1234"
profile.set_preference("network.proxy.type", 1)
profile.set_preference("network.proxy.http", PROXY_HOST)
profile.set_preference("network.proxy.http_port", int(PROXY_PORT))
profile.set_preference("dom.webdriver.enabled", False)
profile.set_preference('useAutomationExtension', False)
profile.update_preferences()
desired = DesiredCapabilities.FIREFOX

driver = webdriver.Firefox()
geckodriver_path = "/snap/bin/geckodriver"
driver_service = webdriver.FirefoxService(executable_path=geckodriver_path)
options = Options() # headless browser
options.add_argument('--headless')

driver = webdriver.Firefox(firefox_profile=profile, desired_capabilities=desired,
                           service=driver_service, options=options)
#driver.add_cookie(s.cookies.get_dict())

#%%

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
            spec = lib.requests_kwargs["coles_spec"]
            sub_url = "-".join(re.split(r"[^A-Za-z0-9]+", item["description"])) + "-" + str(item["id"])
            
            # Prev using requests + bs4s
            """
            spec_r = s.get(**spec(sub_url))
            soup = BeautifulSoup(spec_r.text, 'html.parser')
            print(soup.findChildren("table"))
            table = soup.findChildren("table")[0]
            rows = table.findChildren('tr')
            for row in rows:
                cells = row.findChildren(['td', 'th'])
                if cells[0].text.lower() == macro.lower():
                    ratio = Q_(cells[1].text)/100
            """
            
            driver.get(spec(sub_url)["url"])
            wait = WebDriverWait(driver, 10)
            table = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'table')))
            is_prevly_macro_indicator = False
            ratio = None
            for cell in table.find_elements(By.TAG_NAME, "div"):
                res = cell.get_attribute('innerHTML')
                if res.lower() == macro:
                    is_prevly_macro_indicator = True
                elif is_prevly_macro_indicator:
                    ratio = Q_(res)/100
                    print(ratio)
                    break
        except:
            continue
        
        mpaud = ratio * size / price

        # If liquid, convert the unit from volume to mass
        if mpaud.check("[volume]"):
            mpaud *= Q_("1000 gram/liter")
        
        mpauds.append(mpaud)

# Average from all items
macro_per_AUD_overall = sum(mpauds)/len(mpauds)
print([macro, food, str(macro_per_AUD_overall.to("gram"))])





# %%
