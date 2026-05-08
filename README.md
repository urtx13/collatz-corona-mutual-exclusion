# Local Divisibility and Mutual Exclusion in the Collatz Corona

This repository accompanies the working research note:

**Local Divisibility and Mutual Exclusion in the Collatz Corona: A Research Note**  
Oriol Corcoll Arias, May 2026.

This repository contains code, data, logs, and a LaTeX preprint reporting finite exhaustive computations concerning local divisibility in the **Collatz corona**. It does **not** prove the Collatz conjecture or the absence of non-trivial Collatz cycles.

## Summary

The Collatz corona, in the terminology of Belaga--Mignotte, is the finite set of cycle coefficients

$begin:math:display$
\\mathcal\{C\}\(x\,y\)\=\\\{C\(y\,\\vec\{\\sigma\}\)\:\\vec\{\\sigma\}\\in\\Sigma\(x\,y\)\\\}\,
$end:math:display$

where

$begin:math:display$
C\(y\,\\vec\{\\sigma\}\)\=\\sum\_\{k\=0\}\^\{y\-1\}3\^\{y\-1\-k\}2\^\{\\sigma\_k\}\.
$end:math:display$

The computational question studied here is whether this corona contains a multiple of its associated Collatz number

$begin:math:display$
2\^x\-3\^y\.
$end:math:display$

Across 22 tested parameter pairs and 1,769,706,522 exhaustively enumerated admissible patterns outside the trivial diagonal, no non-trivial zero residue was found for

$begin:math:display$
C\(y\,\\vec\{\\sigma\}\)\\equiv 0 \\pmod\{2\^x\-3\^y\}\.
$end:math:display$

A naive Crandall-type uniformity benchmark predicts approximately 7.21 non-trivial zero residues over the tested rows. This is used only as a nominal benchmark, not as a rigorous probability model.

The central local-divisibility example is $begin:math:text$\(x\,y\)\=\(24\,15\)$end:math:text$, where

$begin:math:display$
2\^\{24\}\-3\^\{15\}\=13\\cdot 186793\.
$end:math:display$

Divisibility by each factor occurs separately on the corona, but not simultaneously on the same admissible pattern:

- $begin:math:text$\|A\_\{13\}\| \= 62\,775$end:math:text$
- $begin:math:text$\|A\_\{186793\}\| \= 50$end:math:text$
- $begin:math:text$\|A\_\{13\}\\cap A\_\{186793\}\| \= 0$end:math:text$

where

$begin:math:display$
A\_q\=\\\{\\vec\{\\sigma\}\\in\\Sigma\(24\,15\)\:q\\mid C\(15\,\\vec\{\\sigma\}\)\\\}\.
$end:math:display$

A naive local-independence benchmark would predict

$begin:math:display$
\\frac\{\|A\_\{13\}\|\\\,\|A\_\{186793\}\|\}\{\|\\Sigma\(24\,15\)\|\}\\approx 3\.8409
$end:math:display$

simultaneous occurrences.

Across five tested squarefree composite cases, the aggregate naive local-independence benchmark is approximately 8.86 simultaneous local hits; observed: 0.

These observations motivate a restricted zero-avoidance conjecture for the Collatz corona. The note is computational and conjectural; it is not a proof.

## Repository structure

```text
.
├── README.md
├── LICENSE
├── HOW_TO_PUBLISH.md
├── reproduce_all.sh
├── paper/
│   ├── preprint.tex
│   └── preprint.pdf
├── src/
│   ├── enumerate_compositions.c
│   ├── mutual_exclusion.py
│   └── verify_27_17.py
├── data/
│   ├── results_summary.csv
│   └── mutual_exclusion_24_15.csv
└── results/
    └── log_runs.txt
```

## Quick start

Compile the C enumerator:

```bash
gcc -O3 -o enumerate_compositions src/enumerate_compositions.c
```

Run selected cases:

```bash
./enumerate_compositions 27 17
./enumerate_compositions 35 22
```

Expected output for these non-trivial cases:

```text
Non-trivial zeros: 0
```

Run the local mutual-exclusion analysis:

```bash
python3 src/mutual_exclusion.py
```

Expected output includes:

```text
|A_13| = 62775
|A_186793| = 50
|A_13 ∩ A_186793| = 0
independence prediction ≈ 3.8409
```

Run the independent Python verification of the critical case $begin:math:text$\(x\,y\)\=\(27\,17\)$end:math:text$:

```bash
python3 src/verify_27_17.py
```

## Main data files

The main summary table is:

```text
data/results_summary.csv
```

Raw logs of larger runs are in:

```text
results/log_runs.txt
```

The local-divisibility data for the central case $begin:math:text$\(x\,y\)\=\(24\,15\)$end:math:text$ are in:

```text
data/mutual_exclusion_24_15.csv
```

## Main verified examples

| $begin:math:text$\(y\,x\)$end:math:text$ | $begin:math:text$\|\\Sigma\|$end:math:text$ | $begin:math:text$2\^x\-3\^y$end:math:text$ | $begin:math:text$E\_\{\\mathrm\{Cr\}\}$end:math:text$ | non-triv. zeros |
|---:|---:|---:|---:|---:|
| (5, 8) | 35 | 13 | 2.692 | 0 |
| (10, 16) | 5,005 | 6,487 | 0.772 | 0 |
| (17, 27) | 5,311,735 | 5,077,565 | 1.046 | 0 |
| (22, 35) | 927,983,760 | 2,978,678,759 | 0.312 | 0 |

The full 22-row table is provided in `data/results_summary.csv`.

## Conjecture

For every $begin:math:text$\(x\,y\)\\in\\mathbb\{N\}\^2$end:math:text$ with $begin:math:text$2\^x\>3\^y$end:math:text$ and $begin:math:text$\(x\,y\)\\ne\(2y\,y\)$end:math:text$,

$begin:math:display$
\\\{C\(y\,\\vec\{\\sigma\}\)\:\\vec\{\\sigma\}\\in\\Sigma\(x\,y\)\\\}
\\cap
\(2\^x\-3\^y\)\\mathbb\{Z\}
\=
\\emptyset\.
$end:math:display$

Equivalently, outside the trivial diagonal, the Collatz corona does not contain a multiple of its corresponding Collatz number.

This conjecture is equivalent to the non-existence of non-trivial accelerated Collatz cycles. It does not address divergent orbits.

## Relation to prior work

- **Böhm--Sontacchi** and **Lagarias**: classical cycle-equation formulation.
- **Belaga--Mignotte**: Collatz number / Collatz corona framework; the object studied here is theirs.
- **Crandall**: heuristic benchmark used here only nominally.
- **Steiner**, **Eliahou**, **Simons--de Weger**, **Simons**, **Hercher**: cycle-length bounds and generalized Syracuse settings.
- **Dhiman--Pandey**: non-Presburger-definability of the unrestricted divisibility predicate.

To the author's knowledge, the explicit local mutual-exclusion observation recorded here has not been isolated in the literature checked so far. The literature survey is preliminary, and any precedent will be acknowledged in later versions.

## Limitations

1. The computations are exhaustive only for the listed parameter pairs.
2. The local mutual-exclusion mechanism is explicitly checked in five squarefree composite cases.
3. The Poisson and independence calculations are nominal benchmarks, not rigorous probability models.
4. The conjecture concerns only the cyclic component of Collatz.
5. The literature survey is preliminary.

## License

MIT. See `LICENSE`.

## Citation

```bibtex
@misc{corcoll2026collatzcorona,
  author = {Corcoll Arias, Oriol},
  title  = {Local Divisibility and Mutual Exclusion in the Collatz Corona: A Research Note},
  year   = {2026},
  note   = {Working draft / computational research note},
  url    = {https://github.com/urtx13/collatz-corona-mutual-exclusion}
}
```