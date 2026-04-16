#%% [markdown]
"""
# Synthetic Dataset
"""

# %%
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# %% [markdown]
"""
## 1. Load Data
"""

# %%
# DATA_PATH = "data/preprocessed/synthetic_dataset.csv"
DATA_PATH = "data/preprocessed/prolific_pairwise.csv"
df = pd.read_csv(DATA_PATH)
# df = df[df["simDiff"] > 0].copy() # Exclude simDiff<=0 for clarity
print(f"Loaded {len(df)} rows from {DATA_PATH}")

# Ensure 'chosen' column is numeric
df['chosen'] = df['chosen'].astype(int)

# Set Seaborn theme and color palette
sns.set_theme(
    style="ticks", 
    font_scale=1.5, 
    rc={"axes.linewidth": 1, "axes.edgecolor": "black"}
)
sns.set_palette("colorblind")

# Display a snippet for confirmation
df.head()

# %% [markdown]
"""
## 2. Plot Probability of Choosing charA vs. Race
"""

# %%

# create version of df that excludes obs where raceChar and raceOpp match
race_df = df[df['raceChar'] != df['raceOpp']].copy()

# Aggregate within participants first, then across participants
subject_means = race_df.groupby(['subject', 'raceChar'])['chosen'].mean().reset_index()
facet_subject_means = race_df.groupby(['subject', 'raceChar', 'condition'])['chosen'].mean().reset_index()

race_ordering = ["east-asian", "black", "latino", "south-asian", "white"]
condition_order = ["Competitive", "Casual"]

# Create bar plot with 95% confidence intervals over participants
plt.figure(figsize=(10, 6))
sns.barplot(
    x='raceChar', y='chosen', data=subject_means, errorbar=("ci", 95),
    # we'll manually sort these for clarity across figure generations
    order=race_ordering
)

# Labels and title

plt.xlabel('Character Race')
plt.ylabel('Preference Rate')
plt.title('Effect of Character Race on Preference Rate (95% CI over Participants)')
plt.xticks(rotation=45)

# Show plot
plt.show()

plt.figure(figsize=(10, 6))
sns.barplot(
    x="raceChar", y="chosen", hue="condition", data=facet_subject_means,
    errorbar=("ci", 95), order=race_ordering, hue_order=condition_order
)
plt.xlabel("Character Race")
plt.ylabel("Preference Rate")
plt.title("Effect of Character Race on Preference Rate by Condition (95% CI over Participants)")
plt.xticks(rotation=45)

plt.legend(title="Condition", loc="center left", bbox_to_anchor=(1, 0.5))

plt.show()

# Create faceted bar plots
g = sns.catplot(
    data=facet_subject_means, x="raceChar", y="chosen", col="condition",
    kind="bar", errorbar=("ci", 95), height=6, aspect=1,
    order=race_ordering, col_order=condition_order
)

# Customize labels
g.set_axis_labels("Character Race", "Preference Rate")
g.set_titles("Condition: {col_name}")
g.set_xticklabels(rotation=45)

# Show plot
plt.show()

# %% [markdown]
"""
## 2. Plot Probability of Choosing charA vs. Gender
"""

# %%

# create version of df that excludes obs where genderChar and genderOpp match
gender_df = df[df['genderChar'] != df['genderOpp']].copy()

# Aggregate within participants first, then across participants
subject_means = gender_df.groupby(['subject', 'genderChar'])['chosen'].mean().reset_index()
facet_subject_means = gender_df.groupby(['subject', 'genderChar', 'condition'])['chosen'].mean().reset_index()

# Create bar plot with 95% confidence intervals over participants
plt.figure(figsize=(10, 6))
sns.barplot(
    x='genderChar', y='chosen', data=subject_means, errorbar=("ci", 95),
)

# Labels and title
plt.xlabel('Character Gender')
plt.ylabel('Preference Rate')

plt.title('Effect of Character Gender on Preference Rate (95% CI over Participants)')
plt.xticks(rotation=45)

# Show plot
plt.show()

plt.figure(figsize=(10, 6))
sns.barplot(
    x='genderChar', y='chosen', hue="condition", data=facet_subject_means, errorbar=("ci", 95),
)

# Labels and title
plt.xlabel('Character Gender')
plt.ylabel('Preference Rate')
plt.title('Effect of Character Gender on Preference Rate (95% CI over Participants)')

plt.legend(title="Condition", loc="center left", bbox_to_anchor=(1, 0.5))
plt.xticks(rotation=45)
plt.show()

# Create faceted bar plots
g = sns.catplot(
    data=facet_subject_means, x="genderChar", y="chosen", col="condition",
    kind="bar", errorbar=("ci", 95), height=6, aspect=1,col_order=["Competitive", "Casual"]
)

# Customize labels
g.set_axis_labels("Character Gender", "Preference Rate")
g.set_titles("Condition: {col_name}")
g.set_xticklabels(rotation=45)

# Show plot
plt.show()

# %%

# Define age bins
age_bins = [0, 24, 32, 39, float("inf")]
age_labels = ["18-24", "25-31", "32-38", "39+"]

# Create binned versions of both ageChar and ageOpp
df["charAge_group"] = pd.cut(df["ageChar"], bins=age_bins, labels=age_labels)
df["oppAge_group"] = pd.cut(df["ageOpp"], bins=age_bins, labels=age_labels)

# Exclude observations where charAge and oppAge fall in the same bin
age_df = df[df["charAge_group"] != df["oppAge_group"]].copy()

# Aggregate within participants first, then across participants
subject_means = age_df.groupby(['subject', 'charAge_group'], observed=False)['chosen'].mean().reset_index()
facet_subject_means = age_df.groupby(['subject', 'charAge_group', 'condition'])['chosen'].mean().reset_index()

# Create bar plot with 95% confidence intervals over participants
plt.figure(figsize=(10, 6))
sns.barplot(
    x='charAge_group', y='chosen', data=subject_means, errorbar=("ci", 95)
)



# Labels and title
plt.xlabel('Character Age Group')
plt.ylabel('Preference Rate')
plt.title('Effect of Character Age on Preference Rate (95% CI over Participants)')
plt.xticks(rotation=45)

# Show plot
plt.show()

# Create bar plot with 95% confidence intervals over participants
plt.figure(figsize=(10, 6))
sns.barplot(
    x='charAge_group', y='chosen', hue='condition', data=facet_subject_means, errorbar=("ci", 95), 
)

# Labels and title
plt.xlabel('Character Age Group')
plt.ylabel('Preference Rate')
plt.title('Effect of Character Age on Preference Rate (95% CI over Participants)')
plt.xticks(rotation=45)
plt.legend(title="Condition", loc="center left", bbox_to_anchor=(1, 0.5))


# Show plot
plt.show()

# Create faceted bar plots
g = sns.catplot(
    data=facet_subject_means, x="charAge_group", y="chosen", col="condition",
    kind="bar", errorbar=("ci", 95), height=6, aspect=1,col_order=["Competitive", "Casual"]
)

# Customize labels
g.set_axis_labels("Character Age", "Preference Rate")
g.set_titles("Condition: {col_name}")
g.set_xticklabels(rotation=45)

# Show plot
plt.show()

# %%
