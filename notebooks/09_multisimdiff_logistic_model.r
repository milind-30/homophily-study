#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(lme4)
})

data_path <- "data/preprocessed/prolific_pairwise.csv"
summary_path <- "statistics/multisimdiff_logistic_model.md"
table_path <- "tables/table_multisimdiff_condition_simple.md"

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

pretty_term <- function(term) {
  term <- gsub("simDiffRace", "Race-match difference", term, fixed = TRUE)
  term <- gsub("simDiffAge", "Age-match difference", term, fixed = TRUE)
  term <- gsub("simDiffGender", "Gender-match difference", term, fixed = TRUE)
  term <- gsub(
    "conditionCompetitive",
    "High-Stakes / Performance frame",
    term,
    fixed = TRUE
  )
  term <- gsub(":", " × ", term, fixed = TRUE)
  term
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

random_effects_df <- function(model) {
  re <- as.data.frame(VarCorr(model))
  re <- re[is.na(re$var2), c("grp", "var1", "vcov", "sdcor")]
  names(re) <- c("Group", "Term", "Variance", "SD")

  re$Group <- as.character(re$Group)
  re$Term <- as.character(re$Term)
  re$Variance <- format_num(re$Variance)
  re$SD <- format_num(re$SD)
  re
}

write_lines <- function(path, lines) {
  writeLines(lines, con = path)
}

df <- read.csv(data_path, stringsAsFactors = FALSE)
df$subject <- factor(df$subject)
df$character <- factor(df$character)
df$condition <- factor(df$condition, levels = c("Casual", "Competitive"))

fit_warnings <- character()

model <- withCallingHandlers(
  glmer(
    chosen ~ (simDiffRace + simDiffAge + simDiffGender) * condition + (1 | character),
    data = df,
    family = binomial("logit")
  ),
  warning = function(w) {
    fit_warnings <<- unique(c(fit_warnings, conditionMessage(w)))
    invokeRestart("muffleWarning")
  }
)

opt_messages <- unlist(model@optinfo$conv$lme4$messages)
all_messages <- unique(c(fit_warnings, opt_messages))
singular <- isSingular(model, tol = 1e-4)

fixed_df <- fixed_effects_df(model)
random_df <- random_effects_df(model)

diagnostic_lines <- if (length(all_messages) == 0) {
  "- Convergence messages: none"
} else {
  c(
    "- Convergence messages:",
    paste0("  - ", all_messages)
  )
}

summary_lines <- c(
  "## Decomposed Similarity Follow-Up Model",
  "",
  "### Specification",
  "",
  "`chosen ~ (simDiffRace + simDiffAge + simDiffGender) * condition + (1 | character)`",
  "",
  "Positive coefficients indicate that the focal candidate was more likely to be chosen when they matched the participant more than the alternative on that demographic dimension.",
  "",
  "### Fit Diagnostics",
  "",
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
  "### Random Effects",
  "",
  markdown_table_lines(
    random_df,
    align = c(":--", ":--", "--:", "--:")
  )
)

table_lines <- markdown_table_lines(
  fixed_df,
  align = c(":--", "--:", "--:", "--:", ":--"),
  caption = ": Fixed effects from the decomposed follow-up model replacing the summed self-similarity gap with separate race-, age-, and gender-match differences. Positive coefficients indicate that the focal candidate was more likely to be chosen when they were relatively more similar to the participant than the alternative on that dimension. {#tbl-multisimdiff-components}"
)

write_lines(summary_path, summary_lines)
write_lines(table_path, table_lines)

cat("Wrote ", summary_path, "\n", sep = "")
cat("Wrote ", table_path, "\n", sep = "")
