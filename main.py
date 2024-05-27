#%%
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from os.path import getmtime
from datetime import datetime

# CSS: manually put it since Streamlit Deployment makes "the other way" much more complicated
# Otherwise for offline use, style.css can be used
css_str = '[class^="st-emotion"]  { font-weight: 500; }'
st.markdown( f'<style>{css_str}</style>' , unsafe_allow_html= True)

# Importing dataset
# Supermarket name appearing on variables are aliased as "supa" (Woolworths) and "supb" (Coles)
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
ax.tick_params(axis='y', left=False, pad=10, labelsize="x-large", labelcolor="#606060")
for i in ax.containers:
    ax.bar_label(i, fmt="%.1f", padding=15, size="x-large", color="#606060")

st.pyplot(fig)

st.caption(f"*(as of {datetime.fromtimestamp(getmtime('out/supa_out.csv')).strftime('%d %b %Y')})*")

# %%
