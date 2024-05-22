
import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("woolies_out.csv", header=0)
df["Amount/$"] = df["Amount/$"].apply(lambda x: float(x.replace(" gram", "")))

st.title("Fitness Food on a Budget")

curr_cat = st.selectbox(
   "Macronutrient (in gram/$)",
    ("protein", "carb", "fat"),
   index=0,
   placeholder="Select"
)
curr_data = df[df["Category"] == curr_cat]
palette_codes = {"protein": "crest", "carb": "flare", "fat": ""}
curr_palette_code = palette_codes[curr_cat]

fig = plt.figure(figsize=(10, 4))
sns.barplot(x='Amount/$', y='Food', data=curr_data.sort_values(by="Amount/$", ascending=False),
            palette=sns.color_palette(palette="pastel", n_colors=len(curr_data))) \
    .set(xlabel="", ylabel="")
st.pyplot(fig)
