import requests

url = "https://www.woolworths.com.au/apis/ui/Search/products"

payload = {
    "Filters": [],
    "IsSpecial": False,
    "Location": "/shop/search/products",
    "PageNumber": 1,
    "PageSize": 36,
    "SortType": "TraderRelevance",
    "IsRegisteredRewardCardPromotion": None,
    "ExcludeSearchTypes": ["UntraceableVendors"],
    "GpBoost": 0,
    "GroupEdmVariants": True,
    "EnableAdReRanking": False
}
headers = {
    "cookie": "EnableLandingPageVideosContentService=true; EnableLandingPageIdeasContentService=true; AKA_A2=A; bff_region=syd2; ai_user=kPh5vamjorsgTXCOnVyMmj|2024-05-16T03:40:54.478Z; akaalb_woolworths.com.au=~op=www_woolworths_com_au_ZoneA:PROD-ZoneA|www_woolworths_com_au_BFF_SYD_Launch:WOW-BFF-SYD2|~rv=59~m=PROD-ZoneA:0|WOW-BFF-SYD2:0|~os=43eb3391333cc20efbd7f812851447e6~id=fe10e758f65623b90951cb55a3b57c48; INGRESSCOOKIE=1715830855.768.1742.124094|37206e05370eb151ee9f1b6a1c80a538; w-rctx=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYmYiOjE3MTU4MzA4NTQsImV4cCI6MTcxNTgzNDQ1NCwiaWF0IjoxNzE1ODMwODU0LCJpc3MiOiJXb29sd29ydGhzIiwiYXVkIjoid3d3Lndvb2x3b3J0aHMuY29tLmF1Iiwic2lkIjoiMCIsInVpZCI6ImNlMWNhOGYyLWJkZDAtNGU5Yi05YWJiLTJhZDQ3Y2YyNDFkNiIsIm1haWQiOiIwIiwiYXV0IjoiU2hvcHBlciIsImF1YiI6IjAiLCJhdWJhIjoiMCIsIm1mYSI6IjEifQ.ODNGqwVUFnkV5wmLlblaWy0QM8oFZiTmVaMgF53FdWl4RyD0d2rH-60EqqhJ7t6Yc6DjTB_-7iFHiXoIvczzvBGAeIAl8txkPwV6ItyA4Cylv5o_m4RSkC5WIHtveMml2MYfiMawe3Kz9OiMQW3Q6v8lfsXwhR74Gh-bPcsLvVy4spYqImwNvgjy6q4pE19zLuci9Ssx0WFMN3Q_jX11aH_c_gsSsiZeNdYPavzEKiAlttFQ9-w9c-euAmGzE6NRzhG7qBDE9sQ4KWrAs5qlylGuBc6pNGsX1Mrz5cPB0wGGJ5mfIYj48vECg5h0mubrxr4N2DYrivQ1MS01aIg9dw; wow-auth-token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYmYiOjE3MTU4MzA4NTQsImV4cCI6MTcxNTgzNDQ1NCwiaWF0IjoxNzE1ODMwODU0LCJpc3MiOiJXb29sd29ydGhzIiwiYXVkIjoid3d3Lndvb2x3b3J0aHMuY29tLmF1Iiwic2lkIjoiMCIsInVpZCI6ImNlMWNhOGYyLWJkZDAtNGU5Yi05YWJiLTJhZDQ3Y2YyNDFkNiIsIm1haWQiOiIwIiwiYXV0IjoiU2hvcHBlciIsImF1YiI6IjAiLCJhdWJhIjoiMCIsIm1mYSI6IjEifQ.ODNGqwVUFnkV5wmLlblaWy0QM8oFZiTmVaMgF53FdWl4RyD0d2rH-60EqqhJ7t6Yc6DjTB_-7iFHiXoIvczzvBGAeIAl8txkPwV6ItyA4Cylv5o_m4RSkC5WIHtveMml2MYfiMawe3Kz9OiMQW3Q6v8lfsXwhR74Gh-bPcsLvVy4spYqImwNvgjy6q4pE19zLuci9Ssx0WFMN3Q_jX11aH_c_gsSsiZeNdYPavzEKiAlttFQ9-w9c-euAmGzE6NRzhG7qBDE9sQ4KWrAs5qlylGuBc6pNGsX1Mrz5cPB0wGGJ5mfIYj48vECg5h0mubrxr4N2DYrivQ1MS01aIg9dw; prodwow-auth-token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYmYiOjE3MTU4MzA4NTQsImV4cCI6MTcxNTgzNDQ1NCwiaWF0IjoxNzE1ODMwODU0LCJpc3MiOiJXb29sd29ydGhzIiwiYXVkIjoid3d3Lndvb2x3b3J0aHMuY29tLmF1Iiwic2lkIjoiMCIsInVpZCI6ImNlMWNhOGYyLWJkZDAtNGU5Yi05YWJiLTJhZDQ3Y2YyNDFkNiIsIm1haWQiOiIwIiwiYXV0IjoiU2hvcHBlciIsImF1YiI6IjAiLCJhdWJhIjoiMCIsIm1mYSI6IjEifQ.ODNGqwVUFnkV5wmLlblaWy0QM8oFZiTmVaMgF53FdWl4RyD0d2rH-60EqqhJ7t6Yc6DjTB_-7iFHiXoIvczzvBGAeIAl8txkPwV6ItyA4Cylv5o_m4RSkC5WIHtveMml2MYfiMawe3Kz9OiMQW3Q6v8lfsXwhR74Gh-bPcsLvVy4spYqImwNvgjy6q4pE19zLuci9Ssx0WFMN3Q_jX11aH_c_gsSsiZeNdYPavzEKiAlttFQ9-w9c-euAmGzE6NRzhG7qBDE9sQ4KWrAs5qlylGuBc6pNGsX1Mrz5cPB0wGGJ5mfIYj48vECg5h0mubrxr4N2DYrivQ1MS01aIg9dw; at_check=true; AMCVS_4353388057AC8D357F000101%40AdobeOrg=1; fullstoryEnabled=false; s_cc=true; bm_mi=E6F0ECDABD6CD18843E186EC393F5FB9~YAAQ1EnVy3IrIWSPAQAASBWbfxcbyI7CK/jl7sc4WQ41AgcMggPa+xoXSk5YTyBuV9i76/aOXZKKuanjfQ3x7V2xyH1Gpb4KVpFRq/n1sKFNN6OLDqb3/4Fx9taqWACr490FAZcNV9CVm/kmTzhHqLopuYLxYiV8MtQdMXT2DH0NymRs4j0VaU6Q6C/gOMOIb/JpqZMcGuypQhJSWhywqfdmVq+BUeEsQ9pytpWG6m68NpB7DJ8POkoVXnBWdy/KR1EXytKOLgdLI+y3D1rZx7Uv83Q7GSKNJAnJvartcbrQUf2n/geusYjx69SpVYz17w3ol2OzLiHE/vJYrbeedTmoq5cZv21ANqJ7HyXaqOEoIG/F0z8i~1; bm_sv=5C70369C7132993B51B781822CE566A7~YAAQ1EnVyzowIWSPAQAAwS6bfxftJbQSA10QIJ6XWHbIygyGILdnrdILW6KDtG5WC3sMqfuV3uBXNxGTDqX1XSDQsAo9NDSBXydgb8ynV3osqDgN8wA4cDu0ob23clgx+IiwlihgjdkQJR1UIYNnTNqCWsMxUPhtfZNYJhuGiavMaER+TiClvClLd1YKSk8A/NYLFKSIqAlQbBbV9wFxOCfWqM1bFK5GdMhLB33WX0sbJAMKA0sEna8uIUjHz9OKTLwyMb/msJM=~1; ak_bmsc=74E5755E185B65DAB67E3471CE9BCF2B~000000000000000000000000000000~YAAQ1EnVy2vUIWSPAQAA54qefxemsFun48TGGiLkmU1g68LYI2op4BNhEG/OU+Q8xWT3zLhmSd8fIGLzxaBOxEyZfA+xdv8k3JiVzAVWQH2PD+Nb/EZiexaLn6b738lIG/PoNFzp04ZBcXJ9SKPncLm5GAq2+rSk0sfMpsCFyZI5XO/i5aYlA75ZXYlRJUc+6REHdFR6cF3Mpn2B/eKzRS+dF3XTQvRDoBOwmJqXQQT3Tunx3Mo1DByUTHC34hr6BDr4kINy09rXYCcmD8TMraNk7wQlUyyBIY/1KoNsKy6kY63EI9Ekp8sXzREFFfvOsbgrbv8T4kDR0KEJKpqzvhHiyqd0txTsrCB3iRcDbIjTbCLJrHjtmIgd+2sB2J28Wqe3M4HxPx5doPZwrqlPYub+z/ts9wixPSIgRLc4ib3iWcTif6qgAM23D+cqZxx4zmnLdKhPOmXvVX7/uZ6Lo6YXhgbZUKz6nw8=; dtCookie=v_4_srv_5_sn_E86957BB17A9F4F1D708914D90CA01E5_perc_100000_ol_0_mul_1_app-3Af908d76079915f06_1_rcs-3Acss_0; bm_sz=894F8F293DB23B9440074F234E116649~YAAQ1EnVyzSNImSPAQAAZwGifxdBpX+laJ8+nfYeBGsBfeRPQObadXRbYptbCHK7xoc61wAy/CBXjB6Ik+/F0v8kIIS4MQR2pTMlkjc5iCLqTGwSJof8p4R1fkmIB7hnMHP3Ng1Y8euOfHiC+yNW7PuImolzDBX8tKMHL/5Eyof3R/ouutvNohEN7BauRaK4sIFC8bDFjjPF9TmLdI0M6vAmXozzYsvIYZv+NPOV4DYo0zJHesyXB0vIV0SGslOlxaL7QDNJ+9QXEAEi+EGKTlPO9Z7MfUlr4xm1L7l7X3V3F6vzTLIDfaEBlC8hCixy0H44fmAMm6NTdJxOLmnfMspfHAR/u2h85RqpbhEarbmMFi4S3A2UYZx0qjx1YzLbeoYumMHnD5gAg6gh9NHomksjCAV6daZh0yIyaave+HuKhZjdhIp+Z8QUxRdcN5U=~3488068~3551811; mbox=session#caed45cb24fb4461bf934c9418f17cb5#1715835136|PC#caed45cb24fb4461bf934c9418f17cb5.36_0#1779075657; AMCV_4353388057AC8D357F000101%40AdobeOrg=179643557%7CMCIDTS%7C19860%7CMCMID%7C13945814881315684679185098284510855405%7CMCOPTOUT-1715840475s%7CNONE%7CvVersion%7C5.5.0; utag_main=v_id:018f7f7d2637004c8230cc5d67c804065001e05d008d7$_sn:1$_se:47$_ss:0$_st:1715835076633$ses_id:1715830859320%3Bexp-session$_pn:4%3Bexp-session$vapi_domain:woolworths.com.au$dc_visit:1$dc_event:11%3Bexp-session; ai_session=4FdbfI2EN60y7siBG4m/Qr|1715830854810|1715833276668; _abck=17C5C9351EF6A7F72E9F99B927A103EE~-1~YAAQ1EnVy8GOImSPAQAAUwmifwuOUF11EYLvaYVocyL4QYzwYqwooLlLGVsYX7a1QZBPPt6CShdZit5yoBUZr2461iYzd9xhpLP5GzNqjrK44a8JB/YIkJd8W//A0xwmkxePtaagdGVULxYvD1mXRgFeiKaj8zM3ILeoTWyUYT3G40wRKs3IWa+Ke+t9y+DzAFuo1a1SetElZkCsGMnUafTWVbkpiikD7dzG+OR43HLG53gCZQl7YEub5SjNcahzwr9AHpBpV/TbbKAzGpR1ZF/lKFoeR9VE9u8DuWmsmCinN1YXQIhfttq6kaxJHYAQtVVAh+w+su/XxCxQsrvYYhgb/X2+POMYWd3wz1q5OvRlvCB4QIqgdlaObf0xtl4RSnXNtLECRj5CTsgqr6Bfdw==~-1~||0||~1715834455",
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-GB,en;q=0.9",
    "content-type": "application/json",
    "origin": "https://www.woolworths.com.au",
    "priority": "u=1, i",
    "referer": "https://www.woolworths.com.au/shop/search/products",
    "request-id": "|717a0d8040b94fc0a0e7651be8ed3c7a.4e34850eb3de40bc",
    "sec-ch-ua": '"Chromium";v="124", "Brave";v="124", "Not-A.Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Linux"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "sec-gpc": "1",
    "traceparent": "00-717a0d8040b94fc0a0e7651be8ed3c7a-4e34850eb3de40bc-01",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}

response = requests.request("POST", url, json=payload, headers=headers)

print(response.json())

# then parse them acc to nutritional price etc
