from coles import coles_search
from woolies import woolies_search
from googlesheet1 import google_sheet_wr

# PLAN: MILK, EGG, CHICKEN BREAST, BEEF, SALMON, SARDINE, YOGHURT, CHEESE
# RICE, WW BREAD, OAT, SWEET POTATO, POTATO, QUINOA, CORN, PASTA, BEAN
# PB, AVODACO, OLIVE OIL, BUTTER, ALMOND/CASHEW, CHIA
# VEGGIES/FRUIT: 

item_to_search = str(input("Please input your item: "))

coles_list = coles_search(suburb="cockburn wa", item=item_to_search)
status = google_sheet_wr(list=coles_list, range="shop!C2")
woolies_list = woolies_search(item=item_to_search)
status2 = google_sheet_wr(list=woolies_list, range="shop!F2")
