
import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("woolies_out.csv", header=0)
df["Amount/$"] = df["Amount/$"].apply(lambda x: float(x.replace(" gram", "")))

st.text("Fitness Food Price Dashboard")

curr_cat = st.selectbox(
   "Macronutrient (in gram/$)",
    ("protein", "carb", "fat"),
   index=0,
   placeholder="Select"
)
fig = plt.figure(figsize=(10, 4))
sns.barplot(x='Amount/$', y='Food', data=df[df["Category"] == curr_cat].sort_values(by="Amount/$",ascending=False)) \
    .set(xlabel="", ylabel="")
st.pyplot(fig)
