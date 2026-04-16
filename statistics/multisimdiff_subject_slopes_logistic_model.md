## Decomposed Similarity Follow-Up Model with Participant-Level Slopes

### Specification

`chosen ~ (simDiffRace + simDiffAge + simDiffGender) * condition + (1 | character) + (0 + simDiffRace + simDiffAge + simDiffGender | subject)`

Positive coefficients indicate that the focal candidate was more likely to be chosen when they matched the participant more than the alternative on that demographic dimension.

### Fit Diagnostics

- AIC: 6034.1
- BIC: 6133.4
- Log-likelihood: -3002.1
- Singular fit: no
- Convergence messages: none

### Fixed Effects

| Fixed Effect | Estimate (beta) | SE | z | p |
|:--|--:|--:|--:|:--|
| (Intercept) | 0.021 | 0.067 | 0.314 | 0.754 |
| Race-match difference | 0.885 | 0.259 | 3.414 | **< .001** |
| Age-match difference | 0.602 | 0.264 | 2.277 | **0.023** |
| Gender-match difference | 0.459 | 0.293 | 1.567 | 0.117 |
| High-Stakes / Performance frame | -0.025 | 0.079 | -0.312 | 0.755 |
| Race-match difference × High-Stakes / Performance frame | -0.548 | 0.354 | -1.548 | 0.122 |
| Age-match difference × High-Stakes / Performance frame | -0.475 | 0.362 | -1.312 | 0.190 |
| Gender-match difference × High-Stakes / Performance frame | -0.168 | 0.403 | -0.418 | 0.676 |

### Random Effects

| Group | Term | Variance | SD |
|:--|:--|--:|--:|
| character | (Intercept) | 0.518 | 0.720 |
| subject | simDiffRace | 2.544 | 1.595 |
| subject | simDiffAge | 2.770 | 1.664 |
| subject | simDiffGender | 3.406 | 1.845 |
