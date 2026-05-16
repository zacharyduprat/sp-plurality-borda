"""Parse the LattE closed-chamber rational function and expand coefficients."""
import sympy as sp
import re

def parse_latte_rat(filepath):
    """Convert LattE's Maple-style output 'x := ...' to a sympy expression in t."""
    with open(filepath) as f:
        text = f.read()
    m = re.search(r'x\s*:=\s*(.+?):?\s*$', text.strip(), re.DOTALL)
    if not m:
        raise ValueError("Could not parse LattE .rat file")
    inner = m.group(1).replace('^', '**')
    t = sp.symbols('t')
    expr = sp.sympify(inner, locals={'t': t})
    return sp.simplify(expr), t

def series_coeffs(expr, t, N):
    """Return list of [t^0], ..., [t^N] coefficients."""
    s = sp.series(expr, t, 0, N + 1).removeO()
    poly = sp.Poly(s, t)
    return [int(poly.coeff_monomial(t**n)) for n in range(N + 1)]

if __name__ == "__main__":
    print("Parsing LattE rational function ...")
    expr, t = parse_latte_rat('latte/chamber_AB.latte.rat')
    print("Simplified Ehrhart series of closed chamber (P=A, B=B):")
    print(f"  {expr}")

    N = 25
    print(f"\nExpanding as Taylor series up to t^{N} ...")
    latte_coeffs = series_coeffs(expr, t, N)
    print(f"  LattE coefficients [t^0..t^{N}]:")
    print(f"  {latte_coeffs}")
