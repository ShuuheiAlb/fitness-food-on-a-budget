from coles import coles_search
from woolies import woolies_search
from googlesheet1 import google_sheet_wr

# Minimum viable product:
# MILK, EGG, CHICKEN BREAST, BEEF, SALMON, BEAN, (SARDINE, CHEESE, YOGHURT)
# RICE, WW BREAD, OAT, POTATO, QUINOA, PASTA, CORN
# PB, AVODACO, OLIVE OIL, ALMOND, CHIA, BUTTER
# BERRIES, BANANA, APPLE, ORANGE, GRAPE, (PEAR, KIWI, WATERMELON, MANGO)
# SPINACH, BROCOLLI, TOMATO, CABBAGE, CARROT, PEA, (CAPSICUM, ZUCHINNI, SPROUT)

item_to_search = str(input("Please input your item: "))

coles_list = coles_search(suburb="cockburn wa", item=item_to_search)
status = google_sheet_wr(list=coles_list, range="shop!C2")
woolies_list = woolies_search(item=item_to_search)
status2 = google_sheet_wr(list=woolies_list, range="shop!F2")
