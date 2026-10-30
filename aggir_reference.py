"""Independent reference implementation of the French national AGGIR algorithm.

Source: Code de l'action sociale et des familles, annex 2-2
(version in force since 13 August 2008, Legifrance LEGIARTI000019325260).
Coefficients and thresholds were checked by hand against the legal text
(29-30 October 2026).

A profile is a sequence of eight ratings, "A", "B" or "C", in this order:
coherence, orientation, washing, dressing, eating, toileting hygiene,
transfers, indoor mobility.

Usage:
    python aggir_reference.py AAAAABBA      -> prints rank and GIR
    python aggir_reference.py --write-csv   -> writes data/aggir_6561_profiles.csv
"""

import csv
import itertools
import sys
from pathlib import Path

VARIABLES = ["coherence", "orientation", "washing", "dressing",
             "eating", "toileting_hygiene", "transfers", "indoor_mobility"]

# Coefficient sets 1 to 8 (labelled A to H in the official text).
# For each set: points if rated B, points if rated C, in the order of VARIABLES.
SETS = {
    1: {"B": [0, 0, 16, 16, 20, 16, 120, 32],
        "C": [2000, 1200, 40, 40, 60, 100, 800, 200]},
    2: {"B": [320, 120, 16, 16, 0, 16, 120, -40],
        "C": [1500, 1200, 40, 40, 60, 100, 800, -80]},
    3: {"B": [0, 0, 16, 16, 20, 20, 200, 40],
        "C": [0, 0, 40, 40, 60, 160, 1000, 400]},
    4: {"B": [0, 0, 0, 0, 200, 200, 200, 0],
        "C": [0, 0, 0, 0, 2000, 400, 2000, 200]},
    5: {"B": [0, 0, 100, 100, 100, 100, 100, 0],
        "C": [400, 400, 400, 400, 400, 800, 800, 200]},
    6: {"B": [100, 100, 100, 100, 100, 100, 100, 0],
        "C": [200, 200, 500, 500, 500, 500, 500, 200]},
    7: {"B": [0, 0, 200, 200, 200, 200, 200, 100],
        "C": [150, 150, 300, 300, 500, 500, 400, 200]},
    8: {"B": [0, 0, 2000, 2000, 2000, 2000, 2000, 1000],
        "C": [0, 0, 3000, 3000, 3000, 3000, 1000, 1000]},
}

# Tested in this order; the first threshold reached gives the rank.
# All comparisons are "greater than or equal to".
THRESHOLDS = [  # (set, minimum total, rank)
    (1, 4380, 1), (1, 4140, 2), (1, 3390, 3),
    (2, 2016, 4),
    (3, 1700, 5), (3, 1432, 6),
    (4, 2400, 7),
    (5, 1200, 8),
    (6, 800, 9),
    (7, 650, 10),
    (8, 4000, 11), (8, 2000, 12),
]
DEFAULT_RANK = 13

RANK_TO_GIR = {1: 1, 2: 2, 3: 2, 4: 2, 5: 2, 6: 2, 7: 2,
               8: 3, 9: 3, 10: 4, 11: 4, 12: 5, 13: 6}


def parse(profile):
    """'AABBAAAA' or ['A', 'A', ...] -> tuple of 8 ratings."""
    p = tuple(str(x).strip().upper() for x in profile)
    if len(p) != 8 or any(x not in "ABC" for x in p):
        raise ValueError("A profile is 8 ratings among A, B, C: %r" % (profile,))
    return p


def set_total(set_number, profile):
    p = parse(profile)
    coef = SETS[set_number]
    return sum(coef[r][i] for i, r in enumerate(p) if r in "BC")


def rank(profile):
    p = parse(profile)
    for s, minimum, r in THRESHOLDS:
        if set_total(s, p) >= minimum:
            return r
    return DEFAULT_RANK


def gir(profile):
    return RANK_TO_GIR[rank(profile)]


def apa_eligible(profile):
    """Eligibility for the allocation personnalisee d'autonomie (GIR 1 to 4)."""
    return gir(profile) <= 4


def all_profiles():
    return ["".join(p) for p in itertools.product("ABC", repeat=8)]


def write_csv(path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["profile"] + VARIABLES +
                   ["set%d_total" % s for s in range(1, 9)] +
                   ["rank", "gir", "apa_eligible"])
        for p in all_profiles():
            w.writerow([p] + list(p) + [set_total(s, p) for s in range(1, 9)] +
                       [rank(p), gir(p), int(apa_eligible(p))])
    return path


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--write-csv":
        print("Written:", write_csv(Path(__file__).with_name("data") / "aggir_6561_profiles.csv"))
    elif len(sys.argv) == 2:
        p = sys.argv[1]
        print("profile %s: rank %d, GIR %d, APA eligible: %s"
              % (p.upper(), rank(p), gir(p), "yes" if apa_eligible(p) else "no"))
    else:
        print(__doc__)
