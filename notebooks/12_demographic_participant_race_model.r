#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(lme4)
})

data_path <- "data/preprocessed/prolific_pairwise.csv"
summary_path <- "statistics/demographic_participant_race_model.md"
table_path <- "tables/table_demographic_participant_race.md"

keep_subject_races <- c(
  "Black",
  "East/Southeast Asian",
  "Hispanic/Latine/Latinx",
  "South Asian",
  "White"
)

excluded_subject_races <- c("Multiracial", "Other")

format_num <- function(x, digits = 3) {
  sprintf(paste0("%.", digits, "f"), x)
}

format_p <- function(p) {
  if (is.na(p)) {
    return("NA")
  }

  if (p < 0.001) {
    return("**< .001**")
  }

  value <- sprintf("%.3f", p)
  if (p < 0.05) {
    paste0("**", value, "**")
  } else {
    value
  }
}

markdown_table_lines <- function(df, align, caption = NULL) {
  header <- paste0("| ", paste(names(df), collapse = " | "), " |")
  rule <- paste0("|", paste(align, collapse = "|"), "|")
  rows <- apply(df, 1, function(row) paste0("| ", paste(row, collapse = " | "), " |"))

  lines <- c(header, rule, rows)
  if (!is.null(caption)) {
    lines <- c(lines, "", caption)
  }

  lines
}

write_lines <- function(path, lines) {
  writeLines(lines, con = path)
}

prettify_race_level <- function(level) {
  mapping <- c(
    "black" = "Black",
    "east-asian" = "East-Asian",
    "latino" = "Latino",
    "south-asian" = "South-Asian",
    "white" = "White",
    "Black" = "Black",
    "East/Southeast Asian" = "East/Southeast Asian",
    "Hispanic/Latine/Latinx" = "Hispanic/Latine/Latinx",
    "South Asian" = "South Asian",
    "White" = "White"
  )

  mapping[[level]]
}

pretty_term <- function(term) {
  replacements <- c(
    "(Intercept)" = "(Intercept)",
    "raceChareast-asian" = "East-Asian face (vs. Black)",
    "raceCharlatino" = "Latino face (vs. Black)",
    "raceCharsouth-asian" = "South-Asian face (vs. Black)",
    "raceCharwhite" = "White face (vs. Black)",
    "ageChar_c" = "Age (years, centered)",
    "genderCharmale" = "Male face (vs. female)",
    "conditionCompetitive" = "High-Stakes / Performance frame",
    "subject_race5East/Southeast Asian" = "Participant race, East/Southeast Asian (vs. Black)",
    "subject_race5Hispanic/Latine/Latinx" = "Participant race, Hispanic/Latine/Latinx (vs. Black)",
    "subject_race5South Asian" = "Participant race, South Asian (vs. Black)",
    "subject_race5White" = "Participant race, White (vs. Black)"
  )

  for (pattern in names(replacements)) {
    term <- gsub(pattern, replacements[[pattern]], term, fixed = TRUE)
  }

  term <- gsub(":", " × ", term, fixed = TRUE)
  term
}

fixed_effects_df <- function(model) {
  coefs <- as.data.frame(summary(model)$coefficients)
  coefs$term <- rownames(coefs)
  rownames(coefs) <- NULL

  data.frame(
    `Fixed Effect` = vapply(coefs$term, pretty_term, character(1)),
    `Estimate (beta)` = format_num(coefs$Estimate),
    SE = format_num(coefs$`Std. Error`),
    z = format_num(coefs$`z value`),
    p = vapply(coefs$`Pr(>|z|)`, format_p, character(1)),
    check.names = FALSE,
    stringsAsFactors = FALSE
  )
}

subject_counts_df <- function(df) {
  counts <- aggregate(subject ~ subject_race5, data = unique(df[c("subject", "subject_race5")]), FUN = length)
  data.frame(
    `Participant Race` = as.character(counts$subject_race5),
    `N Participants` = as.character(counts$subject),
    check.names = FALSE,
    stringsAsFactors = FALSE
  )
}

find_term_name <- function(term_names, primary, secondary = NULL) {
  if (primary %in% term_names) {
    return(primary)
  }

  if (!is.null(secondary) && secondary %in% term_names) {
    return(secondary)
  }

  NULL
}

simple_effects_df <- function(model, participant_levels, race_levels) {
  beta <- fixef(model)
  vc <- as.matrix(vcov(model))
  term_names <- names(beta)

  rows <- list()

  for (participant_level in participant_levels) {
    for (race_level in race_levels[-1]) {
      contrast <- setNames(rep(0, length(beta)), term_names)
      main_term <- paste0("raceChar", race_level)
      interaction_primary <- paste0("raceChar", race_level, ":subject_race5", participant_level)
      interaction_secondary <- paste0("subject_race5", participant_level, ":raceChar", race_level)

      contrast[main_term] <- 1

      if (participant_level != "Black") {
        interaction_term <- find_term_name(term_names, interaction_primary, interaction_secondary)
        if (!is.null(interaction_term)) {
          contrast[interaction_term] <- 1
        }
      }

      estimate <- sum(contrast * beta)
      se <- as.numeric(sqrt(t(contrast) %*% vc %*% contrast))
      z_value <- estimate / se
      p_value <- 2 * pnorm(abs(z_value), lower.tail = FALSE)

      rows[[length(rows) + 1]] <- data.frame(
        `Participant Race` = prettify_race_level(participant_level),
        `Candidate Race Contrast` = paste0(prettify_race_level(race_level), " vs. Black"),
        `Estimate (beta)` = format_num(estimate),
        SE = format_num(se),
        z = format_num(z_value),
        p = format_p(p_value),
        estimate_raw = estimate,
        p_raw = p_value,
        stringsAsFactors = FALSE,
        check.names = FALSE
      )
    }
  }

  do.call(rbind, rows)
}

df <- read.csv(data_path, stringsAsFactors = FALSE)
age_mean <- mean(df$ageChar, na.rm = TRUE)

df <- df[df$subject_race %in% keep_subject_races, ]
df$subject <- factor(df$subject)
df$character <- factor(df$character)
df$condition <- factor(df$condition, levels = c("Casual", "Competitive"))
df$raceChar <- factor(
  df$raceChar,
  levels = c("black", "east-asian", "latino", "south-asian", "white")
)
df$genderChar <- factor(df$genderChar, levels = c("female", "male"))
df$subject_race5 <- factor(df$subject_race, levels = keep_subject_races)
df$ageChar_c <- df$ageChar - age_mean

fit_warnings <- character()

model <- withCallingHandlers(
  glmer(
    chosen ~ (raceChar + ageChar_c + genderChar) * condition +
      raceChar * subject_race5 +
      (1 | character),
    data = df,
    family = binomial("logit"),
    control = glmerControl(
      optimizer = "bobyqa",
      optCtrl = list(maxfun = 1e5)
    )
  ),
  warning = function(w) {
    fit_warnings <<- unique(c(fit_warnings, conditionMessage(w)))
    invokeRestart("muffleWarning")
  }
)

opt_messages <- unlist(model@optinfo$conv$lme4$messages)
all_messages <- unique(c(fit_warnings, opt_messages))
singular <- isSingular(model, tol = 1e-4)

counts_df <- subject_counts_df(df)
fixed_df <- fixed_effects_df(model)
simple_df <- simple_effects_df(model, keep_subject_races, levels(df$raceChar))

diagnostic_lines <- if (length(all_messages) == 0) {
  "- Convergence messages: none"
} else {
  c(
    "- Convergence messages:",
    paste0("  - ", all_messages)
  )
}

white_rows <- simple_df[simple_df$`Candidate Race Contrast` == "White vs. Black", ]
south_asian_rows <- simple_df[simple_df$`Candidate Race Contrast` == "South-Asian vs. Black", ]

significant_groups <- function(rows) {
  rows$`Participant Race`[rows$p_raw < 0.05 & rows$estimate_raw < 0]
}

white_sig <- significant_groups(white_rows)
south_asian_sig <- significant_groups(south_asian_rows)

interpretation_line <- paste0(
  "Group-specific simple effects indicate that the White-face disadvantage was significant for participant groups ",
  if (length(white_sig) == 0) "none" else paste(white_sig, collapse = ", "),
  ", whereas the South-Asian-face disadvantage was significant for participant groups ",
  if (length(south_asian_sig) == 0) "none" else paste(south_asian_sig, collapse = ", "),
  "."
)

summary_lines <- c(
  "## Demographic Model Follow-Up With Participant-Race Interactions",
  "",
  "### Participant Groups",
  "",
  markdown_table_lines(
    counts_df,
    align = c(":--", "--:")
  ),
  "",
  paste0(
    "Excluded from this follow-up due to single-subject cells: ",
    paste(excluded_subject_races, collapse = ", "),
    "."
  ),
  "",
  "### Specification",
  "",
  "`chosen ~ (raceChar + ageChar_c + genderChar) * condition + raceChar * subject_race5 + (1 | character)`",
  "",
  paste0(
    "Age was centered at the full-sample mean age of ",
    format_num(age_mean, 2),
    " years so the intercept remains interpretable as a Black, female face at the sample-mean age in the affiliative frame."
  ),
  "",
  "### Fit Diagnostics",
  "",
  paste0("- N observations: ", nrow(df)),
  paste0("- N participants: ", nlevels(df$subject)),
  paste0("- AIC: ", format_num(AIC(model), 1)),
  paste0("- BIC: ", format_num(BIC(model), 1)),
  paste0("- Log-likelihood: ", format_num(as.numeric(logLik(model)), 1)),
  paste0("- Singular fit: ", if (singular) "yes" else "no"),
  diagnostic_lines,
  "",
  "### Fixed Effects",
  "",
  markdown_table_lines(
    fixed_df,
    align = c(":--", "--:", "--:", "--:", ":--")
  ),
  "",
  "### Candidate-Race Contrasts by Participant Group",
  "",
  interpretation_line,
  "",
  markdown_table_lines(
    simple_df[, c("Participant Race", "Candidate Race Contrast", "Estimate (beta)", "SE", "z", "p")],
    align = c(":--", ":--", "--:", "--:", "--:", ":--")
  )
)

table_lines <- markdown_table_lines(
  simple_df[, c("Participant Race", "Candidate Race Contrast", "Estimate (beta)", "SE", "z", "p")],
  align = c(":--", ":--", "--:", "--:", "--:", ":--"),
  caption = ": Simple effects from the participant-race follow-up to the demographic-only model. Each row reports the candidate-race contrast relative to Black faces within one participant-race group, based on a logistic mixed model that also controlled for target age, target gender, framing condition, and a random intercept for character. Positive coefficients indicate that the focal candidate was more likely to be chosen than a Black face within that participant group; negative coefficients indicate relative avoidance. Multiracial and Other participants were excluded from this follow-up because each group contained a single participant. {#tbl-demo-participant-race}"
)

write_lines(summary_path, summary_lines)
write_lines(table_path, table_lines)

cat("Wrote ", summary_path, "\n", sep = "")
cat("Wrote ", table_path, "\n", sep = "")
