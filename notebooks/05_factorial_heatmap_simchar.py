# %% [markdown]
"""
# 03_factorial_heatmaps.py

## Purpose
Create parallel heatmaps showing the probability of preferring the focal character,
faceted by:
1. **Condition** (Casual vs. Competitive)
2. **Task** (Pairwise Choice vs. Full Ranking)
3. **Condition × Task** (2×2)

Each heatmap displays:
- Rows: "Shared Features with Compared Player" (simOpp)
- Columns: "Shared Features with Reference Player" (simChar)
- Cell value: Mean Preference Rate (`chosen`)

## Data
We load `data/preprocessed/prolific_pairwise.csv`, retain rows with `simDiff >= 0`,
and rename variables for clarity (e.g., `task_type`→`Task`, `condition`→`Condition`).

## Output
Three PNG figures in `figures/`:
- `heatmaps_by_condition.png` (2 facets)
- `heatmaps_by_task.png` (2 facets)
- `heatmaps_by_condition_and_task.png` (2×2 layout)
"""

# %%
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import os

# %% [markdown]
"""
## 1. Load and Filter Data
"""
# %%
DATA_PATH = "data/preprocessed/prolific_pairwise.csv"
df = pd.read_csv(DATA_PATH)
print(f"Loaded {len(df)} rows from {DATA_PATH}")

# Keep only rows with simDiff >= 0
df = df[df["simDiff"] >= 0].copy()
print(f"After filtering simDiff >= 0, {len(df)} rows remain.")

# Rename and map columns for clarity
df = df.rename(columns={"task_type": "Task", "condition": "Condition"})
df["Task"] = df["Task"].replace({
    "choice": "Pairwise Choice",
    "full_ranking": "Full Ranking"
})

df["Condition"] = df["Condition"].replace({
    "Casual": "Low-Stakes / Affiliative Frame",
    "Competitive": "High-Stakes / Performance Frame"
})

# Set Condition as categorical with specified order
df["Condition"] = pd.Categorical(
    df["Condition"],
    categories=[
        "Low-Stakes / Affiliative Frame",
        "High-Stakes / Performance Frame"
    ],
    ordered=True
)

df.head()

# %% [markdown]
"""
## 2. Set Up Style and Output Folder
"""
# %%
os.makedirs("figures", exist_ok=True)

sns.set_theme(
    style="ticks",
    font_scale=1.5,
    rc={"axes.linewidth": 1, "axes.edgecolor": "black"}
)

# %% [markdown]
"""
## 3. Helper Functions

### 3.1 `facet_heatmap`
- Pivots each subset of the data into a 2D grid (rows=`simOpp`, cols=`simChar`),
  computing the **mean** of `chosen`.
- Calls `sns.heatmap` on that pivoted data.

### 3.2 `make_scalar_mappable`
- Creates a matplotlib ScalarMappable for a fixed color scale (here, `vmin=0, vmax=1`)
  so we can add one colorbar per FacetGrid.
"""

# %%
def facet_heatmap(data, x_var, y_var, z_var, **kwargs):
    """
    data   : DataFrame subset for one facet
    x_var  : column name for pivot columns (simChar)
    y_var  : column name for pivot rows (simOpp)
    z_var  : column name to aggregate (chosen)
    kwargs : passed to sns.heatmap
    """
    pivoted = data.groupby([y_var, x_var])[z_var].mean().unstack(fill_value=None)
    ax = plt.gca()
    sns.heatmap(
        pivoted,
        ax=ax,
        **kwargs
    )
    ax.set_xlabel("Focal Character Similarity")
    ax.set_ylabel("Other Character Similarity")

def make_scalar_mappable(cmap="vlag", vmin=0, vmax=1):
    norm = mcolors.Normalize(vmin=vmin, vmax=vmax)
    sm = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
    sm.set_array([])  # no actual data needed
    return sm

# Common kwargs for all heatmaps:
heatmap_kwargs = {
    "cmap": "vlag",
    "center": 0.5,
    "vmin": 0.0,
    "vmax": 1.0,
    "annot": True,
    "fmt": ".2f",
    "cbar": False  # We add a single colorbar manually per FacetGrid
}

# %% [markdown]
"""
## 4. Heatmaps by Condition

Two facets: one for "Casual," one for "Competitive" (assuming those are the levels).
"""

# %%
g = sns.FacetGrid(
    df,
    col="Condition",
    sharex=True,
    sharey=True,
    height=5,
    aspect=1.2
)
g.map_dataframe(
    facet_heatmap,
    x_var="simChar",
    y_var="simOpp",
    z_var="chosen",
    **heatmap_kwargs
)


g.set_titles(col_template="{col_name}")
# g.set_axis_labels(
#     "Reference Character Similarity",
#     "Competitor Similarity"
# )
# g.fig.suptitle("Preference Rate by Condition & Number Features Shared with Participant")

# Adjust to prevent overlap
# g.fig.subplots_adjust(top=0.85, right=0.88)

fig_path = os.path.join("figures", "heatmaps_by_condition.png")
plt.savefig(fig_path, dpi=600, bbox_inches="tight")
plt.show()

# %% [markdown]
"""
## 5. Heatmaps by Task

Two facets: "Pairwise Choice" vs. "Full Ranking."
"""

# %%
# g = sns.FacetGrid(
#     df,
#     col="Task",
#     sharex=True,
#     sharey=True,
#     height=5,
#     aspect=1.2
# )
# g.map_dataframe(
#     facet_heatmap,
#     x_var="simChar",
#     y_var="simOpp",
#     z_var="chosen",
#     **heatmap_kwargs
# )


# g.set_titles(col_template="{col_name}")
# # g.set_axis_labels(
# #     "Reference Character Similarity",
# #     "Competitor Similarity"
# # )
# # g.fig.suptitle("Preference Rate by Task & Number Features Shared with Participant")
# g.fig.subplots_adjust(top=0.85, right=0.88)

# fig_path = os.path.join("figures", "heatmaps_by_task.png")
# plt.savefig(fig_path, dpi=600, bbox_inches="tight")
# plt.show()

# %% [markdown]
"""
## 6. Heatmaps by (Condition × Task)

A 2×2 layout: rows = Condition, cols = Task.

We ensure there's enough space for the colorbar so it won't crowd the right-hand 
figure labels.
"""

# %%
# Make sure Condition and Task have the order you want

# df["Condition"] = pd.Categorical(
#     df["Condition"],
#     categories=[
#         "Low-Stakes / Affiliative Frame",
#         "High-Stakes / Performance Frame"
#     ],
#     ordered=True
# )
# df["Task"] = pd.Categorical(
#     df["Task"],
#     categories=["Pairwise Choice", "Full Ranking"],
#     ordered=True
# )

# g = sns.FacetGrid(
#     df,
#     row="Condition",
#     col="Task",
#     sharex=True,
#     sharey=True,
#     height=4,
#     aspect=1.2,
#     margin_titles=True
# )
# g.map_dataframe(
#     facet_heatmap,
#     x_var="simChar",
#     y_var="simOpp",
#     z_var="chosen",
#     **heatmap_kwargs
# )


# g.set_titles(row_template="{row_name}", col_template="{col_name}")
# # g.set_axis_labels(
# #     "Reference Character Similarity",
# #     "Competitor Similarity"
# # )

# # This helps ensure the colorbar doesn't overlap text
# g.fig.subplots_adjust(top=0.88, right=0.88)

# # g.fig.suptitle("Preference by Number Features Shared with Participant (Condition × Task)")

# fig_path = os.path.join("figures", "heatmaps_by_condition_and_task.png")
# plt.savefig(fig_path, dpi=600, bbox_inches="tight")
# plt.show()

# %% [markdown]
"""
**Done!**

You now have three sets of heatmaps:
- **By Condition** (`heatmaps_by_condition.png`)
- **By Task** (`heatmaps_by_task.png`)
- **By Condition × Task** (`heatmaps_by_condition_and_task.png`)

All use the `vlag` palette from 0..1, centered at 0.5, with a single colorbar
per grid.
"""
