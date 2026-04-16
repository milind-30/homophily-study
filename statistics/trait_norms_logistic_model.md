## Trait-Norm Follow-Up Models

Each model regressed whether the focal face was chosen on the signed focal-minus-opponent difference score for a single CFD trait, framing condition, and their interaction, with a random intercept for character:

`chosen ~ traitDiff * condition + (1 | character)`

Positive baseline coefficients indicate that, in the affiliative frame, focal faces higher on that trait than the alternative were more likely to be chosen. Positive interaction coefficients indicate attenuation or reversal of that trait effect in the performance frame.
Trait-by-frame interactions remaining significant after BH correction: Sadness, Threat.

### Attractiveness

- N: 5544
- AIC: 7275.8
- Singular fit: no
- Convergence messages: none

| Term | Estimate (beta) | SE | z | p | Interaction p_adj |
|:--|--:|--:|--:|:--|:--|
| Attractiveness difference | 0.406 | 0.048 | 8.501 | **< .001** |  |
| Attractiveness difference × High-Stakes / Performance frame | -0.130 | 0.060 | -2.178 | **0.029** | 0.059 |

### Dominance

- N: 3802
- AIC: 5078.5
- Singular fit: no
- Convergence messages: none

| Term | Estimate (beta) | SE | z | p | Interaction p_adj |
|:--|--:|--:|--:|:--|:--|
| Dominance difference | -0.068 | 0.063 | -1.081 | 0.280 |  |
| Dominance difference × High-Stakes / Performance frame | -0.099 | 0.080 | -1.231 | 0.218 | 0.218 |

### Happiness

- N: 5544
- AIC: 7329.7
- Singular fit: no
- Convergence messages: none

| Term | Estimate (beta) | SE | z | p | Interaction p_adj |
|:--|--:|--:|--:|:--|:--|
| Happiness difference | 0.289 | 0.050 | 5.747 | **< .001** |  |
| Happiness difference × High-Stakes / Performance frame | -0.084 | 0.063 | -1.341 | 0.180 | 0.216 |

### Sadness

- N: 5544
- AIC: 7325.9
- Singular fit: no
- Convergence messages: none

| Term | Estimate (beta) | SE | z | p | Interaction p_adj |
|:--|--:|--:|--:|:--|:--|
| Sadness difference | -0.338 | 0.050 | -6.699 | **< .001** |  |
| Sadness difference × High-Stakes / Performance frame | 0.174 | 0.064 | 2.721 | **0.007** | **0.029** |

### Threat

- N: 5544
- AIC: 7297.4
- Singular fit: no
- Convergence messages: none

| Term | Estimate (beta) | SE | z | p | Interaction p_adj |
|:--|--:|--:|--:|:--|:--|
| Threat difference | -0.435 | 0.054 | -8.002 | **< .001** |  |
| Threat difference × High-Stakes / Performance frame | 0.184 | 0.071 | 2.591 | **0.010** | **0.029** |

### Trustworthiness

- N: 5544
- AIC: 7331.6
- Singular fit: no
- Convergence messages: none

| Term | Estimate (beta) | SE | z | p | Interaction p_adj |
|:--|--:|--:|--:|:--|:--|
| Trustworthiness difference | 0.379 | 0.067 | 5.675 | **< .001** |  |
| Trustworthiness difference × High-Stakes / Performance frame | -0.115 | 0.083 | -1.381 | 0.167 | 0.216 |

