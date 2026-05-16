"""Enumerate arrangement slices Q_S and verify all vertex denominators divide 6."""

import math
import sys
from fractions import Fraction
from itertools import chain, combinations


INEQS = [
    ("X1 >= 0", (1, 0, 0, 0)),
    ("X2 >= 0", (0, 1, 0, 0)),
    ("X3 >= 0", (0, 0, 1, 0)),
    ("X4 >= 0", (0, 0, 0, 1)),
    ("X1 - X3 - X4 >= 0", (1, 0, -1, -1)),
    ("X1 - X2 >= 0", (1, -1, 0, 0)),
    ("-X1 + X2 + X3 + 2*X4 >= 0", (-1, 1, 1, 2)),
    ("X1 - X2 + 2*X3 + X4 >= 0", (1, -1, 2, 1)),
]

HYPERPLANE_INDEX = {1: 4, 2: 5, 3: 6, 4: 7}

AFFINE_LHS = (1, 1, 1, 1)
AFFINE_RHS = Fraction(1)
EXPECTED_DENOM_DIVISOR = 6


def solve_4x4(rows, rhs):
    """
    Solve a 4x4 rational linear system A x = b by Gauss-Jordan elimination.
    Returns a list of 4 Fractions, or None if the system is singular.
    All inputs may be ints or Fractions.
    """
    A = [[Fraction(c) for c in row] for row in rows]
    b = [Fraction(r) for r in rhs]
    n = 4
    for c in range(n):
        piv = next((r for r in range(c, n) if A[r][c] != 0), None)
        if piv is None:
            return None
        A[c], A[piv] = A[piv], A[c]
        b[c], b[piv] = b[piv], b[c]

        for r in range(n):
            if r == c or A[r][c] == 0:
                continue
            f = A[r][c] / A[c][c]
            A[r] = [A[r][k] - f * A[c][k] for k in range(n)]
            b[r] = b[r] - f * b[c]
    return [b[c] / A[c][c] for c in range(n)]


def matrix_rank(rows):
    """Rank of a matrix with entries in Q."""
    if not rows:
        return 0
    M = [[Fraction(x) for x in row] for row in rows]
    nr, nc = len(M), len(M[0])
    r = 0
    for c in range(nc):
        if r >= nr:
            break
        piv = next((rr for rr in range(r, nr) if M[rr][c] != 0), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        for rr in range(nr):
            if rr != r and M[rr][c] != 0:
                f = M[rr][c] / M[r][c]
                M[rr] = [M[rr][k] - f * M[r][k] for k in range(nc)]
        r += 1
    return r


def affine_dim(vertices):
    """Affine dimension of a finite point set: -1 if empty, 0 if singleton."""
    vlist = list(vertices)
    if not vlist:
        return -1
    if len(vlist) == 1:
        return 0
    base = vlist[0]
    diffs = [[v[i] - base[i] for i in range(4)] for v in vlist[1:]]
    return matrix_rank(diffs)


def satisfies_affine(X):
    """X lies on the affine hyperplane X1 + X2 + X3 + X4 = 1."""
    return sum(X) == AFFINE_RHS


def satisfies_polytope(X):
    """X lies in the closed chamber P."""
    return all(
        sum(Fraction(a[i]) * X[i] for i in range(4)) >= 0
        for _, a in INEQS
    )


def hyperplane_value(X, h):
    """
    Value of the chamber inequality whose boundary is H_h, evaluated at X.
    Returns 0 iff X lies exactly on H_h.
    """
    a = INEQS[HYPERPLANE_INDEX[h]][1]
    return sum(Fraction(a[i]) * X[i] for i in range(4))


def vertices_for_subset(S):
    """Enumerate vertices of Q_S := P intersect (intersection_{h in S} H_h)."""
    mandatory = [(AFFINE_LHS, AFFINE_RHS)]
    for h in S:
        a = INEQS[HYPERPLANE_INDEX[h]][1]
        mandatory.append((a, Fraction(0)))

    candidate_boundaries = [(a, Fraction(0)) for _, a in INEQS]
    vertices = set()

    for t_size in range(5):
        for T_indices in combinations(range(8), t_size):
            T_eqs = [candidate_boundaries[i] for i in T_indices]
            pool = mandatory + T_eqs

            if len(pool) < 4:
                continue

            for row_indices in combinations(range(len(pool)), 4):
                rows = [pool[i][0] for i in row_indices]
                rhs = [pool[i][1] for i in row_indices]

                if matrix_rank(rows) < 4:
                    continue

                sol = solve_4x4(rows, rhs)
                if sol is None:
                    continue

                if not all(
                    sum(Fraction(eq[0][i]) * sol[i] for i in range(4)) == eq[1]
                    for eq in mandatory
                ):
                    continue

                if not satisfies_polytope(sol):
                    continue

                if not all(hyperplane_value(sol, h) == 0 for h in S):
                    continue

                vertices.add(tuple(sol))

    return vertices


def lcm(a, b):
    return a * b // math.gcd(a, b)


def denom_of(v):
    """LCM of the denominators of the components of v."""
    d = 1
    for c in v:
        d = lcm(d, c.denominator)
    return d


def label_for(S):
    """Format e.g. () -> '{}', (1,3) -> '{H1,H3}'."""
    if not S:
        return "{}"
    return "{" + ",".join(f"H{h}" for h in sorted(S)) + "}"


def all_subsets(items):
    items = list(items)
    return list(
        chain.from_iterable(combinations(items, r) for r in range(len(items) + 1))
    )


def main():
    print("Arrangement-intersection denominator verification for D_AB(n).")
    print()
    print("Closed chamber P:")
    print("  X1, X2, X3, X4 >= 0")
    print("  X1 + X2 + X3 + X4 = 1")
    print("  X1 >= X3 + X4")
    print("  X1 >= X2")
    print("  X2 + X3 + 2*X4 >= X1")
    print("  X1 + 2*X3 + X4 >= X2")
    print()
    print("Score hyperplanes (boundaries of chamber inequalities):")
    print("  H1: X1 = X3 + X4")
    print("  H2: X1 = X2")
    print("  H3: X2 + X3 + 2*X4 = X1")
    print("  H4: X1 + 2*X3 + X4 = X2")
    print()
    print("For each subset S of {H1, H2, H3, H4}, enumerate the vertices of")
    print("    Q_S := P intersect (intersection of H for H in S).")
    print("The sets Q_S are the arrangement-intersection slices relevant to")
    print("the inside-out Ehrhart period bound for the half-open chamber count.")

    H_labels = [1, 2, 3, 4]
    subsets = all_subsets(H_labels)

    all_unique = set()
    overall_lcm = 1
    max_denom = 1
    failures = []
    per_subset_count = {}

    for S in subsets:
        verts = vertices_for_subset(S)
        per_subset_count[S] = len(verts)
        d_aff = affine_dim(verts)

        print()
        print(
            f"S = {label_for(S):<15}  |S| = {len(S)}   "
            f"vertices = {len(verts)}   affine_dim = {d_aff}"
        )

        if not verts:
            print("  (empty intersection in P)")
        else:
            print(f"  {'X1':>10} {'X2':>10} {'X3':>10} {'X4':>10}    denom")
            for v in sorted(verts, key=lambda x: tuple(float(c) for c in x)):
                d = denom_of(v)
                row = "  " + " ".join(f"{str(c):>10}" for c in v)
                print(f"{row}    {d}")
                all_unique.add(v)
                overall_lcm = lcm(overall_lcm, d)
                max_denom = max(max_denom, d)
                if EXPECTED_DENOM_DIVISOR % d != 0:
                    failures.append(
                        f"S={label_for(S)}, vertex "
                        f"({', '.join(str(c) for c in v)}): "
                        f"denominator {d} does not divide "
                        f"{EXPECTED_DENOM_DIVISOR}"
                    )

    print()
    print("Per-subset vertex counts")
    for S in subsets:
        print(f"  {label_for(S):<22} -> {per_subset_count[S]} vertex(s)")

    print()
    print("Aggregate summary")
    print(f"  Subsets considered            : {len(subsets)}")
    print(f"  Total unique vertices         : {len(all_unique)}")
    print(f"  Maximum vertex denominator    : {max_denom}")
    print(f"  LCM of all vertex denominators: {overall_lcm}")

    if EXPECTED_DENOM_DIVISOR % overall_lcm != 0:
        failures.append(
            f"global LCM {overall_lcm} does not divide {EXPECTED_DENOM_DIVISOR}"
        )

    if failures:
        print()
        print("FAIL:")
        for msg in failures:
            print("  - " + msg)
        sys.exit(1)

    print()
    print(f"All vertices of all {len(subsets)} arrangement-intersection slices")
    print("Q_S = P intersect (intersection_{H in S} H) have rational coordinates")
    print(f"with denominator dividing {EXPECTED_DENOM_DIVISOR}.")
    print()
    print("By inside-out / hyperplane-arrangement Ehrhart theory")
    print("(Stanley; Beck-Robins; Beck-Zaslavsky), the half-open chamber")
    print("count D_AB(n) is therefore a quasi-polynomial of degree at")
    print("most 3 with period dividing 6.")
    print()
    print("PASS")
    sys.exit(0)


if __name__ == "__main__":
    main()
