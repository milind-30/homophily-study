# %% [markdown]
"""
# pointplot_simdiff_rt_by_condition.py

Plot **log-transformed reaction time (RT)** against self-similarity gap (`simDiff`),
faceted by **Condition**.

## Data
`data/preprocessed/prolific_pairwise.csv`

* `rt` — reaction time in **milliseconds**
* `simDiff` — self-similarity gap (1 – 3)
* `condition` — "Casual"/"Competitive" (relabeled below)
* trials trimmed to 150 ms – 10 000 ms

## Output
* `figures/pointplot_logRT_vs_simDiff_byCondition.png`
* `tables/table_logRT_vs_simDiff_byCondition.md`
"""
# %%
import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from notebooks.helpers import bootstrap_ci

# %% 1 ── Load & prepare data ────────────────────────────────────────────────
DATA_PATH = "data/preprocessed/prolific_pairwise.csv"
df = pd.read_csv(DATA_PATH)

# Relabel columns
df = df.rename(columns={"condition": "Condition"})

# Descriptive Condition names
df["Condition"] = df["Condition"].replace({
    "Casual": "Low-Stakes / Affiliative Frame",
    "Competitive": "High-Stakes / Performance Frame"
})

# Keep valid trials
df = df[
    (df["rt"].between(150, 10_000)) &      # 150 ms – 10 s
    (df["simDiff"] > 0)                    # exclude ties
].copy()

# Log-transform RT (still in ms)
df["log_rt"] = np.log(df["rt"])

print(f"Usable trials: {len(df)}")

# Categorical order for faceting
df["Condition"] = pd.Categorical(
    df["Condition"],
    categories=[
        "Low-Stakes / Affiliative Frame",
        "High-Stakes / Performance Frame"
    ],
    ordered=True
)

# %% 2 ── Plot: FacetGrid by Condition ───────────────────────────────────────
os.makedirs("figures", exist_ok=True)
sns.set_theme(style="ticks", font_scale=1.5, rc={"axes.linewidth": 1})
sns.set_palette("colorblind")

g = sns.FacetGrid(
    data=df,
    col="Condition",
    sharey=True,
    height=5,
    aspect=1.2,
    margin_titles=True
)

def facet_pointplot(data, x, y, **kwargs):
    sns.pointplot(
        data=data,
        x=x,
        y=y,
        errorbar=("ci", 95),
        capsize=0.2,
        **kwargs
    )

g.map_dataframe(facet_pointplot, x="simDiff", y="log_rt")
g.set_axis_labels("Self-Similarity Gap", "log(RT)")
g.set_titles(col_template="{col_name}")
g.fig.subplots_adjust(top=0.9)

fig_path = "figures/pointplot_logRT_vs_simDiff_byCondition.png"
plt.savefig(fig_path, dpi=600, bbox_inches="tight")
print(f"Figure saved → {fig_path}")
plt.show()

# %%
# ---- Raw RT (ms) FacetGrid by Condition -----------------------------------
g_raw = sns.FacetGrid(
    data=df,
    col="Condition",
    sharey=True,
    height=5,
    aspect=1.2,
    margin_titles=True
)

g_raw.map_dataframe(
    sns.pointplot,
    x="simDiff",
    y="rt",
    errorbar=("ci", 95),
    capsize=0.2
)

g_raw.set_axis_labels("Self-Similarity Gap", "RT (ms)")
g_raw.set_titles(col_template="{col_name}")
g_raw.fig.subplots_adjust(top=0.9)

raw_fig_path = "figures/pointplot_RT_vs_simDiff_byCondition_raw.png"
plt.savefig(raw_fig_path, dpi=600, bbox_inches="tight")
print(f"Raw RT figure saved → {raw_fig_path}")
plt.show()

# %% 3 ── Markdown table of mean RT (ms) per gap & condition ────────────────
os.makedirs("tables", exist_ok=True)

rows = []
for (gap, cond), grp in df.groupby(["simDiff", "Condition"]):
    mean_ms, lo, hi = bootstrap_ci(grp["rt"], n_boot=5000, ci=95)
    rows.append(dict(
        simDiff=gap,
        Condition=cond,
        mean=mean_ms,
        ci_lower=lo,
        ci_upper=hi
    ))

tbl = pd.DataFrame(rows).sort_values(["simDiff", "Condition"])

table_path = "tables/table_logRT_vs_simDiff_byCondition.md"
with open(table_path, "w", encoding="utf-8") as f:
    f.write("| Self-Similarity Gap | Condition | Mean RT (ms) | 95 % CI (Lower) | 95 % CI (Upper) |\n")
    f.write("|:------------------:|:----------:|-------------:|---------------:|---------------:|\n")
    for _, r in tbl.iterrows():
        f.write(
            f"| {int(r['simDiff'])} | {r['Condition']} | "
            f"{r['mean']:.1f} | {r['ci_lower']:.1f} | {r['ci_upper']:.1f} |\n"
        )
    f.write("\n")
    f.write(": Mean reaction time (milliseconds) by self-similarity gap and Condition. {#tbl-rt-simDiff-cond}\n")

print(f"Table saved → {table_path}")
# %%
