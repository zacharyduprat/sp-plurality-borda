"""Derive and verify the strict-chamber generating function F_AB(t)."""

import sys


NMAX = 42  # how far to brute-force; values past 11 act as a check.


def D_AB_count(n):
    """Brute force the strict-chamber count for a single value of n."""
    cnt = 0
    for x1 in range(n + 1):
        for x2 in range(n + 1 - x1):
            for x3 in range(n + 1 - x1 - x2):
                x4 = n - x1 - x2 - x3
                if (x1 >= x3 + x4 + 1
                        and x1 >= x2 + 1
                        and x2 + x3 + 2 * x4 >= x1 + 1
                        and x1 + 2 * x3 + x4 >= x2 + 1):
                    cnt += 1
    return cnt


def poly_mul(a, b):
    """Multiply two integer polynomials given as ascending coefficient lists."""
    out = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        if ai == 0:
            continue
        for j, bj in enumerate(b):
            out[i + j] += ai * bj
    return out


def format_poly(coeffs, var="t"):
    """Pretty print a polynomial from a list of integer coefficients."""
    pieces = []
    for k, c in enumerate(coeffs):
        if c == 0:
            continue
        if k == 0:
            pieces.append(f"{c}")
            continue
        sign = "+" if c > 0 else "-"
        mag = abs(c)
        if mag == 1:
            term = f"{var}^{k}" if k != 1 else var
        else:
            term = f"{mag}*{var}^{k}" if k != 1 else f"{mag}*{var}"
        if not pieces:
            pieces.append(("-" + term) if c < 0 else term)
        else:
            pieces.append(f" {sign} {term}")
    return "".join(pieces) if pieces else "0"


def main():

    one_minus_t = [1, -1]
    one_plus_t = [1, 1]
    cyc3 = [1, 1, 1]
    factor_a = poly_mul(poly_mul(poly_mul(one_minus_t, one_minus_t),
                                 one_minus_t), one_minus_t)   # (1-t)^4
    factor_b = poly_mul(one_plus_t, one_plus_t)               # (1+t)^2
    factor_c = poly_mul(cyc3, cyc3)                           # (1+t+t^2)^2
    D = poly_mul(poly_mul(factor_a, factor_b), factor_c)

    expected_D = [1, 0, -2, -2, 1, 4, 1, -2, -2, 0, 1]
    if D != expected_D:
        print("FAIL: cyclotomic product disagrees with LattE denominator.")
        print(f"  computed: {D}")
        print(f"  expected: {expected_D}")
        sys.exit(1)

    print("Closed-chamber denominator")
    print("  D(t) = (1-t)^4 (1+t)^2 (1+t+t^2)^2")
    print(f"       = {format_poly(D)}")
    print(f"  coefficients: {D}")


    print(f"\nBrute-forcing D_AB(n) for n = 0..{NMAX} ...")
    DAB = [D_AB_count(n) for n in range(NMAX + 1)]
    print(f"  D_AB[0..15] = {DAB[:16]}")


    conv = []
    for k in range(NMAX + 1):
        s = 0
        for i, di in enumerate(D):
            j = k - i
            if 0 <= j < len(DAB):
                s += di * DAB[j]
        conv.append(s)


    N_AB = conv[:11]
    expected_N = [0, 0, 0, 0, 1, 1, 1, 2, 0, 0, -1]
    if N_AB != expected_N:
        print("FAIL: derived numerator does not match expected.")
        print(f"  computed: {N_AB}")
        print(f"  expected: {expected_N}")
        sys.exit(1)

    tail = conv[11:]
    bad = [(k + 11, c) for k, c in enumerate(tail) if c != 0]
    if bad:
        print(f"FAIL: convolution does not vanish past t^10.")
        print(f"  first three nonzero entries: {bad[:3]}")
        sys.exit(1)

    print("\nDerived strict generating function:")
    print(f"  N_AB(t) = {format_poly(N_AB)}")
    print( "  F_AB(t) = N_AB(t) / [(1-t)^4 (1+t)^2 (1+t+t^2)^2]")
    print(f"\nConvolution F_AB(t) * D(t) terminates at t^10 and equals 0 for "
          f"every k in [11, {NMAX}].")
    print("\nPASS")
    sys.exit(0)


if __name__ == "__main__":
    main()
