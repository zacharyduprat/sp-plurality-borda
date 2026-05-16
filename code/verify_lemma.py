"""Check with LattE that all forbidden SP disagreement chambers are empty."""
import os
from latte_verify_final import latte_count

WORKROOT = 'latte_runs/forbidden_chambers'
os.makedirs(WORKROOT, exist_ok=True)


def write_chamber(filename, n, ineqs):
    rows = [
        (n, -1, -1, -1, -1),
        (0, 1, 0, 0, 0),
        (0, 0, 1, 0, 0),
        (0, 0, 0, 1, 0),
        (0, 0, 0, 0, 1),
    ]
    for coeffs in ineqs:
        rows.append((-1,) + coeffs)
    with open(filename, 'w') as f:
        f.write(f"{len(rows)} 5\n")
        for r in rows:
            f.write(" ".join(str(v) for v in r) + "\n")
        f.write("linearity 1 1\n")


def make_strict_ineqs(plur_winner, borda_winner):
    plur = {'A':(1,0,0,0),'B':(0,0,1,1),'C':(0,1,0,0)}
    bord = {'A':(2,0,1,0),'B':(1,1,2,2),'C':(0,2,0,1)}
    ineqs = []
    p = plur[plur_winner]
    for c in 'ABC':
        if c == plur_winner:
            continue
        ineqs.append(tuple(p[i] - plur[c][i] for i in range(4)))
    b = bord[borda_winner]
    for c in 'ABC':
        if c == borda_winner:
            continue
        ineqs.append(tuple(b[i] - bord[c][i] for i in range(4)))
    return ineqs

FORBIDDEN = {
    'A_C': make_strict_ineqs('A','C'),
    'C_A': make_strict_ineqs('C','A'),
    'B_A': make_strict_ineqs('B','A'),
    'B_C': make_strict_ineqs('B','C'),
}

if __name__ == "__main__":
    ns_to_test = [6, 12, 30, 60, 100, 300]
    print("LattE confirmation of SP-Borda centrism lemma")
    print("Each 'forbidden' chamber should give count 0 for all tested n.")
    print(f"{'chamber':>10} | " + " ".join(f"n={n:>3}" for n in ns_to_test))
    all_zero = True
    for label, ineqs in FORBIDDEN.items():
        line = f"{label:>10} |"
        for n in ns_to_test:
            fn = os.path.join(WORKROOT, f"{label}_n{n}.latte")
            write_chamber(fn, n, ineqs)
            c, _ = latte_count(fn)
            line += f" {c:>5}"
            if c != 0:
                all_zero = False
        print(line)

    print(f"\nLemma verified by LattE on tested values: {all_zero}")
