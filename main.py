#%%
import lib
import pandas as pd

import streamlit as st
import altair as alt
from os.path import getmtime
from datetime import datetime

import time

# Supermarket name appearing on variables are aliased as "supa" (Woolworths) and "supb" (Coles)
@st.cache_data
def load_data():
    df_a = pd.read_csv(lib.supa_out_path, header=0)
    df_b = pd.read_csv(lib.supb_out_path, header=0)
    df_concat = pd.concat([df_a, df_b])
    return df_concat.groupby(df_concat.columns[:-1].tolist()).mean().reset_index()

# Plot based on macronutrient selection
@st.cache_data
def select_plot_alt(df, category):
    sub_df = df[df["Category"] == category]
    # Soon: better palette, sizing
    base = alt.Chart(sub_df).encode(
        x=alt.X("Amount:Q") \
            .axis(None),
        y=alt.Y("Food:N") \
            .sort("-x") \
            .axis(grid=False, domain=False, ticks=False, title="", \
                  offset=10, labelFontSize=16, labelColor="#444"),
        tooltip=alt.value(None)
    )

    bar = base.mark_bar().encode(
        color=alt.Color("Amount:Q") \
            .scale(scheme="pastel1") \
            .legend(None)
    )
    #food_text = base.mark_text(align="left", dx=-100, size=14).encode(
    #    text=alt.Text("Food:N")
    #)
    text = base.mark_text(align="left", dx=5, size=14).encode(
        text=alt.Text("Amount:Q").format(".2f"),
        color=alt.ColorValue("#444")
    )

    res = (bar + text).properties(width="container", height=alt.Step(40)).configure_view(stroke="transparent")
    return res

def main():
    # Inline CSS it since Streamlit Deploy makes style.css much more complicated
    css_str = '[class^="st-emotion"]  { font-weight: 500; }'
    st.markdown( f'<style>{css_str}</style>' , unsafe_allow_html= True)

    st.title("Fitness Food on a Budget")

    df = load_data()
    curr_cat = st.selectbox("Macronutrient (in gram/AUD)",
                            ("protein", "carb", "fat", "fruit", "vegetable"),
                            index=0, placeholder="Select")
    alt_obj = select_plot_alt(df, curr_cat)

    st.altair_chart(alt_obj, use_container_width=True, theme=None)

    supa_last_update = datetime.fromtimestamp(getmtime(lib.supa_out_path))
    supb_last_update = datetime.fromtimestamp(getmtime(lib.supb_out_path))
    st.caption(f"*(as of {supa_last_update.strftime('%d %b %Y')} for Woolworths, {supb_last_update.strftime('%d %b %Y')} for Coles)*")

# Time check
if __name__ == "__main__":
    start_time = time.time()
    main()
    print("Time: %s seconds " % (time.time() - start_time))
# %%
