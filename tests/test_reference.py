"""Run with: python -m pytest tests  (or: python tests/test_reference.py)"""
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import aggir_reference as ref
import non_monotonicity as nm


def test_distribution_of_6561_profiles():
    counts = Counter(ref.gir(p) for p in ref.all_profiles())
    assert dict(counts) == {1: 8, 2: 3208, 3: 2400, 4: 760, 5: 157, 6: 28}


def test_witness_profiles():
    assert ref.gir("AAAAAAAA") == 6
    assert ref.gir("CCCCCCCC") == 1
    assert ref.gir("AAAAABBA") == 4
    assert ref.gir("AAAAABCA") == 5


def test_thirty_non_monotonic_transitions():
    t = nm.transitions()
    assert len(t) == 30
    assert sum(x["loses_apa_eligibility"] for x in t) == 12


if __name__ == "__main__":
    test_distribution_of_6561_profiles()
    test_witness_profiles()
    test_thirty_non_monotonic_transitions()
    print("All tests passed.")
