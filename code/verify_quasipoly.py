"""Fit the period-6 cubic quasi-polynomial for D_SP(n) and verify it."""

import sys
from fractions import Fraction


NMAX = 42  # brute-force range


def D_SP(n):
    """Count integer single-peaked profiles (x1, x2, x3, x4) with sum = n
    where Plurality and Borda each have a unique winner and the winners
    differ.  Brute force directly from the definition.
    """
    cnt = 0
    for x1 in range(n + 1):
        for x2 in range(n + 1 - x1):
            for x3 in range(n + 1 - x1 - x2):
                x4 = n - x1 - x2 - x3
                pa, pb, pc = x1, x3 + x4, x2
                pmax = max(pa, pb, pc)
                pwins = [c for c, v in (('A', pa), ('B', pb), ('C', pc))
                         if v == pmax]
                if len(pwins) != 1:
                    continue
                pw = pwins[0]
                ba = 2 * x1 + x3
                bb = x1 + x2 + 2 * x3 + 2 * x4
                bc = 2 * x2 + x4
                bmax = max(ba, bb, bc)
                bwins = [c for c, v in (('A', ba), ('B', bb), ('C', bc))
                         if v == bmax]
                if len(bwins) != 1:
                    continue
                bw = bwins[0]
                if pw != bw:
                    cnt += 1
    return cnt


def vandermonde_solve(xs, ys):
    """Exact rational Vandermonde solver.  Given d+1 points
    (xs[i], ys[i]) returns [a_0, ..., a_d] such that
    sum_j a_j * xs[i]^j = ys[i] for every i.
    """
    n = len(xs)
    A = [[Fraction(x) ** j for j in range(n)] for x in xs]
    b = [Fraction(y) for y in ys]
    for c in range(n):
        piv = None
        for r in range(c, n):
            if A[r][c] != 0:
                piv = r
                break
        if piv is None:
            raise ValueError("singular Vandermonde system")
        A[c], A[piv] = A[piv], A[c]
        b[c], b[piv] = b[piv], b[c]
        # Normalize pivot row.
        inv = Fraction(1) / A[c][c]
        A[c] = [v * inv for v in A[c]]
        b[c] = b[c] * inv
        # Eliminate column c in every other row.
        for r in range(n):
            if r == c or A[r][c] == 0:
                continue
            factor = A[r][c]
            A[r] = [A[r][k] - factor * A[c][k] for k in range(n)]
            b[r] = b[r] - factor * b[c]
    return b


# Published target coefficients (c_1, c_0) per residue.
TARGET = {
    0: (Fraction(-5, 6),    Fraction(2, 1)),
    1: (Fraction(-1, 3),    Fraction(29, 108)),
    2: (Fraction(-19, 18),  Fraction(46, 27)),
    3: (Fraction(-1, 3),    Fraction(-1, 4)),
    4: (Fraction(-5, 6),    Fraction(68, 27)),
    5: (Fraction(-5, 9),    Fraction(-59, 108)),
}

A3 = Fraction(1, 27)   # leading coefficient (residue-independent)
A2 = Fraction(1, 36)   # quadratic coefficient (residue-independent)


def main():
    print(f"Brute-forcing D_SP(n) for n = 0..{NMAX} ...")
    DSP = [D_SP(n) for n in range(NMAX + 1)]
    print(f"  D_SP[0..14] = {DSP[:15]}")

    fits = {}
    failures = []

    print("\nFitted period-6 cubic per residue class (n >= 1):")
    print(f"  {'r':>2} | {'a_3':>6} {'a_2':>6} {'c_1':>10} {'c_0':>12}    sample n's")
    for r in range(6):
        ns = [n for n in range(1, NMAX + 1) if n % 6 == r][:4]
        if len(ns) < 4:
            failures.append(f"r={r}: only {len(ns)} sample(s) available; "
                            f"need at least 4")
            continue
        ys = [DSP[n] for n in ns]
        a0, a1, a2, a3 = vandermonde_solve(ns, ys)
        fits[r] = (a0, a1, a2, a3)
        print(f"  {r:>2} | {str(a3):>6} {str(a2):>6} "
              f"{str(a1):>10} {str(a0):>12}    {ns}")
        if a3 != A3:
            failures.append(f"r={r}: a_3 = {a3} != 1/27")
        if a2 != A2:
            failures.append(f"r={r}: a_2 = {a2} != 1/36")
        c1_target, c0_target = TARGET[r]
        if a1 != c1_target:
            failures.append(f"r={r}: c_1 = {a1} != {c1_target}")
        if a0 != c0_target:
            failures.append(f"r={r}: c_0 = {a0} != {c0_target}")

    def formula(n):
        a0, a1, a2, a3 = fits[n % 6]
        return a3 * n ** 3 + a2 * n ** 2 + a1 * n + a0

    mismatches = []
    if not failures:  # only meaningful if all fits succeeded
        for n in range(1, NMAX + 1):
            f = formula(n)
            if f != Fraction(DSP[n]):
                mismatches.append((n, DSP[n], f))
        if mismatches:
            failures.append(
                "formula disagrees with brute force at "
                f"{[m[0] for m in mismatches[:5]]}"
            )


    f0 = formula(0) if not failures else None
    print(f"\nn = 0 sanity check:")
    print(f"  D_SP(0) (brute force) = {DSP[0]}")
    if f0 is not None:
        print(f"  formula(0)            = {f0}")
        print(f"  gap = formula(0) - D_SP(0) = {f0 - DSP[0]}")
        print( "  (Expected gap of 2 from the polynomial part of F_SP(t).)")
        if DSP[0] != 0:
            failures.append(f"expected D_SP(0) = 0, got {DSP[0]}")
        if f0 != Fraction(2):
            failures.append(f"expected formula(0) = 2, got {f0}")

    if failures:
        print("\nFAIL:")
        for f in failures:
            print("  - " + f)
        sys.exit(1)

    print(f"\nFormula matches brute force at every n in [1, {NMAX}].")
    print("All published quasi-polynomial coefficients confirmed.")
    print("\nPASS")
    sys.exit(0)


if __name__ == "__main__":
    main()
