# AGGIR reference implementation and reference dataset

Supplementary material S6 and S7 of the article *Auditing the algorithms that ration long-term care: exhaustive verification of France's national dependency algorithm and its online calculators* (Koskas P, Koskas R; submitted).

The French national AGGIR algorithm converts eight activity ratings (A, B or C) into an iso-resource group (GIR 1 to 6), which decides eligibility for the personalized autonomy allowance (APA, GIR 1 to 4). Because the algorithm has only 3⁸ = 6,561 possible inputs, any implementation can be checked completely. This repository provides what is needed to do so.

## Contents

| File | What it is |
| --- | --- |
| `aggir_reference.py` | Independent reference implementation of the official algorithm (annex 2-2 of the French Social Action and Families Code), coefficients and thresholds checked by hand against the legal text |
| `data/aggir_6561_profiles.csv` | **Reference dataset (S6)**: all 6,561 profiles with the eight ratings, the total of each coefficient set, the official rank, the GIR and APA eligibility |
| `non_monotonicity.py` | Enumerates the transitions in which worsening one activity gives a less dependent GIR |
| `data/non_monotonic_transitions.csv` | The 30 transitions (12 with loss of APA eligibility) |
| `error_models.py` | Error models reproducing the responses of the three audited calculators that followed the official structure (calculators 1 to 3; sites are not named) |
| `check_my_tool.py` | Compares the results of any GIR calculator, supplied as a CSV file, with the official algorithm |
| `tests/test_reference.py` | Checks the distribution of the 6,561 profiles and the 30 transitions |

The code of the ABC Autonomie website is not part of this repository.

## Quick start

Python 3.8 or later, no external package.

```
python aggir_reference.py AAAAABBA      # rank 11, GIR 4
python aggir_reference.py --write-csv   # regenerates data/aggir_6561_profiles.csv
python non_monotonicity.py              # 30 transitions
python error_models.py                  # 327, 266 and 97 misclassified profiles
python tests/test_reference.py
```

## Conventions

- Order of the eight discriminant variables: coherence, orientation, washing, dressing, eating, toileting hygiene, transfers, indoor mobility.
- Ratings: A, performs the activity alone, spontaneously, completely, habitually and correctly; B, partially; C, does not perform it.
- Coefficient sets are numbered 1 to 8; the official text labels them A to H.
- The two other discriminant variables (outdoor mobility, communication at a distance) and the seven illustrative variables do not enter the calculation.
- All profiles are weighted equally: the proportions describe the rule, not the population.

## Expected distribution

| GIR | 1 | 2 | 3 | 4 | 5 | 6 |
| --- | --- | --- | --- | --- | --- | --- |
| Profiles | 8 | 3,208 | 2,400 | 760 | 157 | 28 |

## Source

Code de l'action sociale et des familles, annexe 2-2, version in force since 13 August 2008 (Légifrance, LEGIARTI000019325260).

## Licence

Code: MIT licence. Data: CC BY 4.0. Please cite the article.

## Contact

AGE ET AUTONOMIE, contact@abc-autonomie.fr
