
import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("woolies_out.csv", header=0)
fig, axs = plt.subplots(ncols=3)
sns.barplot(x='Food', y='Amount/$', data=df[df["Category"] == "protein"], ax=axs[0])
sns.barplot(x='Food', y='Amount/$', data=df[df["Category"] == "carb"], ax=axs[0])
sns.barplot(x='Food', y='Amount/$', data=df[df["Category"] == "fat"], ax=axs[0])

st.text("Fitness Food Price Dashboard")
st.pyplot(fig)