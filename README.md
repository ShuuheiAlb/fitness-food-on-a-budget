# "Fitness Food on a Budget" Dashboard (In Progress)

This project calculates macronutrient contents per unit price across a range of common foods available in two major Australian supermarket chains (Woolworths and Coles), with a goal of helping customers make informed, budget-conscious choices to support their health.

The current visualisation is here: https://fitness-food-on-a-budget.streamlit.app/.

The data was collected from web scraping with minimal number of requests: for each food type, the first page of its search result will be used to calculate in-stock median as the representative value of food's macroonutrient amount per Australian Dollar.

The project is intended only for personal and educational purpose. I do not take any liabilities for any consequences resulting from the use of this project by others, nor am I affiliated with any of these companies.

## How to use

Run `supa.py` then `supb.py` then `streamlit run main.py`

## Other tools used

Insomnia, VS Code Notebook, pipreqs