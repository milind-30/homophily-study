# %% [markdown]
"""
convert_pairwise_two_row.py

PURPOSE
-------
1. Convert raw Prolific/JATOS JSON data into a pairwise-comparison CSV.
2. For each pairwise trial, **two** lines are appended:
   - (charA, charB) => chosen
   - (charB, charA) => !chosen
   allowing each “character” to appear as the 'focal' character.
3. We produce:
   a) An unswapped CSV (exactly as processed)
   b) An optional swapped CSV if you'd like simChar ≥ simOpp

NOTES
-----
- If you prefer only the unswapped version, comment out the swap logic cell.
- By default, `charA` vs. `charB` might be somewhat randomized if your code chooses to shuffle them.
- The script references a `notebooks.helpers` module for custom functions.
"""

# %%
#| code-summary: Imports
import json
import random
import numpy as np
import pandas as pd
import re

# If your helpers are in notebooks/helpers.py, adjust the import:
import notebooks.helpers as helpers

def retrieve_conditions(participants_data: list[list[dict]]) -> list[str]:
    """
    Retrieve the condition ("Casual" or "Competitive") assigned to each participant in the data.

    Args:
        participants_data: List of lists of dictionaries, where each inner list contains recorded entries for a participant and trial.

    Returns:
        conditions: Contains the condition of each participant.
    """
    conditions = []
    for participant_data in participants_data:
        condition = next(
            (
                ["Threatening", "Competent"][entry["condition"]]
                for entry in participant_data
                if entry.get("condition") is not None
            )
        )
        conditions.append(condition)
    return conditions

# %%
#| code-summary: Load raw data
jatos_data_path = "data/raw/attributejudgments.jsonl"
data1 = helpers.load_jsonl(jatos_data_path)
datasets = [data1]

print("Example snippet from dataset 0, participant 0, event 1:")
print(datasets[0][0][1])

# %%
#| code-summary: Image paths & metadata
with open("experiment/character_images.json", "r") as file:
    character_images = json.load(file)

image_paths = [path for paths in character_images.values() for path in paths]

character_codes = [image_path.split('/')[-1].split('_')[1] for image_path in image_paths]

# concatenate the two feature datasets
data_dirs = ["materials/cfd/features.csv", "materials/cfd/india_features.csv"]
character_features = pd.concat([pd.read_csv(data_dir) for data_dir in data_dirs])

# %%
#| code-summary: Pre-Allocation
merged = {
    "subject": [],
    "task_type": [],
    "task_ordering": [],
    "condition": [],
    "subject_race": [],
    "subject_age": [],
    "subject_gender": [],
    "character": [],
    "opponent": [],
    "simChar": [],
    "simOpp": [],
    "simDiff": [],
    "simDiffRace": [],
    "simDiffAge": [],
    "simDiffGender": [],
    "chosen": [],
    "raceChar": [],
    "ageChar": [],
    "genderChar": [],
    "raceOpp": [],
    "ageOpp": [],
    "genderOpp": [],
    "subject_college": [],
    "rt": [],
    "data_index": []
}

# for each column beyond the second, add <columnname>Char and <columnname>Opp to merged
feature_names = []
for column in character_features.columns[2:]:
    merged[f"{column}Char"] = []
    merged[f"{column}Opp"] = []
    merged[f"{column}Diff"] = []
    feature_names.append(column)

# %%
#| code-summary: Two-choice trials
task_type = "choice"

subject_id = 0
for data_index, data in enumerate(datasets):
    conditions = retrieve_conditions(data)
    task_orderings = helpers.retrieve_task_ordering(data)
    subject_demographics = helpers.retrieve_subj_demographics(data)

    for i, participant_data in enumerate(data):
        subject_id += 1
        condition = conditions[i]
        task_ordering = task_orderings[i]
        subject_race, subject_gender, subject_age, subject_college = subject_demographics[i]

        for entry in participant_data:
            if "choice" not in entry or entry["choice"] not in ["left", "right"]:
                continue

            # Identify compared characters & choice
            shuffling = random.choice([True, False])
            if shuffling:
                charA = entry["left_image"]
                charB = entry["right_image"]
                chosenA = entry["choice"] == "left"
            else:
                charA = entry["right_image"]
                charB = entry["left_image"]
                chosenA = entry["choice"] == "right"
            charA_id = image_paths.index(charA)
            charB_id = image_paths.index(charB)

            # match charA and charB to their respective demographics
            charA_code = character_codes[charA_id]
            charB_code = character_codes[charB_id]

            # charA_code identifies the row in the demographics table via "Model" column; 
            # need to do a contains check instead of an equality
            maskA = character_features["Model"].str.contains(charA_code) | character_features["Model"].str.contains(charA_code.replace("-", ""))
            maskB = character_features["Model"].str.contains(charB_code) | character_features["Model"].str.contains(charB_code.replace("-", ""))
            charA_rows = character_features.loc[maskA]
            charB_rows = character_features.loc[maskB]

            # Safety checks — you can decide how to handle 0 or >1 rows
            if len(charA_rows) != 1:
                print(f"Warning: Expected exactly 1 row for charA_code={charA_code}, got {len(charA_rows)}")
                continue
            if len(charB_rows) != 1:
                print(f"Warning: Expected exactly 1 row for charB_code={charB_code}, got {len(charB_rows)}")
                continue

            # Create local copies so we don't overwrite the original DataFrame
            charA_row = charA_rows.copy()
            charB_row = charB_rows.copy()

            # Now parse each feature as numeric
            for feature in feature_names:
                # Convert the single row cell to string
                rawA = str(charA_row.iloc[0][feature])
                rawB = str(charB_row.iloc[0][feature])

                # Use a regex to capture digits or decimal points
                matchA = re.search(r'([\d.]+)', rawA)
                matchB = re.search(r'([\d.]+)', rawB)

                if matchA:
                    valA = float(matchA.group(1))  # convert the matched digits to float
                else:
                    valA = np.nan  # or handle differently if no match

                if matchB:
                    valB = float(matchB.group(1))
                else:
                    valB = np.nan

                # If you rely on these always being valid, you can assert:
                # assert not np.isnan(valA), f"Could not parse a valid float from '{rawA}'"
                # assert not np.isnan(valB), f"Could not parse a valid float from '{rawB}'"

                # Store these numeric values back into our *local copy*:
                charA_row.at[charA_row.index[0], feature] = valA
                charB_row.at[charB_row.index[0], feature] = valB

            # Extract demographics of both
            charA_demographics = helpers.extract_race_gender_age(charA)
            charB_demographics = helpers.extract_race_gender_age(charB)
            raceA, genderA, ageA = charA_demographics
            raceB, genderB, ageB = charB_demographics

            # Similarities
            simRaceA = helpers.compare_race(subject_race, raceA)
            simAgeA = helpers.convert_age(subject_age) == helpers.convert_age(int(ageA))
            simGenderA = helpers.convert_gender(subject_gender) == helpers.convert_gender(genderA)
            simA = simRaceA + simAgeA + simGenderA

            simRaceB = helpers.compare_race(subject_race, raceB)
            simAgeB = (helpers.convert_age(subject_age) == helpers.convert_age(int(ageB)))
            simGenderB = (helpers.convert_gender(subject_gender) == helpers.convert_gender(genderB))
            simB = simRaceB + simAgeB + simGenderB

            # Row 1: (charA, charB)
            simDiffAB = simA - simB
            simDiffRaceAB = simRaceA - simRaceB
            simDiffAgeAB = simAgeA - simAgeB
            simDiffGenderAB = simGenderA - simGenderB

            # response time
            rt = int(entry["rt"])

            # -- First row: (charA, charB), chosen=(chosenA)
            merged["subject"].append(subject_id)
            merged["task_type"].append(task_type)
            merged["task_ordering"].append(task_ordering)
            merged["condition"].append(condition)
            merged["subject_race"].append(subject_race)
            merged["subject_age"].append(subject_age)
            merged["subject_gender"].append(subject_gender)
            merged["character"].append(charA_id)
            merged["opponent"].append(charB_id)
            merged["simChar"].append(simA)
            merged["simOpp"].append(simB)
            merged["simDiff"].append(simDiffAB)
            merged["simDiffRace"].append(simDiffRaceAB)
            merged["simDiffAge"].append(simDiffAgeAB)
            merged["simDiffGender"].append(simDiffGenderAB)
            merged["chosen"].append(chosenA)
            merged["raceChar"].append(raceA)
            merged["ageChar"].append(ageA)
            merged["genderChar"].append(genderA)
            merged["raceOpp"].append(raceB)
            merged["ageOpp"].append(ageB)
            merged["genderOpp"].append(genderB)
            merged["subject_college"].append(subject_college)
            merged["rt"].append(rt)
            merged["data_index"].append(data_index)

            for feature in feature_names:
                merged[f"{feature}Char"].append(charA_row[feature].values[0])
                merged[f"{feature}Opp"].append(charB_row[feature].values[0])
                merged[f"{feature}Diff"].append(charA_row[feature].values[0] - charB_row[feature].values[0])

            # -- Second row: (charB, charA), chosen=(!chosenA)
            simDiffBA = simB - simA
            simDiffRaceBA = simRaceB - simRaceA
            simDiffAgeBA = simAgeB - simAgeA
            simDiffGenderBA = simGenderB - simGenderA
            merged["subject"].append(subject_id)
            merged["task_type"].append(task_type)
            merged["task_ordering"].append(task_ordering)
            merged["condition"].append(condition)
            merged["subject_race"].append(subject_race)
            merged["subject_age"].append(subject_age)
            merged["subject_gender"].append(subject_gender)
            merged["character"].append(charB_id)
            merged["opponent"].append(charA_id)
            merged["simChar"].append(simB)
            merged["simOpp"].append(simA)
            merged["simDiff"].append(simDiffBA)
            merged["simDiffRace"].append(simDiffRaceBA)
            merged["simDiffAge"].append(simDiffAgeBA)
            merged["simDiffGender"].append(simDiffGenderBA)
            merged["chosen"].append(not chosenA)
            merged["raceChar"].append(raceB)
            merged["ageChar"].append(ageB)
            merged["genderChar"].append(genderB)
            merged["raceOpp"].append(raceA)
            merged["ageOpp"].append(ageA)
            merged["genderOpp"].append(genderA)
            merged["subject_college"].append(subject_college)
            merged["rt"].append(rt)
            merged["data_index"].append(data_index)

            for feature in feature_names:
                merged[f"{feature}Char"].append(charB_row[feature].values[0])
                merged[f"{feature}Opp"].append(charA_row[feature].values[0])
                merged[f"{feature}Diff"].append(charB_row[feature].values[0] - charA_row[feature].values[0])

# %%
#| code-summary: Save & optional swapping
df = pd.DataFrame(merged)

# Convert chosen from bool to int
df['chosen'] = df['chosen'].astype(int)

# 1) Save baseline unswapped
outpath = "data/preprocessed/attribute_judgments.csv"
df.to_csv(outpath, index=False)
print(f"Saved to: {outpath}")

df.head()

# %%
