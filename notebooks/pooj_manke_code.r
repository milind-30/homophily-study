# Load necessary libraries
# setwd("/Users/shreyasteegala/R Files/Homophily Research")
library(lme4)
library(dplyr)

# Read the data
df <- read.csv("prolific_pairwise.csv", stringsAsFactors = FALSE)

df <- df %>%
  mutate(
    subject   = factor(subject),
    task_type = factor(task_type),
    character = factor(character),
  )

head(df)

# m <- glmer(
#   chosen ~ (simDiffRace + simDiffAge + simDiffGender) * condition  + (1 | character),
#   data  = data,
#   family  = binomial("logit")
# )

# # 7) Summarize Model Results
# summary(m)


# m2 <- glmer(
#   chosen ~ (simDiffRace + simDiffAge + simDiffGender) * task_type  + (1 | character),
#   data  = data,
#   family  = binomial("logit")
# )

# # 7) Summarize Model Results
# summary(m2)


m3 <- glmer(
  chosen ~ raceChar + ageChar + genderChar + (1 | character),
  data  = df,
  family  = binomial("logit")
)

# 7) Summarize Model Results
summary(m3)
