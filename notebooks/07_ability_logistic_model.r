#!/usr/bin/env Rscript

# ==================================================
# Example R script for a two-row-per-pair logistic model
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
#    Typically, 'subject', 'task_type', 'character', 'opponent',
#    or any categorical columns you want to treat as factors:
df <- df %>%
  mutate(
    subject   = factor(subject),
    task_type = factor(task_type),
    character = factor(character),
  )

# 5) Check the Structure (Optional)
str(df)

# 6) Fit the Mixed-Effects Logistic Model
#    In a two-row-per-pair design:
#      - "chosen" is 0 or 1 (whether the focal 'character' was chosen)
#      - "simDiff" can be used or you might directly use "simChar"
#        plus other predictors like "task_type" or interactions.

# Example formula using simDiff * task_type:
#   chosen ~ simDiff * task_type + random intercepts by subject & character
m <- glm(
  chosen ~ simDiff * subject_ability + (1 | subject) + (1 | character),
  data    = df,
  family  = binomial("logit")
)

# 7) Summarize Model Results
summary(m)

# 8) (Optional) Extract Fixed Effects, Random Effects
fixef(m)
ranef(m)

# 9) (Optional) Further Diagnostics or Plots
# e.g., library(ggplot2) to visualize effects
# ...

# ==================================================
# End of Script
# ==================================================
