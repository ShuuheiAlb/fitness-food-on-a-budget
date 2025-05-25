#%%
import lib
import pandas as pd

# Load dataset (try main, fallback to backup)
df = pd.read_csv(lib.supa_out_path, header=0)

# Compute summary stats per category and food
summary = (
    df.groupby(['Category', 'Food'])['Amount']
    .agg(
        Median='median',
        Q1=lambda x: x.quantile(0.25),
        Q3=lambda x: x.quantile(0.75),
        N='count'
    )
    .reset_index()
)

# Save as JSON for D3
summary.to_json("vis/supa_out.json", orient="records")

# %%
