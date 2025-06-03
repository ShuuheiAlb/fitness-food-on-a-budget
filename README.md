
# Fitness Food on a Budget: Infographics

This project summarises the macronutrients you get per dollar from common foods at major Australian supermarkets. The goal is to help you make smarter, budget-friendly food choices that still support your fitness goals.

**Current Status:** The Woolworths data collection and visualization are complete. Coles implementation is in progress (delayed due to bot prevention measures on their website).

![Current visualisation](data/image.png)


## Data Collection Methodology

I collected data by scraping the first page of search results for each food category, then calculated median values from in-stock items to determine typical nutrient content per AUD$.


### Why Median of In-Stock Items?

This approach models a realistic shopping scenario where a customer walks down a supermarket aisle looking at a specific food category.

**The Customer Shopping Model:**
- Customers only see items that are currently in stock on the shelf
- Each visible product (different brands, sizes, packaging) represents one choice option
- Customers are assumed to notice all available options and choose with equal probability

**Why Not Other Statistical Measures?**

**Mean:** Too volatile. Premium brands with fluctuating availability can skew results dramatically when they go in/out of stock.

**Weighted Mean:** Larger package sizes don't necessarily increase the likelihood of a customer choosing that particular macronutrient concentration.

**Minimum (cheapest option):** 
- Highly volatile due to stock fluctuations
- Cheapest options are often highly processed, contradicting fitness goals
- Larger "value" sizes may exceed customer needs (depending on lifestyle, family size, etc.)

**Why Different Sizes = Different Products?**
Products with the same brand but different sizes appear as separate options on the shelf, giving customers distinct choices with different macro/dollar ratios. Combining them would misrepresent the actual shopping experience.


## How to Use

1. Run `supa.py` (Woolworths scraper)
2. Run `supb.py` (Coles scraper - coming soon)
3. Start the visualization server:
   ```bash
   cd vis
   python3 -m http.server
   ```
4. Open `http://localhost:8000/` in your browser


## Tools Used

- Python with native libraries (or "close to native" libraries)
- d3.js for visualisation (previously: Streamlit)
- Insomnia (API testing)
- VS Code Notebook
- pipreqs (dependency management)


## Inspiration

This project was inspired by Jeremy Ethier's video on budget-friendly healthy eating:[watch here](https://www.youtube.com/watch?v=PXub4lr-9J8).


## Disclaimer

This project is intended for personal and educational purposes only. I take no liability for any consequences arising from the use of this project, nor am I affiliated with any of the mentioned companies.

---

*Note: This represents one of my first major data analysis projects, involving significant trial and error in data collection, methodology refinement, and visualization development.*
