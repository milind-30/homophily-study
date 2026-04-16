## Demographic Model Follow-Up With Participant-Race Interactions

### Participant Groups

| Participant Race | N Participants |
|:--|--:|
| Black | 18 |
| East/Southeast Asian | 28 |
| Hispanic/Latine/Latinx | 16 |
| South Asian | 11 |
| White | 24 |

Excluded from this follow-up due to single-subject cells: Multiracial, Other.

### Specification

`chosen ~ (raceChar + ageChar_c + genderChar) * condition + raceChar * subject_race5 + (1 | character)`

Age was centered at the full-sample mean age of 31.74 years so the intercept remains interpretable as a Black, female face at the sample-mean age in the affiliative frame.

### Fit Diagnostics

- N observations: 5432
- N participants: 97
- AIC: 7147.7
- BIC: 7378.7
- Log-likelihood: -3538.8
- Singular fit: no
- Convergence messages: none

### Fixed Effects

| Fixed Effect | Estimate (beta) | SE | z | p |
|:--|--:|--:|--:|:--|
| (Intercept) | 0.770 | 0.189 | 4.080 | **< .001** |
| East-Asian face (vs. Black) | -0.261 | 0.296 | -0.881 | 0.378 |
| Latino face (vs. Black) | -0.640 | 0.304 | -2.103 | **0.035** |
| South-Asian face (vs. Black) | -1.273 | 0.304 | -4.190 | **< .001** |
| White face (vs. Black) | -1.644 | 0.295 | -5.581 | **< .001** |
| Age (years, centered) | -0.034 | 0.008 | -4.498 | **< .001** |
| Male face (vs. female) | -0.383 | 0.123 | -3.105 | **0.002** |
| High-Stakes / Performance frame | -0.282 | 0.189 | -1.491 | 0.136 |
| Participant race, East/Southeast Asian (vs. Black) | -0.906 | 0.213 | -4.244 | **< .001** |
| Participant race, Hispanic/Latine/Latinx (vs. Black) | -0.499 | 0.277 | -1.799 | 0.072 |
| Participant race, South Asian (vs. Black) | -0.337 | 0.346 | -0.976 | 0.329 |
| Participant race, White (vs. Black) | -0.477 | 0.232 | -2.061 | **0.039** |
| East-Asian face (vs. Black) × High-Stakes / Performance frame | 0.174 | 0.229 | 0.759 | 0.448 |
| Latino face (vs. Black) × High-Stakes / Performance frame | 0.400 | 0.247 | 1.621 | 0.105 |
| South-Asian face (vs. Black) × High-Stakes / Performance frame | 0.474 | 0.254 | 1.864 | 0.062 |
| White face (vs. Black) × High-Stakes / Performance frame | 0.331 | 0.236 | 1.401 | 0.161 |
| Age (years, centered) × High-Stakes / Performance frame | 0.007 | 0.008 | 0.888 | 0.375 |
| Male face (vs. female) × High-Stakes / Performance frame | 0.040 | 0.142 | 0.282 | 0.778 |
| East-Asian face (vs. Black) × Participant race, East/Southeast Asian (vs. Black) | 1.066 | 0.314 | 3.395 | **< .001** |
| Latino face (vs. Black) × Participant race, East/Southeast Asian (vs. Black) | 0.368 | 0.344 | 1.071 | 0.284 |
| South-Asian face (vs. Black) × Participant race, East/Southeast Asian (vs. Black) | 1.656 | 0.342 | 4.838 | **< .001** |
| White face (vs. Black) × Participant race, East/Southeast Asian (vs. Black) | 1.586 | 0.345 | 4.591 | **< .001** |
| East-Asian face (vs. Black) × Participant race, Hispanic/Latine/Latinx (vs. Black) | 0.086 | 0.413 | 0.209 | 0.834 |
| Latino face (vs. Black) × Participant race, Hispanic/Latine/Latinx (vs. Black) | 0.771 | 0.366 | 2.106 | **0.035** |
| South-Asian face (vs. Black) × Participant race, Hispanic/Latine/Latinx (vs. Black) | 0.675 | 0.431 | 1.564 | 0.118 |
| White face (vs. Black) × Participant race, Hispanic/Latine/Latinx (vs. Black) | 1.156 | 0.400 | 2.889 | **0.004** |
| East-Asian face (vs. Black) × Participant race, South Asian (vs. Black) | 0.709 | 0.461 | 1.540 | 0.124 |
| Latino face (vs. Black) × Participant race, South Asian (vs. Black) | 0.308 | 0.484 | 0.637 | 0.524 |
| South-Asian face (vs. Black) × Participant race, South Asian (vs. Black) | 1.087 | 0.449 | 2.421 | **0.015** |
| White face (vs. Black) × Participant race, South Asian (vs. Black) | 0.610 | 0.475 | 1.286 | 0.198 |
| East-Asian face (vs. Black) × Participant race, White (vs. Black) | 0.426 | 0.362 | 1.177 | 0.239 |
| Latino face (vs. Black) × Participant race, White (vs. Black) | 0.429 | 0.365 | 1.175 | 0.240 |
| South-Asian face (vs. Black) × Participant race, White (vs. Black) | 0.898 | 0.364 | 2.466 | **0.014** |
| White face (vs. Black) × Participant race, White (vs. Black) | 1.519 | 0.326 | 4.665 | **< .001** |

### Candidate-Race Contrasts by Participant Group

Group-specific simple effects indicate that the White-face disadvantage was significant for participant groups Black, South Asian, whereas the South-Asian-face disadvantage was significant for participant groups Black.

| Participant Race | Candidate Race Contrast | Estimate (beta) | SE | z | p |
|:--|:--|--:|--:|--:|:--|
| Black | East-Asian vs. Black | -0.261 | 0.296 | -0.881 | 0.378 |
| Black | Latino vs. Black | -0.640 | 0.304 | -2.103 | **0.035** |
| Black | South-Asian vs. Black | -1.273 | 0.304 | -4.190 | **< .001** |
| Black | White vs. Black | -1.644 | 0.295 | -5.581 | **< .001** |
| East/Southeast Asian | East-Asian vs. Black | 0.805 | 0.250 | 3.216 | **0.001** |
| East/Southeast Asian | Latino vs. Black | -0.272 | 0.303 | -0.896 | 0.370 |
| East/Southeast Asian | South-Asian vs. Black | 0.383 | 0.289 | 1.325 | 0.185 |
| East/Southeast Asian | White vs. Black | -0.058 | 0.310 | -0.187 | 0.851 |
| Hispanic/Latine/Latinx | East-Asian vs. Black | -0.175 | 0.376 | -0.465 | 0.642 |
| Hispanic/Latine/Latinx | Latino vs. Black | 0.131 | 0.329 | 0.399 | 0.690 |
| Hispanic/Latine/Latinx | South-Asian vs. Black | -0.598 | 0.393 | -1.521 | 0.128 |
| Hispanic/Latine/Latinx | White vs. Black | -0.488 | 0.361 | -1.350 | 0.177 |
| South Asian | East-Asian vs. Black | 0.449 | 0.440 | 1.018 | 0.308 |
| South Asian | Latino vs. Black | -0.332 | 0.470 | -0.706 | 0.480 |
| South Asian | South-Asian vs. Black | -0.185 | 0.423 | -0.438 | 0.661 |
| South Asian | White vs. Black | -1.033 | 0.456 | -2.266 | **0.023** |
| White | East-Asian vs. Black | 0.165 | 0.274 | 0.602 | 0.548 |
| White | Latino vs. Black | -0.211 | 0.290 | -0.726 | 0.468 |
| White | South-Asian vs. Black | -0.374 | 0.281 | -1.332 | 0.183 |
| White | White vs. Black | -0.124 | 0.235 | -0.529 | 0.597 |
