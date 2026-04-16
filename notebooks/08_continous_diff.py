# %% [markdown]
"""
# Percentile Binned Preference Rate Plot by Condition

This notebook visualizes how the preference rate (proportion chosen) varies with a specified difference feature (e.g., TrustworthyDiff, AttractiveDiff) across percentile bins and experimental conditions.
"""

# %%
# Imports
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# %% User-specified parameters
DATA_PATH = 'data/preprocessed/prolific_pairwise.csv'  # Specify the dataset path
DIFF_FEATURE = 'warmDiff'        # Specify the difference feature of interest
BIN_COUNT = 3                   # Number of bins for percentiles (e.g., 5 for 20% increments)

# %% Load dataset
data = pd.read_csv(DATA_PATH, low_memory=False)

# %% Filter dataset to non-negative values of the specified difference feature
filtered_data = data[data[DIFF_FEATURE] >= 0].copy()

# %% Compute percentile bins
filtered_data[f'{DIFF_FEATURE}_Percentile'] = pd.qcut(
    filtered_data[DIFF_FEATURE],
    q=BIN_COUNT,
    labels=[f'{int(100*(i+1)/BIN_COUNT)}%' for i in range(BIN_COUNT)],
    duplicates='drop'
)

# %% Plot preference rate by percentile bins and conditions with updated CI syntax

sns.set_theme(
    style="ticks", 
    font_scale=1.5, 
    rc={
    "axes.linewidth": 1,
    "axes.edgecolor": "black",
    "axes.grid": False,          # Enable gridlines
    # "grid.linestyle": "--",     # Gridline style (dashed)
    # "grid.alpha": 0.6           # Gridline transparency
    }
)
sns.set_palette("colorblind")

plt.figure(figsize=(10, 6))
sns.pointplot(
    data=filtered_data,
    x=f'{DIFF_FEATURE}_Percentile',
    y='chosen',
    hue='condition',
    dodge=True,
    errorbar=('ci', 95),  # updated confidence interval syntax
    markers='o'
)

plt.title(f'Preference Rate by {DIFF_FEATURE} Percentile')
plt.xlabel(f'{DIFF_FEATURE} Percentile Bin')
plt.ylabel('Preference Rate')
plt.tight_layout()
plt.show()

# %%
