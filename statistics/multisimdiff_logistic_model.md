## Decomposed Similarity Follow-Up Model

### Specification

`chosen ~ (simDiffRace + simDiffAge + simDiffGender) * condition + (1 | character)`

Positive coefficients indicate that the focal candidate was more likely to be chosen when they matched the participant more than the alternative on that demographic dimension.

### Fit Diagnostics

- AIC: 7208.4
- BIC: 7267.9
- Log-likelihood: -3595.2
- Singular fit: no
- Convergence messages: none

### Fixed Effects

| Fixed Effect | Estimate (beta) | SE | z | p |
|:--|--:|--:|--:|:--|
| (Intercept) | 0.007 | 0.064 | 0.106 | 0.915 |
| Race-match difference | 0.466 | 0.075 | 6.196 | **< .001** |
| Age-match difference | 0.398 | 0.073 | 5.443 | **< .001** |
| Gender-match difference | 0.200 | 0.075 | 2.679 | **0.007** |
| High-Stakes / Performance frame | -0.026 | 0.071 | -0.364 | 0.716 |
| Race-match difference × High-Stakes / Performance frame | -0.320 | 0.102 | -3.125 | **0.002** |
| Age-match difference × High-Stakes / Performance frame | -0.404 | 0.099 | -4.076 | **< .001** |
| Gender-match difference × High-Stakes / Performance frame | 0.029 | 0.104 | 0.276 | 0.782 |

### Random Effects

| Group | Term | Variance | SD |
|:--|:--|--:|--:|
| character | (Intercept) | 0.693 | 0.832 |
