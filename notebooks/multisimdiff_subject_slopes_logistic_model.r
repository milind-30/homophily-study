#!/usr/bin/env Rscript

# ==================================================
# Example R script: Feature-specific simDiff variables
# with subject-specific slopes
# ==================================================

# 1) Load Necessary Packages
# install.packages("lme4")    # if not installed
# install.packages("dplyr")   # if not installed

library(lme4)
library(dplyr)

# 2) Read the Data
file_arg <- grep("^--file=", commandArgs(trailingOnly = FALSE), value = TRUE)
root_candidates <- c(
  if (length(file_arg)) file.path(dirname(sub("^--file=", "", file_arg[1])), "..") else NULL,
  getwd(),
  file.path(getwd(), "..")
)
data_path <- NULL
for (candidate_root in root_candidates) {
  candidate_path <- normalizePath(
    file.path(candidate_root, "data", "preprocessed", "prolific_pairwise.csv"),
    winslash = "/",
    mustWork = FALSE
  )
  if (file.exists(candidate_path)) {
    data_path <- candidate_path
    break
  }
}
if (is.null(data_path)) {
  stop("Could not locate data/preprocessed/prolific_pairwise.csv")
}
df <- read.csv(data_path, stringsAsFactors = FALSE)

# 3) Inspect the First Rows (Optional)
head(df)

# 4) Convert Relevant Columns to Factors
df <- df %>%
  mutate(
    subject   = factor(subject),
    task_type = factor(task_type),
    character = factor(character),
    condition = factor(condition)  # ensure 'condition' is a factor
  )

# 5) Check the Structure (Optional)
str(df)

# 6) Fit the Mixed-Effects Logistic Model
#    - We replace "simDiff" with "simDiffAge + simDiffGender + simDiffRace" 
#    - We allow random intercepts for character plus subject-specific slopes 
#      for each simDiff dimension.
#    - We also switch optimizer to "bobyqa" and raise maxfun to help convergence.

m_featspec_slopes <- glmer(
  chosen ~ simDiff * task_type * condition
    + (1 | character)
    + (0 + simDiffAge + simDiffGender + simDiffRace | subject), 
  data    = df,
  family  = binomial("logit"),
  control = glmerControl(
    optimizer = "bobyqa",
    optCtrl   = list(maxfun = 1e5)   # Increase iterations for better convergence
  )
)

# 7) Summarize Model Results
summary(m_featspec_slopes)

# 8) (Optional) Extract Fixed and Random Effects
fixef(m_featspec_slopes)
ranef(m_featspec_slopes)

# 9) (Optional) Further Diagnostics or Plots
#    e.g., library(ggplot2) for effect plots, or check for convergence warnings.
# ==================================================
# End of Script
# ==================================================
