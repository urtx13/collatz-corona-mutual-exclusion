/*
 * enumerate_compositions.c
 *
 * Exhaustive enumeration of compositions of x into y parts >= 1.
 * For each composition sigma = (a_1, ..., a_y) with sum a_k = x:
 *
 *     C(y, sigma) = sum_{k=0}^{y-1} 3^{y-1-k} * 2^{S_k}
 *
 * where S_k = a_1 + ... + a_k (partial sums starting at S_0 = 0).
 *
 * Output: count of compositions sigma with C(y, sigma) ≡ 0 (mod 2^x - 3^y),
 * marking non-trivial zeros (those with sigma != (2,2,...,2) at x = 2y).
 *
 * Throughput: ~10^7 compositions/sec on a single core (uint64 mode).
 * Constraint: requires 2^x - 3^y < 2^62 for uint64 mode.
 *
 * Build:   gcc -O3 -o enumerate_compositions enumerate_compositions.c
 * Usage:   ./enumerate_compositions <x> <y>
 *
 * Author: Oriol Corcoll Arias, 2026
 * License: MIT
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <time.h>

static uint64_t pow2_mod[256];
static uint64_t pow3_mod[256];
static uint64_t diff;

static uint64_t compute_C_mod(int *period, int y) {
    uint64_t result = 0;
    int S_acc = 0;
    for (int j = 0; j < y; j++) {
        __uint128_t term = (__uint128_t)pow3_mod[y - 1 - j] * pow2_mod[S_acc];
        term %= diff;
        result += (uint64_t)term;
        if (result >= diff) result -= diff;
        S_acc += period[j];
    }
    return result;
}

static int next_combination(int *cuts, int y, int x) {
    int i = y - 2;
    while (i >= 0 && cuts[i] == x - 1 - (y - 2 - i)) i--;
    if (i < 0) return 0;
    cuts[i]++;
    for (int j = i + 1; j < y - 1; j++) cuts[j] = cuts[j - 1] + 1;
    return 1;
}

int main(int argc, char **argv) {
    if (argc < 3) {
        fprintf(stderr, "Usage: %s <x> <y>\n", argv[0]);
        return 1;
    }
    int x = atoi(argv[1]);
    int y = atoi(argv[2]);

    if (x < 1 || y < 1 || x > 200 || y > 200) {
        fprintf(stderr, "Out of range: 1 <= x, y <= 200\n");
        return 1;
    }
    if (y > x) {
        fprintf(stderr, "Need y <= x\n");
        return 1;
    }

    // Compute 2^x and 3^y as 128-bit, check that diff fits in uint64
    __uint128_t two_x = 1;
    for (int i = 0; i < x; i++) two_x *= 2;
    __uint128_t three_y = 1;
    for (int i = 0; i < y; i++) three_y *= 3;

    if (two_x <= three_y) {
        fprintf(stderr, "2^x <= 3^y; not a candidate for positive cycle\n");
        return 1;
    }
    __uint128_t d128 = two_x - three_y;
    if (d128 >= ((__uint128_t)1 << 62)) {
        fprintf(stderr, "2^x - 3^y too large for uint64 mode (>= 2^62)\n");
        return 1;
    }
    diff = (uint64_t)d128;

    printf("(x=%d, y=%d): 2^x - 3^y = %llu\n", x, y, (unsigned long long)diff);

    // Precompute powers mod diff
    uint64_t p2 = 1;
    for (int i = 0; i <= x; i++) {
        pow2_mod[i] = p2;
        p2 = (p2 * 2) % diff;
    }
    uint64_t p3 = 1;
    for (int i = 0; i < y; i++) {
        pow3_mod[i] = p3;
        p3 = (p3 * 3) % diff;
    }

    int *cuts = malloc((y - 1) * sizeof(int));
    int *period = malloc(y * sizeof(int));
    if (!cuts || !period) { perror("malloc"); return 1; }
    for (int i = 0; i < y - 1; i++) cuts[i] = i + 1;

    long long count = 0, zeros = 0, nontrivial = 0;
    time_t start = time(NULL);

    do {
        int prev = 0;
        for (int i = 0; i < y - 1; i++) { period[i] = cuts[i] - prev; prev = cuts[i]; }
        period[y - 1] = x - prev;

        uint64_t C = compute_C_mod(period, y);
        if (C == 0) {
            zeros++;
            int trivial = 1;
            for (int i = 0; i < y; i++) if (period[i] != 2) { trivial = 0; break; }
            if (!trivial) {
                nontrivial++;
                printf("NON-TRIVIAL ZERO: ");
                for (int i = 0; i < y; i++) printf("%d ", period[i]);
                printf("\n");
            }
        }
        count++;
        if (count % 100000000 == 0) {
            time_t now = time(NULL);
            double rate = count / (double)(now - start + 1);
            printf("  %lld iter, %lld zeros, rate=%.0f/s, elapsed=%lds\n",
                   count, zeros, rate, (long)(now - start));
            fflush(stdout);
        }
    } while (next_combination(cuts, y, x));

    time_t end = time(NULL);
    printf("\nFINAL: %lld compositions in %lds\n", count, (long)(end - start));
    printf("Zeros total: %lld\n", zeros);
    printf("Non-trivial zeros: %lld %s\n", nontrivial,
           nontrivial == 0 ? "(consistent with conjecture)" : "(CONJECTURE FALSIFIED!)");

    free(cuts);
    free(period);
    return 0;
}
