# How to publish this repository on GitHub

## Quick steps

1. **Create a new empty repository on GitHub** (via web): go to https://github.com/new
   - Repository name: `collatz-mutual-exclusion`
   - Description: "Empirical study of mutual exclusion of local divisibility constraints in the Collatz cycle equation"
   - Public
   - Do NOT initialize with README, .gitignore, or LICENSE (we already have them)

2. **From your local machine**, after downloading the contents of this folder:

   ```bash
   cd path/to/collatz-mutual-exclusion
   git init
   git add .
   git commit -m "Initial commit: empirical observations and conjecture"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/collatz-mutual-exclusion.git
   git push -u origin main
   ```

   (Replace `YOUR_USERNAME` with your GitHub username.)

3. **Update the URL in the README and paper:**

   In `README.md` line:
   ```
   url    = {https://github.com/<USER>/collatz-mutual-exclusion}
   ```
   replace `<USER>` with your GitHub username.

   In `paper/preprint.tex`, same substitution. Then recompile:
   ```bash
   cd paper && pdflatex preprint.tex
   ```

4. **For Zenodo deposit (optional):**
   - Connect GitHub to Zenodo: https://zenodo.org/account/settings/github/
   - Toggle the repo `collatz-mutual-exclusion` ON.
   - Create a release on GitHub (Releases > Draft a new release > tag `v0.1`).
   - Zenodo will mint a DOI automatically.

## File checklist

```
collatz-mutual-exclusion/
├── README.md                       project description
├── LICENSE                         MIT
├── HOW_TO_PUBLISH.md              this file
├── reproduce_all.sh               full reproduction script
├── paper/
│   ├── preprint.tex               LaTeX source
│   └── preprint.pdf               compiled
├── src/
│   ├── enumerate_compositions.c   fast C enumerator
│   ├── verify_recurrence.py       Python verifier
│   ├── mutual_exclusion.py        marginal-vs-joint analysis
│   └── adversarial_battery.py     adversarial test battery
├── data/
│   └── results_summary.csv        full results table
└── results/                       (run reproduce_all.sh to populate)
```

## Reproducibility check

After cloning a fresh copy, running `./reproduce_all.sh` should regenerate all
the numerical claims of the preprint. Expected total runtime: ~5 minutes.
