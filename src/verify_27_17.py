"""
verify_27_17.py

Independent Python verification of the critical case (x=27, y=17), which is
the closest pair to the convergent (485, 306) of log_2(3) within reach of
exhaustive enumeration.

Why this case matters:
  - 2^27 - 3^17 = 5,077,565 (closest "diff" relative to |Sigma| in our table)
  - |Sigma(27, 17)| = C(26, 16) = 5,311,735
  - Crandall expectation E_Cr = 5,311,735 / 5,077,565 ≈ 1.046
  - This is the only enumerable case with E_Cr > 1 individually (besides the
    tiny (8,5)). Any non-trivial zero here would invalidate Conjecture 1.

This script reproduces the result of enumerate_compositions.c using only
Python's arbitrary-precision integers, thereby ruling out any possibility
of a C-level overflow bug or modular-arithmetic mistake.

Expected output:
  Total compositions      : 5,311,735  (= C(26, 16))
  Zero count (mod diff)   : 0
  Crandall expectation    : ~1.046
  Result                  : consistent with Conjecture 1

Runtime: ~25 seconds on a single core.

Author: Oriol Corcoll Arias, 2026
License: MIT
"""

import time
from itertools import combinations
from math import comb


def cycle_value_exact(period):
    """C(y, sigma) = sum_{k=0}^{y-1} 3^{y-1-k} * 2^{S_k}, computed in pure
    Python bigint arithmetic. No modular reduction; no overflow possible."""
    y = len(period)
    S = [0]
    for a in period:
        S.append(S[-1] + a)
    return sum(3 ** (y - 1 - k) * 2 ** S[k] for k in range(y))


def compositions(x, y):
    """All compositions of x into y parts >= 1, via (y-1)-subset cuts."""
    for cuts in combinations(range(1, x), y - 1):
        prev = 0
        comp = []
        for c in cuts:
            comp.append(c - prev)
            prev = c
        comp.append(x - prev)
        yield tuple(comp)


def main():
    x, y = 27, 17
    diff = 2 ** x - 3 ** y
    expected_n = comb(x - 1, y - 1)

    print(f"=== Independent verification: (x={x}, y={y}) ===")
    print()
    print(f"  diff = 2^{x} - 3^{y} = {diff:,}")
    print(f"  expected |Sigma| = C({x-1}, {y-1}) = {expected_n:,}")
    print(f"  Crandall expectation E_Cr = {expected_n / diff:.4f}")
    print()
    print(f"  Trivial cycle case (x = 2y)? {x == 2*y}  -> "
          f"{'no trivial zero possible here' if x != 2*y else 'trivial zero expected'}")
    print()
    print(f"Enumerating with pure-Python bigint arithmetic...")

    start = time.time()
    n_total = 0
    n_zero = 0
    nontriv_examples = []

    for sigma in compositions(x, y):
        C = cycle_value_exact(sigma)
        n_total += 1
        if C % diff == 0:
            # In bigint we can also report the actual C and its quotient
            n_zero += 1
            trivial = all(a == 2 for a in sigma)
            if not trivial:
                nontriv_examples.append((sigma, C, C // diff))

    elapsed = time.time() - start

    print()
    print(f"  total compositions    : {n_total:,}")
    print(f"  matches expected |Σ|  : {'YES' if n_total == expected_n else 'NO -- BUG'}")
    print(f"  zeros mod diff        : {n_zero}")
    print(f"  non-trivial zeros     : {len(nontriv_examples)}")
    print(f"  elapsed               : {elapsed:.1f} s")
    print()

    if len(nontriv_examples) == 0:
        print("  RESULT: consistent with Conjecture 1 (mutual exclusion holds)")
    else:
        print(f"  RESULT: CONJECTURE 1 FALSIFIED for (x, y) = ({x}, {y})")
        for sigma, C, n0 in nontriv_examples[:5]:
            print(f"    sigma = {list(sigma)}")
            print(f"    C(y, sigma) = {C}")
            print(f"    n_0 = C / diff = {n0}")

    # Cross-check vs C binary if available
    print()
    print("  (To cross-check this result against the C implementation, run:")
    print("     gcc -O3 -o enumerate src/enumerate_compositions.c")
    print(f"     ./enumerate {x} {y}")
    print("   The 'Non-trivial zeros' line should match.)")


if __name__ == "__main__":
    main()
