#%%
import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from os.path import getmtime
from datetime import datetime

# Importing dataset
# Supermarket name appearing on variables are aliased as "supa" (Woolworths) and "supb" (Coles)

with open("style.css") as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

df = pd.read_csv("out/supa_out.csv", header=0)
df["Amount/$"] = df["Amount/$"].apply(lambda x: float(x.replace(" gram", "")))

st.title("Fitness Food on a Budget")

curr_cat = st.selectbox(
   "Macronutrient (in gram/$)",
   ("protein", "carb", "fat", "fruit", "vegetable"),
   index=0,
   placeholder="Select"
)
curr_data = df[df["Category"] == curr_cat]

# Main plot
fig = plt.figure(figsize=(12, 6))
ax = sns.barplot(x='Amount/$', y='Food', hue='Food', data=curr_data.sort_values(by="Amount/$", ascending=False),
               palette=sns.color_palette(palette="pastel", n_colors=len(curr_data)), legend=False)

# Styling: colors etc
sns.set_style("white")
sns.despine(left=True, bottom=True)

# Labels, ticks etc
ax.set(xlabel="", ylabel="")
ax.tick_params(axis='x', bottom=False, labelbottom=False)
ax.tick_params(axis='y', left=False, labelsize=14)
for i in ax.containers:
    ax.bar_label(i, fmt="%.1f", padding=10, size=12)

st.pyplot(fig)

st.caption(f"*(as of {datetime.fromtimestamp(getmtime('out/supa_out.csv')).strftime('%d %b %Y')})*")

# %%
