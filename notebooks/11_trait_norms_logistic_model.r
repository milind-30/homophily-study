#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(lme4)
})

data_path <- "data/preprocessed/prolific_pairwise.csv"
summary_path <- "statistics/trait_norms_logistic_model.md"
table_path <- "tables/table_trait_norms_condition.md"

traits <- list(
  list(column = "AttractiveDiff", label = "Attractiveness"),
  list(column = "DominantDiff", label = "Dominance"),
  list(column = "HappyDiff", label = "Happiness"),
  list(column = "SadDiff", label = "Sadness"),
  list(column = "ThreateningDiff", label = "Threat"),
  list(column = "TrustworthyDiff", label = "Trustworthiness")
)

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

format_p_plain <- function(p) {
  if (is.na(p)) {
    return("NA")
  }

  if (p < 0.001) {
    return("< .001")
  }

  sprintf("%.3f", p)
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

fit_trait_model <- function(df, trait_column, label) {
  trait_df <- df[!is.na(df[[trait_column]]), c("chosen", "character", "condition", trait_column)]
  names(trait_df)[names(trait_df) == trait_column] <- "traitDiff"

  fit_warnings <- character()
  model <- withCallingHandlers(
    glmer(
      chosen ~ traitDiff * condition + (1 | character),
      data = trait_df,
      family = binomial("logit")
    ),
    warning = function(w) {
      fit_warnings <<- unique(c(fit_warnings, conditionMessage(w)))
      invokeRestart("muffleWarning")
    }
  )

  coefs <- as.data.frame(summary(model)$coefficients)
  coefs$term <- rownames(coefs)
  rownames(coefs) <- NULL

  interaction_term <- "traitDiff:conditionCompetitive"
  interaction_row <- coefs[coefs$term == interaction_term, ]
  baseline_row <- coefs[coefs$term == "traitDiff", ]

  messages <- unlist(model@optinfo$conv$lme4$messages)
  diagnostics <- unique(c(fit_warnings, messages))

  list(
    label = label,
    n = nrow(trait_df),
    model = model,
    singular = isSingular(model, tol = 1e-4),
    diagnostics = diagnostics,
    baseline = baseline_row,
    interaction = interaction_row
  )
}

df <- read.csv(data_path, stringsAsFactors = FALSE)
df$character <- factor(df$character)
df$condition <- factor(df$condition, levels = c("Casual", "Competitive"))

results <- lapply(traits, function(trait) fit_trait_model(df, trait$column, trait$label))

interaction_ps <- vapply(
  results,
  function(result) result$interaction$`Pr(>|z|)`,
  numeric(1)
)

interaction_ps_adj <- p.adjust(interaction_ps, method = "BH")

for (i in seq_along(results)) {
  results[[i]]$interaction_p_adj <- interaction_ps_adj[[i]]
}

robust_labels <- vapply(
  results[interaction_ps_adj < 0.05],
  function(result) result$label,
  character(1)
)

robust_summary <- if (length(robust_labels) == 0) {
  "No trait-by-frame interactions remained significant after BH correction."
} else {
  paste0(
    "Trait-by-frame interactions remaining significant after BH correction: ",
    paste(robust_labels, collapse = ", "),
    "."
  )
}

summary_sections <- unlist(lapply(results, function(result) {
  diagnostics <- if (length(result$diagnostics) == 0) {
    "- Convergence messages: none"
  } else {
    c("- Convergence messages:", paste0("  - ", result$diagnostics))
  }

  coef_df <- data.frame(
    Term = c(
      paste0(result$label, " difference"),
      paste0(result$label, " difference × High-Stakes / Performance frame")
    ),
    `Estimate (beta)` = c(
      format_num(result$baseline$Estimate),
      format_num(result$interaction$Estimate)
    ),
    SE = c(
      format_num(result$baseline$`Std. Error`),
      format_num(result$interaction$`Std. Error`)
    ),
    z = c(
      format_num(result$baseline$`z value`),
      format_num(result$interaction$`z value`)
    ),
    p = c(
      format_p(result$baseline$`Pr(>|z|)`),
      format_p(result$interaction$`Pr(>|z|)`)
    ),
    `Interaction p_adj` = c(
      "",
      format_p(result$interaction_p_adj)
    ),
    check.names = FALSE,
    stringsAsFactors = FALSE
  )

  c(
    paste0("### ", result$label),
    "",
    paste0("- N: ", result$n),
    paste0("- AIC: ", format_num(AIC(result$model), 1)),
    paste0("- Singular fit: ", if (result$singular) "yes" else "no"),
    diagnostics,
    "",
    markdown_table_lines(
      coef_df,
      align = c(":--", "--:", "--:", "--:", ":--", ":--")
    ),
    ""
  )
}))

summary_lines <- c(
  "## Trait-Norm Follow-Up Models",
  "",
  "Each model regressed whether the focal face was chosen on the signed focal-minus-opponent difference score for a single CFD trait, framing condition, and their interaction, with a random intercept for character:",
  "",
  "`chosen ~ traitDiff * condition + (1 | character)`",
  "",
  "Positive baseline coefficients indicate that, in the affiliative frame, focal faces higher on that trait than the alternative were more likely to be chosen. Positive interaction coefficients indicate attenuation or reversal of that trait effect in the performance frame.",
  robust_summary,
  "",
  summary_sections
)

table_df <- data.frame(
  Trait = vapply(results, function(result) result$label, character(1)),
  N = vapply(results, function(result) as.character(result$n), character(1)),
  `Trait Difference (beta)` = vapply(results, function(result) format_num(result$baseline$Estimate), character(1)),
  `SE` = vapply(results, function(result) format_num(result$baseline$`Std. Error`), character(1)),
  `z` = vapply(results, function(result) format_num(result$baseline$`z value`), character(1)),
  `p` = vapply(results, function(result) format_p(result$baseline$`Pr(>|z|)`), character(1)),
  `Trait Difference × High-Stakes (beta)` = vapply(results, function(result) format_num(result$interaction$Estimate), character(1)),
  `SE ` = vapply(results, function(result) format_num(result$interaction$`Std. Error`), character(1)),
  `z ` = vapply(results, function(result) format_num(result$interaction$`z value`), character(1)),
  `p ` = vapply(results, function(result) format_p(result$interaction$`Pr(>|z|)`), character(1)),
  `p_adj ` = vapply(results, function(result) format_p_plain(result$interaction_p_adj), character(1)),
  check.names = FALSE,
  stringsAsFactors = FALSE
)

table_lines <- markdown_table_lines(
  table_df,
  align = c(":--", "--:", "--:", "--:", "--:", ":--", "--:", "--:", "--:", ":--", ":--"),
  caption = ": Fixed effects from six separate trait-norm logistic mixed models. Each model regressed whether the focal face was chosen on the signed focal-minus-opponent difference score for one CFD trait, framing condition, and their interaction, with a random intercept for character. Positive baseline coefficients indicate that higher values of the focal trait increased selection in the affiliative frame; positive interaction coefficients indicate attenuation or reversal of that effect in the high-stakes/performance frame. `p_adj` reports Benjamini-Hochberg adjusted p-values across the six trait-by-frame interaction tests. {#tbl-trait-norms}"
)

write_lines(summary_path, summary_lines)
write_lines(table_path, table_lines)

cat("Wrote ", summary_path, "\n", sep = "")
cat("Wrote ", table_path, "\n", sep = "")
