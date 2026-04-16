# %% [markdown]
"""
# heatmap_preferences.py

## Purpose
Visualize the probability that the "focal" player is preferred
across different levels of shared features for both the focal and the other player.

## Data
We load `data/preprocessed/prolific_pairwise.csv`, filter as needed,
then compute the mean preference rate for the focal player by `(simOpp, simChar)`.

## Output
A single PNG in `figures/`:
- `heatmap_preferences.png` showing the probability of preferring the focal player 
  for each combination of overlap with the participant (focal vs. other).
"""

# %%
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# %% [markdown]
"""
## 1. Load Data
"""
# %%
DATA_PATH = "data/preprocessed/prolific_pairwise.csv"
df = pd.read_csv(DATA_PATH)
df = df[df["simDiff"] >= 0].copy()
print(f"Loaded {len(df)} rows from {DATA_PATH}")

# %% [markdown]
"""
## 2. Compute Mean Preference Rate by (simOpp, simChar)
"""
# %%
grouped_prob = df.groupby(["simOpp", "simChar"])["chosen"].mean().unstack()
grouped_prob.head()

# %% [markdown]
"""
## 3. Plot Heatmap
"""
# %%
os.makedirs("figures", exist_ok=True)

sns.set_theme(
    style="ticks",
    font_scale=1.5,
    rc={"axes.linewidth": 1, "axes.edgecolor": "black"}
)

plt.figure(figsize=(7, 6))

ax = sns.heatmap(
    grouped_prob,
    annot=True,
    fmt=".2f",       
    cmap="vlag",
    center=0.5,
    vmin=0, vmax=1,
    cbar=False
)

# ax.set_title("Preference Rate by Number Features Shared with Participant")
ax.set_ylabel("Other Character Similarity")
ax.set_xlabel("Focal Character Similarity")

# Clean up the spines
sns.despine()

# Save figure
fig_path = os.path.join("figures", "heatmap_preferences.png")
plt.savefig(fig_path, dpi=600, bbox_inches="tight")
print(f"Heatmap saved to {fig_path}")

plt.show()

# %%

# Save data table with caption
os.makedirs("tables", exist_ok=True)
table_filename = os.path.join("tables", "table_chosen_vs_simCharSimOpp.md")

with open(table_filename, "w", encoding="utf-8") as f:
    # Write the header row with dynamic column labels
    col_labels = grouped_prob.columns.tolist()
    f.write("| Other \\ Focal | " + " | ".join(f"{col}" for col in col_labels) + " |\n")
    f.write("|:-------------:|" + "|".join([":--:"] * len(col_labels)) + "|\n")

    # Write each row of the table
    for idx, row in grouped_prob.iterrows():
        row_str = " | ".join(f"{val:.3f}" if pd.notnull(val) else "" for val in row)
        f.write(f"| {idx} | {row_str} |\n")

    # Add caption
    f.write("\n")
    f.write(": Probability of preferring the focal player by similarity of focal and other player to participant. {#tbl-heatmap}\n")

with open(table_filename, "r", encoding="utf-8") as f:
    table = f.read()

print(table)

# %%
