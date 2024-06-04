#%%
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from os.path import getmtime
from datetime import datetime

# Importing data
# Supermarket name appearing on variables are aliased as "supa" (Woolworths) and "supb" (Coles)
@st.cache_resource
def load_data(path):
    return pd.read_csv(path, header=0)

@st.cache_data
def merged_average(df1, df2):
    df_concat = pd.concat([df1, df2])
    return df_concat.groupby(df_concat.columns[:-1].tolist()).mean().reset_index()

@st.cache_data
def select_category(df, category):
    return df[df["Category"] == category]

supa = load_data("out/supa_out.csv")
supb = load_data("out/supb_out.csv")
df = merged_average(supa, supb)

# CSS: manually put it since Streamlit Deployment makes "the other way" much more complicated
# Otherwise for offline use, style.css can be used
css_str = '[class^="st-emotion"]  { font-weight: 500; }'
st.markdown( f'<style>{css_str}</style>' , unsafe_allow_html= True)

# Title
st.title("Fitness Food on a Budget")

# Current variables
curr_cat = st.selectbox(
   "Macronutrient (in gram/$)",
   ("protein", "carb", "fat", "fruit", "vegetable"),
   index=0,
   placeholder="Select"
)
curr_data = select_category(df, curr_cat)

# Main plot, styling, ticks/labels
fig = plt.figure(figsize=(12, 6))
ax = sns.barplot(x='Amount', y='Food', hue='Food', data=curr_data.sort_values(by="Amount", ascending=False),
               palette=sns.color_palette(palette="pastel", n_colors=len(curr_data)), legend=False)

sns.set_style("white")
sns.despine(left=True, bottom=True)

# Make rounded bars
new_patches = []
for patch in reversed(ax.patches):
    bb = patch.get_bbox()
    color = patch.get_facecolor()
    p_bbox = FancyBboxPatch(
        (bb.xmin, bb.ymin), abs(bb.width), abs(bb.height),
        boxstyle="round, pad=-0.005, rounding_size=0.015", mutation_aspect=0.2,
        ec="none", fc=color,
    )
    patch.remove()
    new_patches.append(p_bbox)
for patch in new_patches:
    ax.add_patch(patch)

ax.set(xlabel="", ylabel="")
ax.tick_params(axis='x', bottom=False, labelbottom=False)
ax.tick_params(axis='y', left=False, pad=10, labelsize="x-large", labelcolor="#606060")
for i in ax.containers:
    ax.bar_label(i, fmt="%.1f", padding=15, size="x-large", color="#606060")

st.pyplot(fig)

# Last update time: should do the supb soon too
st.caption(f"*(as of {datetime.fromtimestamp(getmtime('out/supa_out.csv')).strftime('%d %b %Y')})*")

# %%
