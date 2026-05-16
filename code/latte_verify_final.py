"""Verify Theorem 4 values with LattE counts on the strict open chamber."""

import os, subprocess, shutil, time
from fractions import Fraction

QUASI = {
    0: (Fraction(2),        Fraction(-5,6),  Fraction(1,36), Fraction(1,27)),
    1: (Fraction(29,108),   Fraction(-1,3),  Fraction(1,36), Fraction(1,27)),
    2: (Fraction(46,27),    Fraction(-19,18),Fraction(1,36), Fraction(1,27)),
    3: (Fraction(-1,4),     Fraction(-1,3),  Fraction(1,36), Fraction(1,27)),
    4: (Fraction(68,27),    Fraction(-5,6),  Fraction(1,36), Fraction(1,27)),
    5: (Fraction(-59,108),  Fraction(-5,9),  Fraction(1,36), Fraction(1,27)),
}
def formula(n):
    a0, a1, a2, a3 = QUASI[n % 6]
    return a0 + a1*n + a2*n*n + a3*n*n*n

def write_chamber_AB(filename, n):
    """LattE input for the OPEN chamber (P=A, B=B) at parameter n.
    Constraints:
      sum x_i = n                               (linearity)
      x_i >= 0           (4 inequalities)
      x_1 - x_3 - x_4 >= 1     (Plur A > B,  strict for integers)
      x_1 - x_2 >= 1            (Plur A > C)
      -x_1 + x_2 + x_3 + 2 x_4 >= 1   (Borda B > A)
      x_1 - x_2 + 2 x_3 + x_4 >= 1    (Borda B > C)
    LattE row format: [b, c1, c2, c3, c4] meaning b + c1 x1 + c2 x2 + c3 x3 + c4 x4 >= 0.
    """
    rows = [
        (n, -1, -1, -1, -1),     # n - sum x = 0  (linearity)
        (0, 1, 0, 0, 0),         # x1 >= 0
        (0, 0, 1, 0, 0),         # x2 >= 0
        (0, 0, 0, 1, 0),         # x3 >= 0
        (0, 0, 0, 0, 1),         # x4 >= 0
        (-1, 1, 0, -1, -1),      # -1 + x1 - x3 - x4 >= 0  i.e. x1 - x3 - x4 >= 1
        (-1, 1, -1, 0, 0),       # x1 - x2 >= 1
        (-1, -1, 1, 1, 2),       # -x1 + x2 + x3 + 2 x4 >= 1
        (-1, 1, -1, 2, 1),       # x1 - x2 + 2 x3 + x4 >= 1
    ]
    with open(filename, 'w') as f:
        f.write(f"{len(rows)} 5\n")
        for r in rows:
            f.write(" ".join(str(v) for v in r) + "\n")
        f.write("linearity 1 1\n")

def latte_count(filename):
    """Run latte-count from a fresh dir to avoid stale output files; return integer."""
    workdir = filename + ".workdir"
    if os.path.isdir(workdir):
        shutil.rmtree(workdir)
    os.makedirs(workdir)
    fname_in_workdir = os.path.join(workdir, os.path.basename(filename))
    shutil.copy(filename, fname_in_workdir)
    res = subprocess.run(
        ['latte-count', os.path.basename(filename)],
        cwd=workdir, capture_output=True, text=True, timeout=180
    )
    cnt_path = os.path.join(workdir, 'numOfLatticePoints')
    if not os.path.isfile(cnt_path):
        return None, res.stdout + res.stderr
    with open(cnt_path) as f:
        cnt = int(f.read().strip())
    return cnt, ""

WORKROOT = 'latte_runs/open_chamber'
os.makedirs(WORKROOT, exist_ok=True)
ns = [4, 6, 12, 18, 24, 30, 36, 42, 48, 60, 72,
      80, 90, 100, 120, 150, 200, 300, 500, 1000]

print("LattE strict-count verification of Theorem 4")
print(f"{'n':>5} {'r':>3} {'D_{(A,B)} LattE':>17} {'D^SP=2*L':>10} "
      f"{'Formula':>12} {'Match':>6}")

t0 = time.time()
all_match = True
for n in ns:
    fname = os.path.join(WORKROOT, f"AB_n{n}.latte")
    write_chamber_AB(fname, n)
    L, err = latte_count(fname)
    if L is None:
        print(f"{n:>5} -- LattE failed: {err[:200]}")
        all_match = False
        continue
    pred = formula(n)
    twoL = 2 * L
    ok = (Fraction(twoL) == pred)
    if not ok:
        all_match = False
    print(f"{n:>5} {n%6:>3} {L:>17} {twoL:>10} {int(pred):>12} {'✓' if ok else '✗'}")

print(f"\nTotal LattE runs: {len(ns)}; elapsed {time.time()-t0:.1f}s")
print(f"All match Theorem 4 formula: {all_match}")
