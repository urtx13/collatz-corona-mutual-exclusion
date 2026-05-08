"""
mutual_exclusion.py

Marginal-vs-joint analysis of divisibility events for prime power factors of
2^x - 3^y, applied to the cycle constants C(y, sigma) = sum_{k=0}^{y-1}
3^{y-1-k} 2^{S_k} as sigma ranges over admissible compositions.

Verifies the empirical observations of the preprint (Section 2):

  - Featured case (x, y) = (24, 15):
        2^x - 3^y = 2,428,309 = 13 * 186,793
        |A_13|             = 62,775
        |A_186793|         = 50
        |A_13 cap A_186793| = 0
        independence prediction = 3.8409

  - Aggregate over 5 composite-diff cases (15,9), (16,10), (20,12), (24,15),
    (26,16): independence prediction sums to 8.86, observed joint = 0.

The script handles prime powers p^e correctly: for each prime power factor
of 2^x - 3^y, it counts compositions sigma with C(y, sigma) ≡ 0 mod p^e
(not just mod p).

Output:
  - Console table replicating Table 2 of the preprint.
  - CSV at data/mutual_exclusion_24_15.csv with per-factor breakdown
    of the featured case.

Author: Oriol Corcoll Arias, 2026
License: MIT
"""

import os
import csv
from itertools import combinations
from sympy import factorint


def cycle_value(period):
    """C(y, sigma) for sigma = (a_1, ..., a_y) given as `period`."""
    y = len(period)
    S = [0]
    for a in period:
        S.append(S[-1] + a)
    return sum(3 ** (y - 1 - k) * 2 ** S[k] for k in range(y))


def compositions(x, y):
    """All compositions of x into y parts >= 1, via L-1 cuts in [1, x-1]."""
    for cuts in combinations(range(1, x), y - 1):
        prev = 0
        comp = []
        for c in cuts:
            comp.append(c - prev)
            prev = c
        comp.append(x - prev)
        yield tuple(comp)


def analyze_pair(x, y, max_n=10**8):
    """
    For (x, y) with 2^x > 3^y, enumerate all compositions and count
      n_total       = total compositions
      n_zero[q]     = #{sigma : q | C(y, sigma)}    for each prime-power factor q of diff
      n_zero_diff   = #{sigma : diff | C(y, sigma)}

    Independence prediction (under Crandall + CRT independence):
      indep_pred = n_total * prod_q (n_zero[q] / n_total)

    Crandall prediction (assumes uniform mod diff):
      crandall_pred = n_total / diff
    """
    diff = 2 ** x - 3 ** y
    if diff <= 0:
        return None

    # Factorize. Treat each p^e as a single factor (via CRT, the factors
    # p_i^{e_i} are pairwise coprime, so the joint event is well-defined.)
    fact = factorint(diff)
    prime_powers = sorted(p ** e for p, e in fact.items())

    n_total = 0
    n_zero_q = {q: 0 for q in prime_powers}
    n_zero_diff = 0

    for comp in compositions(x, y):
        n_total += 1
        if n_total > max_n:
            return None  # too large
        C = cycle_value(comp)
        for q in prime_powers:
            if C % q == 0:
                n_zero_q[q] += 1
        if C % diff == 0:
            n_zero_diff += 1

    indep_pred = n_total
    for q in prime_powers:
        indep_pred *= n_zero_q[q] / n_total

    crandall_pred = n_total / diff

    return {
        "x": x,
        "y": y,
        "diff": diff,
        "factorization": dict(fact),
        "prime_powers": prime_powers,
        "n_total": n_total,
        "n_zero_q": dict(n_zero_q),
        "n_zero_diff": n_zero_diff,
        "indep_pred": indep_pred,
        "crandall_pred": crandall_pred,
    }


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

# The 5 composite-diff cases highlighted in the preprint
CASES = [(15, 9), (16, 10), (20, 12), (24, 15), (26, 16)]


def main():
    print("=" * 86)
    print("Mutual exclusion analysis: 5 composite-diff cases")
    print("=" * 86)
    print()

    header = (
        f"{'(x,y)':>8} | {'diff':>10} | {'factors (p^e)':>22} | "
        f"{'|Sigma|':>10} | {'observed':>8} | {'indep_pred':>10} | {'crandall':>9}"
    )
    print(header)
    print("-" * len(header))

    total_indep = 0.0
    total_obs = 0
    total_n = 0

    for x, y in CASES:
        r = analyze_pair(x, y)
        if r is None:
            print(f"  ({x:>2},{y:>2}): SKIPPED (too large or invalid)")
            continue
        fstr = ", ".join(f"{p}^{e}" if e > 1 else str(p)
                         for p, e in sorted(r["factorization"].items()))
        if len(fstr) > 20:
            fstr = fstr[:18] + ".."
        print(
            f"  ({x:>2},{y:>2}) | {r['diff']:>10} | {fstr:>22} | "
            f"{r['n_total']:>10} | {r['n_zero_diff']:>8} | "
            f"{r['indep_pred']:>10.4f} | {r['crandall_pred']:>9.4f}"
        )
        total_indep += r["indep_pred"]
        total_obs += r["n_zero_diff"]
        total_n += r["n_total"]

    print()
    print(f"Aggregate over the 5 cases:")
    print(f"  total compositions enumerated   : {total_n:,}")
    print(f"  observed joint zeros (= cycles) : {total_obs}")
    print(f"  sum of independence predictions : {total_indep:.4f}")
    import math
    p_value = math.exp(-total_indep) if total_indep > 0 else 1.0
    print(f"  Poisson p-value (lambda=indep)  : {p_value:.6f}")
    print()

    # ---------------------------------------------------------------------
    # Featured case: (24, 15) with detailed CSV output
    # ---------------------------------------------------------------------
    print("=" * 86)
    print("Featured case (x=24, y=15): per-factor detail")
    print("=" * 86)
    r = analyze_pair(24, 15)
    print(f"  diff = 2^24 - 3^15 = {r['diff']}")
    print(f"  factorization      = {r['factorization']}")
    print(f"  |Sigma|            = {r['n_total']}")
    print()
    print(f"  {'prime power q':>15} | {'|A_q|':>10} | {'rate':>10} | {'expected (n/q)':>14}")
    print("  " + "-" * 60)
    for q in r["prime_powers"]:
        rate = r["n_zero_q"][q] / r["n_total"]
        expected = r["n_total"] / q
        print(f"  {q:>15} | {r['n_zero_q'][q]:>10} | {rate:>10.6f} | {expected:>14.4f}")
    print()
    print(f"  joint observed |A_13 cap A_186793| = {r['n_zero_diff']}")
    print(f"  independence prediction = "
          f"{' * '.join(f'({r['n_zero_q'][q]}/{r['n_total']})' for q in r['prime_powers'])} "
          f"* {r['n_total']} = {r['indep_pred']:.4f}")
    print()

    # Write CSV
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_dir = os.path.join(repo_root, "data")
    os.makedirs(csv_dir, exist_ok=True)
    csv_path = os.path.join(csv_dir, "mutual_exclusion_24_15.csv")
    with open(csv_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["x", "y", "diff", "p_or_factor", "count", "rate"])
        for q in r["prime_powers"]:
            w.writerow([
                r["x"], r["y"], r["diff"], q,
                r["n_zero_q"][q],
                f"{r['n_zero_q'][q] / r['n_total']:.8f}",
            ])
        w.writerow([r["x"], r["y"], r["diff"], "intersection (= diff)",
                    r["n_zero_diff"],
                    f"{r['n_zero_diff'] / r['n_total']:.8f}"])
        w.writerow([r["x"], r["y"], r["diff"], "n_total", r["n_total"], 1.0])
        w.writerow([r["x"], r["y"], r["diff"], "indep_pred", "",
                    f"{r['indep_pred']:.6f}"])
    print(f"  Wrote {csv_path}")


if __name__ == "__main__":
    main()
