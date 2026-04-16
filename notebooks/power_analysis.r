setwd("/Users/shreyasteegala/R Files/Homophily Research")

data <- read.csv("prolific_first_pass_data.csv")

library(lme4)  # For mixed-effects models
library(simr)  # For power analysis

data$chosen <- factor(data$chosen, levels = c("False", "True"))

# Fit the model
model <- glmer(
  chosen ~ shared_features * condition + shared_features * task_type + # Main effects and interaction
    (0 + shared_features| subject),
  data = data,                      # Replace with your actual dataset
  family = binomial(link = "logit")       # Logistic regression for binary outcome
)

summary(model)

# PROBLEM: How to configure/test the interaction effect? Right now just have slope effect and correlation 0. But when slope and intercept used, it's 1. 