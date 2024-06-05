#%%
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import FancyBboxPatch
from os.path import getmtime
from datetime import datetime

# Supermarket name appearing on variables are aliased as "supa" (Woolworths) and "supb" (Coles)
@st.cache_data
def load_data():
    df_a = pd.read_csv("out/supa_out.csv", header=0)
    df_b = pd.read_csv("out/supb_out.csv", header=0)
    df_concat = pd.concat([df_a, df_b])
    return df_concat.groupby(df_concat.columns[:-1].tolist()).mean().reset_index()

# Plot based on macronutrient selection
@st.cache_data()
def select_plot(df, category):
    fig, ax = plt.subplots(figsize=(12, 6))
    sub_df = df[df["Category"] == category]
    sns.barplot(x='Amount', y='Food', hue='Food', legend=False,
                data=sub_df.sort_values(by="Amount", ascending=False),
                palette=sns.color_palette(palette="pastel", n_colors=len(sub_df)))

    # Styling
    sns.set_style("white")
    sns.despine(left=True, bottom=True)

    # Ticks/labels
    ax.set(xlabel="", ylabel="")
    ax.tick_params(axis='x', bottom=False, labelbottom=False)
    ax.tick_params(axis='y', left=False, pad=10, labelsize="x-large", labelcolor="#606060")
    for i in ax.containers:
        ax.bar_label(i, fmt="%.1f", padding=15, size="x-large", color="#606060")

    # Make rounded bars
    new_patches = []
    for patch in reversed(ax.patches):
        bb = patch.get_bbox()
        color = patch.get_facecolor()
        p_bbox = FancyBboxPatch((bb.xmin, bb.ymin), abs(bb.width), abs(bb.height),
                                boxstyle="round, pad=0.01, rounding_size=0.2", mutation_aspect=0.7,
                                ec="none", fc=color)
        patch.remove()
        new_patches.append(p_bbox)
    for patch in new_patches:
        ax.add_patch(patch)

    return {"fig": fig, "ax": ax}

# ===

# Inline CSS it since Streamlit Deploy makes style.css much more complicated
css_str = '[class^="st-emotion"]  { font-weight: 500; }'
st.markdown( f'<style>{css_str}</style>' , unsafe_allow_html= True)

st.title("Fitness Food on a Budget")

df = load_data()
curr_cat = st.selectbox("Macronutrient (in gram/AUD)",
                        ("protein", "carb", "fat", "fruit", "vegetable"),
                        index=0, placeholder="Select")
plt_obj = select_plot(df, curr_cat)

st.pyplot(plt_obj["fig"])

# Should do the supb soon too
last_update_time = datetime.fromtimestamp(getmtime("out/supa_out.csv"))
st.caption(f"*(as of {last_update_time.strftime('%d %b %Y')})*")

# %%
