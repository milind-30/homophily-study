# %% [markdown]
"""
# cochran_armitage.py

## Purpose
1. Compute a manual **Cochran–Armitage test** for a linear trend across `simDiff` (0..3).
2. Save **paper-friendly** contingency tables to `tables/` (as before).
3. Save **all test results** (Overall, by Task, by Condition) in a single Markdown file,
   `cochran_armitage_results.md`, also in `tables/`.

## Data
- `prolific_pairwise.csv` is loaded from `data/preprocessed/`.
- We keep only rows where `simDiff >= 0`.
- `chosen` is 0/1 indicating whether the focal character was selected.

## Output
- **Markdown contingency tables** in `tables/`, with human-readable labels.
- **Single** Markdown file, `cochran_armitage_results.md`, containing:
  - A brief description of the analysis.
  - A formal results statement (Z-stat, p-value) for each subset (Overall, Task, Condition).
"""

# %%
from scipy.stats import norm
import pandas as pd
import os
from math import sqrt
import numpy as np

# %% [markdown]
"""
## 1. Manual Cochran–Armitage Linear Trend Test
"""
# %%
def cochran_armitage_linear(count_1, nobs, scores=None, alternative="two-sided"):
    """
    Manual Cochran–Armitage linear trend test.

    Parameters
    ----------
    count_1 : array-like
        Number of successes (chosen=1) in each category i.
    nobs : array-like
        Total observations in each category i.
    scores : array-like or None
        Ordinal scores for each category i. If None, use [0, 1, 2, ..., k-1].
    alternative : str
        "two-sided", "less", or "greater".

    Returns
    -------
    z_stat : float
        Z statistic under the normal approximation.
    p_val : float
        Corresponding p-value.
    """

    count_1 = np.asarray(count_1, dtype=float)
    nobs = np.asarray(nobs, dtype=float)
    if scores is None:
        scores = np.arange(len(count_1), dtype=float)
    else:
        scores = np.asarray(scores, dtype=float)

    # Overall proportion
    total_success = count_1.sum()
    total_obs = nobs.sum()
    p = total_success / total_obs if total_obs > 0 else np.nan

    # Numerator
    numerator = np.sum(scores * (count_1 - nobs * p))

    # Denominator
    sum_w2 = np.sum(nobs * scores**2)
    denominator = sqrt(p * (1 - p) * sum_w2) if not np.isnan(p) else np.nan

    if denominator == 0 or np.isnan(denominator):
        return np.nan, np.nan

    z_stat = numerator / denominator

    # p-value
    
    if alternative == "two-sided":
        p_val = 2 * (1 - norm.cdf(abs(z_stat)))
    elif alternative == "greater":
        p_val = 1 - norm.cdf(z_stat)
    else:  # "less"
        p_val = norm.cdf(z_stat)

    return z_stat, p_val

# %% [markdown]
"""
## 2. Load Data
"""
# %%
DATA_PATH = "data/preprocessed/prolific_pairwise.csv"
df = pd.read_csv(DATA_PATH)
print(f"Loaded {len(df)} rows from {DATA_PATH}")

# Keep only simDiff≥0
df = df[df["simDiff"] >= 0].copy()
df["simDiff"] = df["simDiff"].astype(int)
df["chosen"] = df["chosen"].astype(int)
print(f"After filtering simDiff>=0, {len(df)} rows remain.")

# Rename if needed
df = df.rename(columns={"task_type": "Task", "condition": "Condition"})
df["Task"] = df["Task"].replace({
    "choice": "Pairwise Choice",
    "full_ranking": "Full Ranking"
})
df.head()

# %% [markdown]
"""
## 3. Save Paper-Style Contingency Tables
As before, we create a function to produce a more readable table
(e.g., "Similarity Difference", "Chose Focal", etc.).
"""
# %%
def save_contingency_markdown_paperstyle(table: pd.DataFrame, caption: str, label: str, filename: str):
    os.makedirs("tables", exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        f.write("| Similarity Difference | Did Not Choose Focal | Chose Focal |\n")
        f.write("|:-----------------------:|:---------------------:|------------:|\n")

        for idx in table.index:
            chosen0 = table.loc[idx, 0] if 0 in table.columns else 0
            chosen1 = table.loc[idx, 1] if 1 in table.columns else 0
            f.write(f"| {idx} | {chosen0} | {chosen1} |\n")

        f.write("\n")
        f.write(f": {caption} {{#{label}}}\n")

# %% [markdown]
"""
## 4. Prepare a Markdown Results File
We'll store **all** test results in `cochran_armitage_results.md`.
We'll start by writing a header/description, then append each result.
"""
# %%
results_file = os.path.join("tables", "cochran_armitage_results.md")
os.makedirs("tables", exist_ok=True)

with open(results_file, "w", encoding="utf-8") as f:
    f.write("# Cochran–Armitage Test Results\n\n")
    f.write("Below are the results of the Cochran–Armitage test for a linear trend.\n")
    f.write("We examine whether the probability of choosing the focal (more-similar) player\n")
    f.write("systematically increases across `simDiff = 0,1,2,3`.\n\n")

print(f"Initialized results file: {results_file}")

# %% [markdown]
"""
## 5. Run Overall Test and Save Table
"""
# %%
overall_table = pd.crosstab(df["simDiff"], df["chosen"])

# Save table (paper-friendly)
overall_md_path = os.path.join("tables", "cochran_armitage_overall.md")
save_contingency_markdown_paperstyle(
    table=overall_table,
    caption="Contingency of preference vs. surplus features (Overall).",
    label="tbl-cochran-overall",
    filename=overall_md_path
)

# Convert table to arrays
ordered_diff = sorted(overall_table.index.unique())
count_1 = overall_table.loc[ordered_diff, 1] if 1 in overall_table.columns else [0]*len(ordered_diff)
count_0 = overall_table.loc[ordered_diff, 0] if 0 in overall_table.columns else [0]*len(ordered_diff)
nobs = count_0 + count_1
z_stat, p_val = cochran_armitage_linear(count_1, nobs, scores=ordered_diff)

# Append the results to the single results file
with open(results_file, "a", encoding="utf-8") as f:
    f.write("## Overall Analysis\n\n")
    f.write(f"**Z-statistic**: {z_stat:.3f}\n\n")
    f.write(f"**p-value**: {p_val:.6g}\n\n")
    f.write("Interpretation: If `p < 0.05`, we conclude that there's a significant linear trend\n")
    f.write("across similarity difference in the probability of choosing the focal character.\n\n")

# %% [markdown]
"""
## 6. Analysis by Task
Repeat the above approach, appending each result to `cochran_armitage_results.md`.
"""
# %%
# tasks = df["Task"].dropna().unique()

# for task_level in tasks:
#     df_sub = df[df["Task"] == task_level]
#     sub_table = pd.crosstab(df_sub["simDiff"], df_sub["chosen"])

#     # Save table
#     task_table_md = os.path.join("tables", f"cochran_armitage_task_{task_level.replace(' ','_')}.md")
#     save_contingency_markdown_paperstyle(
#         table=sub_table,
#         caption=f"Contingency of preference vs. surplus features for Task='{task_level}'",
#         label=f"tbl-cochran-task-{task_level.replace(' ','-')}",
#         filename=task_table_md
#     )

#     ordered_diff = sorted(sub_table.index.unique())
#     count_1 = sub_table.loc[ordered_diff, 1] if 1 in sub_table.columns else [0]*len(ordered_diff)
#     count_0 = sub_table.loc[ordered_diff, 0] if 0 in sub_table.columns else [0]*len(ordered_diff)
#     nobs = count_0 + count_1
#     z_stat, p_val = cochran_armitage_linear(count_1, nobs, scores=ordered_diff)

#     with open(results_file, "a", encoding="utf-8") as f:
#         f.write(f"## Task = {task_level}\n\n")
#         f.write(f"**Z-statistic**: {z_stat:.3f}\n\n")
#         f.write(f"**p-value**: {p_val:.6g}\n\n")
#         f.write("(See table above for exact counts. If `p < 0.05`, there's a significant linear trend.)\n\n")

# %% [markdown]
"""
## 7. Analysis by Condition
Same approach for each Condition. 
"""
# %%
conditions = df["Condition"].dropna().unique()

for cond_level in conditions:
    df_sub = df[df["Condition"] == cond_level]
    sub_table = pd.crosstab(df_sub["simDiff"], df_sub["chosen"])

    # Save table
    cond_table_md = os.path.join("tables", f"cochran_armitage_cond_{cond_level}.md")
    save_contingency_markdown_paperstyle(
        table=sub_table,
        caption=f"Contingency of preference vs. surplus features for Condition='{cond_level}'",
        label=f"tbl-cochran-cond-{cond_level.lower()}",
        filename=cond_table_md
    )

    ordered_diff = sorted(sub_table.index.unique())
    count_1 = sub_table.loc[ordered_diff, 1] if 1 in sub_table.columns else [0]*len(ordered_diff)
    count_0 = sub_table.loc[ordered_diff, 0] if 0 in sub_table.columns else [0]*len(ordered_diff)
    nobs = count_0 + count_1
    z_stat, p_val = cochran_armitage_linear(count_1, nobs, scores=ordered_diff)

    with open(results_file, "a", encoding="utf-8") as f:
        f.write(f"## Condition = {cond_level}\n\n")
        f.write(f"**Z-statistic**: {z_stat:.3f}\n\n")
        f.write(f"**p-value**: {p_val:.6g}\n\n")
        f.write("(Refer to the corresponding contingency table in `tables/` for details.)\n\n")

# %% [markdown]
"""
**Done!**  

All results are written to `cochran_armitage_results.md` in the `tables/` directory, 
with a single consolidated text describing:
- Overall analysis
- By-Task analysis
- By-Condition analysis

Each block includes a short formal results statement (Z-stat, p-value).
"""

# %%
