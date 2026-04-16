# %%  Setup: load and preprocess data  ---------------------------------------
import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from notebooks.helpers import bootstrap_ci

DATA_PATH = "data/preprocessed/prolific_pairwise.csv"
df = pd.read_csv(DATA_PATH)

# Relabel and filter
df = df.rename(columns={"condition": "Condition"})
df["Condition"] = df["Condition"].replace({
    "Casual": "Low-Stakes / Affiliative Frame",
    "Competitive": "High-Stakes / Performance Frame"
})
df = df[(df["rt"].between(150, 10_000)) & (df["simDiff"] > 0)].copy()
df["log_rt"] = np.log(df["rt"])

print(f"Data loaded: {len(df)} usable trials")

# %%  Participant‑level correlation tests (low‑stakes frame)

from scipy.stats import spearmanr

# ── Filter low‑stakes (affiliative) rows only ───────────────────────────────
d_aff = df[df["Condition"] == "Low-Stakes / Affiliative Frame"]

# Compute participant‑level means at each gap
pm = (
    d_aff.groupby(["subject", "simDiff"])
         .agg(pref=("chosen", "mean"),
              log_rt=("log_rt", "mean"))
         .reset_index()
)

# Spearman correlations using all participant‑gap observations
rho_pref, p_pref = spearmanr(pm["simDiff"], pm["pref"])      # expect positive
rho_rt,   p_rt   = spearmanr(pm["simDiff"], pm["log_rt"])    # expect negative

print(f"Preference vs. gap  (participant means):  ρ = {rho_pref:+.3f}, p = {p_pref:.4g}")
print(f"log‑RT vs. gap      (participant means):  ρ = {rho_rt:+.3f}, p = {p_rt:.4g}")
