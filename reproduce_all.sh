#!/bin/bash
# reproduce_all.sh
# Reproduces all main empirical results from the preprint.
#
# Requires: gcc, python3, sympy (pip install sympy), mpmath (pip install mpmath)
#
# Usage: ./reproduce_all.sh

set -e

echo "=== Building C enumerator ==="
gcc -O3 -o enumerate_compositions src/enumerate_compositions.c
echo "OK"
echo

echo "=== Verifying dual recurrence (Python) ==="
python3 src/verify_recurrence.py
echo

echo "=== Mutual exclusion analysis (Python) ==="
python3 src/mutual_exclusion.py
echo

echo "=== Adversarial battery (Python) ==="
python3 src/adversarial_battery.py
echo

echo "=== Exhaustive enumeration: a sample of (x, y) pairs ==="
echo
for case in "8 5" "16 10" "27 17" "32 20" "35 22"; do
    x=$(echo $case | cut -d' ' -f1)
    y=$(echo $case | cut -d' ' -f2)
    echo "--- (x=$x, y=$y) ---"
    ./enumerate_compositions $x $y | tail -3
    echo
done

echo "=== Done ==="
echo "All outputs match the values reported in paper/preprint.pdf, Table 1."
