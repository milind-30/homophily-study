# %% [markdown]
"""
# pointplot_simdiff_rt.py

## Purpose
Plot mean **reaction time** (log-transformed, trimmed) as a function of
`simDiff` (self-similarity gap).

## Data
We load `data/preprocessed/prolific_pairwise.csv`, keep trials with:
- 150 ms ≤ rt ≤ 10 s
- simDiff > 0
Columns:
- `rt`  (raw reaction time in milliseconds)
- `simDiff`  (integer 1–3)

## Outputs
- `figures/pointplot_rt_vs_simDiff.png`
- `tables/table_rt_vs_simDiff.md`
"""

# %%
import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from notebooks.helpers import bootstrap_ci

# %%
DATA_PATH = "data/preprocessed/prolific_pairwise.csv"
df = pd.read_csv(DATA_PATH)
# Convert RT from milliseconds to seconds
# df["rt"] = df["rt"] / 1000.0

# --- 1.  Trim and prepare RTs ----------------------------------------------
 # Keep rows with valid simDiff and RT, then drop NaNs
df = df[(df["simDiff"] > 0) &                      # only gaps > 0
        (df["rt"].between(150, 10000))            # 150 ms – 10 000 ms window
       ].copy()

df = df[df["rt"].notna()]                         # drop missing RTs
if df.empty:
    raise ValueError("No trials left after RT trimming!")

df["log_rt"] = np.log(df["rt"])                   # natural‑log transform

print(f"Usable rows: {len(df)}")

# %%  2.  Plot mean log-RT vs simDiff ----------------------------------------
os.makedirs("figures", exist_ok=True)

sns.set_theme(style="ticks", font_scale=1.5,
              rc={"axes.linewidth": 1, "axes.edgecolor": "black"})
sns.set_palette("colorblind")

plt.figure(figsize=(7, 5))
sns.pointplot(
    data=df,
    x="simDiff",
    y="log_rt",
    errorbar=("ci", 95),
    capsize=0.2
)

plt.xlabel("Self-Similarity Gap")
plt.ylabel("log(RT)")

sns.despine()

fig_path = os.path.join("figures", "pointplot_rt_vs_simDiff.png")
plt.savefig(fig_path, dpi=600, bbox_inches="tight")
print(f"Plot saved → {fig_path}")
plt.show()

 # %% [markdown]
"""
### Raw RT version for comparison

Below we plot the same point‑plot using **raw reaction times (ms)** so you can
directly inspect the difference between the log‑transformed and untransformed
scales.
"""

# %%
plt.figure(figsize=(7, 5))
sns.pointplot(
    data=df,
    x="simDiff",
    y="rt",                # raw RT in ms
    errorbar=("ci", 95),
    capsize=0.2
)
plt.xlabel("Self-Similarity Gap")
plt.ylabel("RT (ms)")
sns.despine()

raw_fig_path = os.path.join("figures", "pointplot_rt_vs_simDiff_raw.png")
plt.savefig(raw_fig_path, dpi=600, bbox_inches="tight")
print(f"Raw‑RT plot saved → {raw_fig_path}")
plt.show()

# %%  3.  Markdown table of mean RT (seconds) --------------------------------
os.makedirs("tables", exist_ok=True)

rows = []
for simdiff, grp in df.groupby("simDiff"):
    mean_sec, lo, hi = bootstrap_ci(grp["rt"], n_boot=5000, ci=95)
    rows.append(
        dict(simDiff=simdiff, mean=mean_sec, ci_lower=lo, ci_upper=hi)
    )

tbl = pd.DataFrame(rows).sort_values("simDiff")

table_path = os.path.join("tables", "table_rt_vs_simDiff.md")
with open(table_path, "w", encoding="utf-8") as f:
    f.write("| Self-Similarity Gap | Mean RT (ms) | 95 % CI (Lower) | 95 % CI (Upper) |\n")
    f.write("|:-------------------:|:-----------:|---------------:|---------------:|\n")
    for _, r in tbl.iterrows():
        f.write(
            f"| {int(r['simDiff'])} | {r['mean']:.3f} | {r['ci_lower']:.3f} | {r['ci_upper']:.3f} |\n"
        )
    f.write("\n")
    f.write(": Mean reaction time (milliseconds) as a function of self-similarity gap. {#tbl-rt-simdiff}\n")

print(f"Table saved → {table_path}")