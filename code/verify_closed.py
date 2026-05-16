"""Compare closed-chamber brute-force counts against LattE coefficients."""
from disagreement import compositions


def closed_AB(n):
    """Count integer profiles (x1,x2,x3,x4) on SP domain with x1+x2+x3+x4=n,
    where Plur(A)>=Plur(B), Plur(A)>=Plur(C), Borda(B)>=Borda(A), Borda(B)>=Borda(C).
    All weakly (closed)."""
    cnt = 0
    for x1, x2, x3, x4 in compositions(n, 4):
        if (x1 >= x3 + x4 and
            x1 >= x2 and
            x2 + x3 + 2*x4 >= x1 and
            x1 + 2*x3 + x4 >= x2):
            cnt += 1
    return cnt

LATTE = [1, 0, 3, 3, 6, 8, 14, 15, 25, 29, 39, 47, 62, 69, 90, 102,
         123, 141, 169, 186, 222, 246, 282, 314, 359, 390]

if __name__ == "__main__":
    print("LattE closed Ehrhart vs brute force")
    print(f"{'n':>3} {'brute':>6} {'latte':>6} {'match':>6}")
    all_match = True
    for n in range(len(LATTE)):
        b = closed_AB(n)
        L = LATTE[n]
        ok = (b == L)
        if not ok:
            all_match = False
        print(f"{n:>3} {b:>6} {L:>6} {'✓' if ok else '✗'}")
    print(f"\nAll match: {all_match}")
