"""Enumerate the non-monotonic transitions of the official AGGIR algorithm.

For every profile and every variable, the rating is worsened by one level
(A to B, or B to C). A transition is non-monotonic when the resulting GIR
indicates LESS dependency (a higher GIR number).

Usage:
    python non_monotonicity.py   -> prints the count, writes data/non_monotonic_transitions.csv
"""

import csv
from pathlib import Path

from aggir_reference import VARIABLES, all_profiles, rank, gir

WORSE = {"A": "B", "B": "C"}


def transitions():
    out = []
    for p in all_profiles():
        for i, r in enumerate(p):
            if r not in WORSE:
                continue
            q = p[:i] + WORSE[r] + p[i + 1:]
            if gir(q) > gir(p):
                out.append({
                    "profile_before": p, "variable": VARIABLES[i],
                    "change": r + "->" + WORSE[r], "profile_after": q,
                    "rank_before": rank(p), "rank_after": rank(q),
                    "gir_before": gir(p), "gir_after": gir(q),
                    "loses_apa_eligibility": int(gir(p) <= 4 < gir(q)),
                })
    return out


if __name__ == "__main__":
    t = transitions()
    path = Path(__file__).with_name("data") / "non_monotonic_transitions.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(t[0]))
        w.writeheader()
        w.writerows(t)
    print("%d non-monotonic transitions, %d with loss of APA eligibility. Written: %s"
          % (len(t), sum(x["loses_apa_eligibility"] for x in t), path))
