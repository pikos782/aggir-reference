"""Check any GIR calculator against the official algorithm.

Prepare a CSV file with two columns, "profile" (8 letters A/B/C in the order
coherence, orientation, washing, dressing, eating, toileting hygiene,
transfers, indoor mobility) and "gir" (the result returned by your tool),
ideally for all 6,561 profiles listed in data/aggir_6561_profiles.csv.

Usage:
    python check_my_tool.py my_results.csv
Exit code 0 if every profile agrees, 1 otherwise.
"""

import csv
import sys

import aggir_reference as ref


def main(path):
    rows = list(csv.DictReader(open(path, encoding="utf-8")))
    wrong = [(r["profile"], int(r["gir"]), ref.gir(r["profile"])) for r in rows
             if int(r["gir"]) != ref.gir(r["profile"])]
    print("%d profiles checked, %d disagree with the official algorithm." % (len(rows), len(wrong)))
    for p, mine, official in wrong[:20]:
        print("  %s: your tool %d, official %d" % (p, mine, official))
    if len(rows) < 6561:
        print("Note: only %d of the 6,561 possible profiles were checked." % len(rows))
    return 0 if not wrong else 1


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
