# Collatz Cycle Equation: Mutual Exclusion of Local Divisibilities

Computational evidence and a conjecture concerning the cyclic component of the Collatz problem.

## Summary

This repository contains the code, data, and preprint accompanying an empirical study of the **Collatz corona** (Belaga-Mignotte 1998) and its intersection with multiples of the corresponding **Collatz number** $2^x - 3^y$.

For all 22 admissible parity patterns $(x, y)$ with $2^x > 3^y$ and total composition count $\sum |\Sigma| \approx 1.77 \times 10^9$ exhaustively enumerated, the only patterns producing $C(y, \vec\sigma) \equiv 0 \pmod{2^x - 3^y}$ correspond to the trivial cycle $a_i = 2$ at $x = 2y$.

The Crandall heuristic (1978) predicts an aggregate of $\sim 7.21$ non-trivial cycle solutions across this sample; observed: $0$ ($p \approx 7 \times 10^{-4}$).

The deviation is explained structurally by **mutual exclusion** between local divisibility events: when $2^x - 3^y$ has multiple prime factors, the marginal events $\{p_i \mid C\}$ each occur at their expected Crandall rate, but their joint occurrence is empirically empty.

## Author

Oriol Corcoll Arias (working draft, May 2026)

## Repository structure

```
.
├── README.md                  this file
├── LICENSE                    MIT license
├── paper/
│   ├── preprint.tex           LaTeX source
│   └── preprint.pdf           compiled preprint (3 pages)
├── src/
│   ├── enumerate_compositions.c   fast C enumerator (uint64, ~10^7 patterns/s)
│   ├── verify_recurrence.py       Python verifier of the dual recurrence
│   ├── mutual_exclusion.py        marginal-vs-joint analysis
│   └── adversarial_battery.py     test suite for the conjecture (Sturmian etc.)
├── data/
│   └── results_summary.csv    table of all (x, y) pairs enumerated
└── results/
    └── log_runs.txt           raw output of enumeration runs
```

## Quick start

### Reproduce the main empirical table

```bash
gcc -O3 -o enumerate src/enumerate_compositions.c
./enumerate 27 17        # ~6 seconds
./enumerate 35 22        # ~80 seconds
```

Expected output: `Zeros: 0 (non-trivial: none)` for all `(x, y)` with `x != 2y`.

### Verify the dual 3-adic recurrence

```bash
python3 src/verify_recurrence.py
```

This computes $R_k(\vec\sigma) \equiv 2^{-S_k}\sum_{j=0}^{k-1} 3^{k-1-j} 2^{S_j} \pmod{3^k}$ via the recurrence $R_{k+1} \equiv 2^{-a_{k+1}}(3 R_k + 1) \pmod{3^{k+1}}$ and verifies the formula identity.

### Reproduce the mutual exclusion observation at (24, 15)

```bash
python3 src/mutual_exclusion.py
```

Outputs $|A_{13}|$, $|A_{186793}|$, $|A_{13} \cap A_{186793}|$ and the independence prediction.

## Main observations

| $(y, x)$ | $|\Sigma|$ | $2^x - 3^y$ | $E_{\text{Crandall}}$ | non-triv. zeros |
|---:|---:|---:|---:|---:|
| (5, 8) | 35 | 13 | 2.69 | 0 |
| (10, 16) | 5,005 | 6,487 | 0.77 | 0 |
| (17, 27) | 5,311,735 | 5,077,565 | 1.05 | 0 |
| (22, 35) | 927,983,760 | 2,978,678,759 | 0.31 | 0 |
| **aggregate (22 pairs)** | **1.77 × 10⁹** | — | **7.21** | **0** |

**Mutual exclusion** at $(y, x) = (15, 24)$, $2^x - 3^y = 13 \cdot 186793$:
- $|A_{13}| = 62{,}775$ (rate $0.0768$, marginal expected $\approx 0.077$)
- $|A_{186793}| = 50$ (rate $6.1 \cdot 10^{-5}$, marginal expected $\approx 5.4 \cdot 10^{-6}$)
- Independence prediction: $|A_{13}| \cdot |A_{186793}| / |\Sigma| \approx 3.84$
- **Observed**: $|A_{13} \cap A_{186793}| = 0$

## Conjecture

For every $(x, y) \in \mathbb{N}^2$ with $2^x > 3^y$ and $(x, y) \ne (2y, y)$:
$$\bigl\{C(y, \vec\sigma) : \vec\sigma \in \Sigma(x, y)\bigr\} \cap (2^x - 3^y) \mathbb{Z} = \emptyset.$$

If true, this implies non-existence of non-trivial Collatz cycles by purely structural means.

## Relation to prior work

- **Belaga, Mignotte** (1998): introduced the *Collatz number* $2^j - 3^k$ and the *Collatz corona*; the object studied here is theirs.
- **Belaga** (2003): polynomial upper bound on the *number* of $(3x+d)$-cycles of given odd-length. Different result: bounds, not emptiness.
- **Belaga, Mignotte** (2006): exhaustive enumeration of primitive cycles for $1 \le d \le 19{,}999$. Enumerate cycles, not full coronas.
- **Steiner** (1977), **Simons–de Weger** (2005), **Simons** (2008), **Hercher** (2018, 2022): lower bounds on cycle length via Baker–Wüstholz / Laurent linear forms in logarithms (current: $m \ge 92$ local minima).
- **Dhiman, Pandey** (arXiv:2601.12772, January 2026): the divisibility predicate $\mathcal{D}_y$ is not Presburger-definable.

To the author's knowledge, the explicit *mutual exclusion* observation between distinct prime factors of $2^x - 3^y$, and the resulting conjecture on emptiness of the corona modulo its Collatz number for $d = 1$, are not stated in this prior literature. Any precedent will be acknowledged in subsequent versions.

## Limitations

1. Enumeration is bounded by $|\Sigma| \le 10^9$ on a single machine. The convergent pair $(x, y) = (485, 306)$ of $\log_2 3$, where $|\Sigma| \approx 10^{140}$, is computationally inaccessible.
2. The mutual exclusion mechanism is verified explicitly only at $(24, 15)$; verification across more composite-diff cases is the next step.
3. The conjecture concerns only the cyclic component of Collatz. The divergent component is independent and unaffected.
4. The independence-of-cases assumption underlying our Poisson p-values is an approximation.

## License

MIT. See `LICENSE`.

## Citation

```bibtex
@misc{corcoll2026mutual,
  author = {Oriol Corcoll Arias},
  title  = {Mutual Exclusion of Local Divisibility Constraints in the Collatz Cycle Equation},
  year   = {2026},
  note   = {Working draft},
  url    = {https://github.com/<USER>/collatz-mutual-exclusion}
}
```
