# %% [markdown]
"""
## Percentile Binned Preference Rate Plot Across Multiple Features

This notebook visualizes preference rates (proportion chosen) across multiple specified difference features, each binned into percentile categories.
"""
# %%
# Imports
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# %% User-specified parameters
DATA_PATH = 'data/preprocessed/prolific_pairwise.csv'  # Specify the dataset path

# Attractive
# Dominant
# Happy
# Sad
# Threatening
# Trustworthy
DIFF_FEATURES = ['AttractiveDiff', 'DominantDiff', 'HappyDiff', 'SadDiff', 'ThreateningDiff', 'TrustworthyDiff']
BIN_COUNT = 3  # Number of bins (e.g., 4 for quartiles)

# %% Load dataset
data = pd.read_csv(DATA_PATH, low_memory=False)

# %%
# User-specified parameters

# %%
# Prepare the data
filtered_frames = []
for feature in DIFF_FEATURES:
    temp_df = data[data[feature] >= 0].copy()
    temp_df['DiffFeature'] = feature
    temp_df['PercentileBin'] = pd.qcut(
        temp_df[feature],
        q=BIN_COUNT,
        labels=[f'{int(100*(i+1)/BIN_COUNT)}%' for i in range(BIN_COUNT)],
        duplicates='drop'
    )
    filtered_frames.append(temp_df)

# Concatenate dataframes for plotting
plot_data = pd.concat(filtered_frames, ignore_index=True)

# %%
# Set seaborn theme
sns.set_theme(
    style="ticks",
    font_scale=1.2,
    rc={
        "axes.linewidth": 1,
        "axes.edgecolor": "black",
        # "axes.grid": True,
        "grid.linestyle": "--",
        "grid.alpha": 0.6
    }
)
sns.set_palette("colorblind")

# %%
# Plot using FacetGrid
g = sns.catplot(
    data=plot_data,
    x='PercentileBin',
    y='chosen',
    col='DiffFeature',
    # hue='condition',  # Optional: if you want to differentiate by condition
    kind='point',
    dodge=True,
    errorbar=('ci', 95),
    markers='o',
    col_wrap=3,  # Adjust based on the number of features
    height=5,
    aspect=1
)

g.set_axis_labels("Percentile Bin", "Preference Rate")
g.set_titles("{col_name}")
g.set(ylim=(0.3, 0.7))  # Optional: Consistent y-axis limits
g.fig.tight_layout()
plt.show()
# %%
