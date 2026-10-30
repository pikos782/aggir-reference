"""Error models of the three audited calculators that followed the official
structure (calculators 1 to 3 in the article; sites are not named).

Each model is the reference algorithm with the smallest set of changes that
reproduced all 6,561 responses of that calculator during the audit.
The models of calculators 4 to 6, which used rules of their own design,
are not published here.

Usage:
    python error_models.py   -> prints, for each model, the number of
                                misclassified profiles and of eligibility changes
"""

import copy

import aggir_reference as ref

# Index of each variable in a coefficient row.
COH, ORI, WAS, DRE, EAT, TOI, TRA, MOB = range(8)


def make_model(changes=(), strict_set8_rank11=False):
    """changes: (set, rating, variable index, new value)."""
    sets = copy.deepcopy(ref.SETS)
    for s, rating, i, v in changes:
        sets[s][rating][i] = v

    def total(s, p):
        return sum(sets[s][r][i] for i, r in enumerate(p) if r in "BC")

    def gir(profile):
        p = ref.parse(profile)
        for s, minimum, r in ref.THRESHOLDS:
            t = total(s, p)
            if (s, r) == (8, 11) and strict_set8_rank11:
                hit = t > minimum
            else:
                hit = t >= minimum
            if hit:
                return ref.RANK_TO_GIR[r]
        return ref.RANK_TO_GIR[ref.DEFAULT_RANK]

    return gir


MODELS = {
    # Set 4, row B: the 200 points of eating shifted to indoor mobility;
    # set 8: rank 11 threshold applied as "greater than" 4,000.
    "calculator 1": make_model([(4, "B", EAT, 0), (4, "B", MOB, 200)],
                               strict_set8_rank11=True),
    # Set 6: indoor mobility C = 500 instead of 200; coherence B = 0 instead of 100.
    "calculator 2": make_model([(6, "C", MOB, 500), (6, "B", COH, 0)]),
    # Set 8: eating B = 200 instead of 2,000. (This calculator also aggregated
    # the dressing sub-items differently; not modelled, as sub-items were not varied.)
    "calculator 3": make_model([(8, "B", EAT, 200)]),
}


if __name__ == "__main__":
    profiles = ref.all_profiles()
    for name, model in MODELS.items():
        wrong = [p for p in profiles if model(p) != ref.gir(p)]
        excluded = sum(ref.gir(p) <= 4 < model(p) for p in wrong)
        included = sum(model(p) <= 4 < ref.gir(p) for p in wrong)
        print("%s: %d misclassified (%.1f%%), %d falsely ineligible, %d falsely eligible"
              % (name, len(wrong), 100 * len(wrong) / len(profiles), excluded, included))
