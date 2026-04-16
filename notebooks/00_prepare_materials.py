# %% [markdown]
"""
# 00_prepare_materials.py

PURPOSE
-------
1. Preprocess and resize images from the Chicago Face Database (CFD), placing them into:
   materials/characters/Age_<bin>_<gender>_<ethnicity>
2. Generate JavaScript files (character_images_local.js and character_images_github.js)
   mapping demographic folders to image paths.

NOTES
-----
- Produces two JS outputs:
    1) Local references (relative paths)
    2) GitHub references (raw URLs)
- After running:
    - Resized images in materials/characters/
    - .js files in experiment/ referencing those images.
"""

# %%
#| code-summary: Imports
import json
import os
import re

import pandas as pd
from PIL import Image

# %%
#| code-summary: Configuration
RESIZE_FACTOR = 8  # Factor by which to reduce image resolution

# Allowed facial expressions for filtering.
# Options are N (neutral), A (angry), F (fear), HC (happy closed mouth), HO (happy open mouth)
allowed_expressions = {"N"}  # Accept only neutral faces

# Mappings to convert gender and ethnicity codes into descriptive labels
gender_map = {"F": "female", "M": "male"}
ethnicity_map = {
    "A": "east-asian",
    "B": "black",
    "I": "south-asian",
    "L": "latino",
    "M": "multiracial",
    "W": "white"
}

# Define directories containing image datasets and corresponding age metadata files
# Each csv contains name and age for each model in the dataset; we have 3 related datasets
data_dirs = [
    ("materials/cfd/images/CFD", "materials/cfd/features.csv"),
    ("materials/cfd/images/CFD-India", "materials/cfd/india_features.csv"),
    # ("materials/cfd/images/CFD-MR", "materials/cfd/mr_age.csv")
]

# Base directory where the processed and relabeled images will be saved
output_base_dir = "materials/characters"
output_js_file_local = "experiment/character_images_local.js"
output_js_file_github = "experiment/character_images_github.js"

# %%
#| code-summary: Helpers
def standardize_model_id(model_id):
    """
    Standardizes a model ID by extracting the base part and reformatting it
    into 'prefix-number' (e.g., "AF-123").
    
    Args:
        model_id (str): The raw model ID from the dataset.

    Returns:
        str: The standardized model ID.
    """
    base_id = model_id.split("-")[0]
    if match := re.match(r"([A-Za-z]+)(\d+)", base_id):
        prefix, number = match.groups()
        return f"{prefix}-{number}"
    return model_id

def parse_demographics(filename):
    """
    Parses demographic and metadata information from a file name.

    Args:
        filename (str): File name of an image (e.g., "CFD-AF-123-N.jpg").

    Returns:
        tuple: Ethnicity (str), gender (str), model ID (str), and expression type (str).
    """
    parts = filename.split("-")
    ethnicity_gender = parts[1]           # e.g. "AF"
    model_id = f"{ethnicity_gender}-{parts[2]}"  # e.g. "AF-123"
    ethnicity_code = ethnicity_gender[0]  # e.g. "A"
    gender_code = ethnicity_gender[1]     # e.g. "F"
    ethnicity = ethnicity_map.get(ethnicity_code, "unknown")
    gender = gender_map.get(gender_code, "unknown")
    expression_type = filename.split("-")[-1][:-4]  # "N"
    return ethnicity, gender, model_id, expression_type

# %%
#| code-summary: Process each dataset directory and its corresponding age CSV

image_count = 0
for cfd_directory, csv_path in data_dirs:
    attr_df = pd.read_csv(csv_path)

    # Standardize the model IDs in the DataFrame for consistent lookup
    attr_df["Model"] = attr_df["Model"].apply(standardize_model_id)

    # Create age groups based on predefined ranges
    attr_df["age_group"] = pd.cut(
        attr_df["Age"],
        bins=[0, 24, 32, 39, float("inf")],
        labels=["24", "25-31", "32-38", "39"]
    )
    attr_df["rounded_age"] = attr_df["Age"].round().astype(int)

    age_map = {
        row["Model"]: (row["age_group"], row["rounded_age"])
        for _, row in attr_df.iterrows()
    }

    used_models = set()

    # Walk through all files in the current dataset directory
    for root, _, files in os.walk(cfd_directory):
        for filename in files:

            # Skip non-JPEG files and files with disallowed expressions or missing age info
            if not filename.endswith(".jpg"):
                continue
            ethnicity, gender, model_id, expression_type = parse_demographics(filename)

            if model_id in used_models or expression_type not in allowed_expressions:
                continue

            age_info = age_map.get(model_id)
            if age_info is None or pd.isna(age_info[0]):
                continue
            
            # Sort the image into the appropriate output directory based on age, gender, ethnicity
            age_group, rounded_age = age_info
            used_models.add(model_id)

            target_dir = os.path.join(
                output_base_dir,
                f"Age_{age_group}_{gender}_{ethnicity}"
            )
            os.makedirs(target_dir, exist_ok=True)

            new_filename = f"cdf_{model_id}_{ethnicity}_{gender}_{rounded_age}.jpg"
            src_path = os.path.join(root, filename)
            dest_path = os.path.join(target_dir, new_filename)

            # Open, resize, and save the image with a reduced resolution
            with Image.open(src_path) as img:
                new_size = (img.width // RESIZE_FACTOR, img.height // RESIZE_FACTOR)
                img = img.resize(new_size, Image.LANCZOS)
                img.save(dest_path, format='JPEG')
                image_count += 1

print(f"Total images used: {image_count}")

# %%
#| code-summary: Generating a JavaScript File with Image Paths by Demographic Bin: Local
print(f"Generating local JS references at {output_js_file_local} ...")

# Base directory containing character folders
base_dir_local = "materials/characters"

# Dictionary to store paths by demographic key
character_images_local = {}

# Walk through each directory and collect file paths
for root, dirs, files in os.walk(base_dir_local):
    for file in files:
        if file.endswith(".jpg") or file.endswith(".png"):

            # Get the demographic folder name (e.g., "Age_<24_female_asian")
            folder_name = os.path.basename(root)
            file_path = os.path.join(root, file).replace("\\", "/")

            # Initialize list for this demographic if it doesn't exist
            if folder_name not in character_images_local:
                character_images_local[folder_name] = []

            # Add file path to the list
            character_images_local[folder_name].append(file_path)

# Convert to JavaScript format and write to file
with open(output_js_file_local, "w") as js_file:
    js_file.write("const characterImages = ")
    json.dump(character_images_local, js_file, indent=4)
    js_file.write(";\n")

print(f"Local version done: {len(character_images_local)} demographic folders processed.")

# %%
#| code-summary: Version 2: Github-hosted image references

print(f"Generating GitHub-based JS references at {output_js_file_github} ...")

# GitHub base URL for raw image access
github_base_url = "https://raw.githubusercontent.com/githubpsyche/images/main/characters"

# Dictionary to store paths by demographic key
character_images_github = {}

# Walk through each directory and collect file paths
for root, dirs, files in os.walk(base_dir_local):
    for file in files:
        if file.endswith(".jpg") or file.endswith(".png"):

            # Get the demographic folder name (e.g., "Age_<24_female_asian")
            folder_name = os.path.basename(root)

            # Create the GitHub URL by constructing the path from folder and file name
            github_url = f"{github_base_url}/{folder_name}/{file}"

            # Initialize list for this demographic if it doesn't exist
            if folder_name not in character_images_github:
                character_images_github[folder_name] = []

            # Add GitHub URL to the list
            character_images_github[folder_name].append(github_url)

# Convert to JavaScript format and write to file
with open(output_js_file_github, "w") as js_file:
    js_file.write("const characterImages = ")
    json.dump(character_images_github, js_file, indent=4)
    js_file.write(";\n")

print(f"GitHub version done: {len(character_images_github)} demographic folders processed.")
