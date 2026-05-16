"""Compute closed-chamber vertices and verify denominator bound 6."""

import sys
import math
from fractions import Fraction
from itertools import combinations


# Each entry is (label, (a1, a2, a3, a4)) encoding the inequality
#   a1*X1 + a2*X2 + a3*X3 + a4*X4 >= 0.
INEQS = [
    ("X1 >= 0",                  (1,  0,  0,  0)),
    ("X2 >= 0",                  (0,  1,  0,  0)),
    ("X3 >= 0",                  (0,  0,  1,  0)),
    ("X4 >= 0",                  (0,  0,  0,  1)),
    ("X1 - X3 - X4 >= 0",        (1,  0, -1, -1)),  # Plurality A >= B
    ("X1 - X2 >= 0",             (1, -1,  0,  0)),  # Plurality A >= C
    ("-X1 + X2 + X3 + 2*X4 >= 0",(-1, 1,  1,  2)),  # Borda B >= A
    ("X1 - X2 + 2*X3 + X4 >= 0", (1, -1,  2,  1)),  # Borda B >= C
]

# Equation: X1 + X2 + X3 + X4 = 1
EQ_LHS = (1, 1, 1, 1)
EQ_RHS = 1


def solve_4x4(rows, rhs):
    """Solve a 4x4 rational linear system A x = b exactly.
    Return a list of 4 Fractions, or None if singular.
    """
    A = [[Fraction(c) for c in row] for row in rows]
    b = [Fraction(r) for r in rhs]
    n = 4
    for c in range(n):
        # Find a nonzero pivot in column c.
        piv = None
        for r in range(c, n):
            if A[r][c] != 0:
                piv = r
                break
        if piv is None:
            return None
        A[c], A[piv] = A[piv], A[c]
        b[c], b[piv] = b[piv], b[c]
        # Eliminate column c in every other row.
        for r in range(n):
            if r == c or A[r][c] == 0:
                continue
            factor = A[r][c] / A[c][c]
            A[r] = [A[r][k] - factor * A[c][k] for k in range(n)]
            b[r] = b[r] - factor * b[c]
    return [b[c] / A[c][c] for c in range(n)]


def in_polytope(X):
    """True iff X (list of 4 Fractions) lies in the closed chamber P."""
    for _, a in INEQS:
        if sum(Fraction(a[i]) * X[i] for i in range(4)) < 0:
            return False
    if sum(X) != 1:
        return False
    return True


def lcm(a, b):
    return a * b // math.gcd(a, b)


def main():
    vertices = set()
    for triple in combinations(range(len(INEQS)), 3):
        rows = [list(INEQS[i][1]) for i in triple]
        rows.append(list(EQ_LHS))
        rhs = [0, 0, 0, EQ_RHS]
        sol = solve_4x4(rows, rhs)
        if sol is None:
            continue
        if in_polytope(sol):
            vertices.add(tuple(sol))

    print("Closed chamber polytope vertices:")
    print(f"  {'X1':>10} {'X2':>10} {'X3':>10} {'X4':>10}    denom")
    overall = 1
    for v in sorted(vertices, key=lambda x: tuple(float(c) for c in x)):
        d = 1
        for c in v:
            d = lcm(d, c.denominator)
        overall = lcm(overall, d)
        row = "  " + " ".join(f"{str(c):>10}" for c in v)
        print(f"{row}    {d}")
    print(f"\nNumber of vertices       : {len(vertices)}")
    print(f"LCM of vertex denominators: {overall}")


    failures = []
    if len(vertices) != 6:
        failures.append(f"expected 6 vertices, got {len(vertices)}")
    if overall != 6:
        failures.append(f"expected LCM = 6, got {overall}")
    for v in vertices:
        for c in v:
            if 6 % c.denominator != 0:
                failures.append(
                    f"vertex {v} has denominator {c.denominator} "
                    f"not dividing 6"
                )

    if failures:
        print("\nFAIL:")
        for f in failures:
            print("  - " + f)
        sys.exit(1)

    print("\nAll vertex denominators divide 6.")
    print("By Stanley's theorem on Ehrhart series of rational polytopes,")
    print("D_AB(n) is a quasi-polynomial of degree <= 3 and period dividing 6.")
    print("\nPASS")
    sys.exit(0)


if __name__ == "__main__":
    main()
