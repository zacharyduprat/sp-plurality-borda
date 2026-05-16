"""Brute-force disagreement counts for IAC and SP profiles on three candidates."""

from itertools import product
from fractions import Fraction

RANKINGS = [
    ('A','B','C'), ('A','C','B'),
    ('B','A','C'), ('B','C','A'),
    ('C','A','B'), ('C','B','A'),
]

SP_INDICES = (0, 5, 2, 3)            # single-peaked on A<B<C
IAC_INDICES = (0, 1, 2, 3, 4, 5)     # full IAC

def compositions(n, k):
    """Iterate compositions of n into k nonneg integer parts."""
    if k == 1:
        yield (n,)
        return
    for i in range(n + 1):
        for rest in compositions(n - i, k - 1):
            yield (i,) + rest

def winners(profile, indices):
    """Return (plurality winner, borda winner). None if tied."""
    plur = {'A':0, 'B':0, 'C':0}
    bord = {'A':0, 'B':0, 'C':0}
    for cnt, idx in zip(profile, indices):
        rk = RANKINGS[idx]
        plur[rk[0]] += cnt
        for pos, cand in enumerate(rk):
            bord[cand] += cnt * (2 - pos)
    pmax = max(plur.values())
    pwins = [c for c,v in plur.items() if v == pmax]
    pw = pwins[0] if len(pwins) == 1 else None
    bmax = max(bord.values())
    bwins = [c for c,v in bord.items() if v == bmax]
    bw = bwins[0] if len(bwins) == 1 else None
    return pw, bw

def enumerate_events(n, indices):
    """Return dict counting joint (plurality, borda) outcomes."""
    counts = {}
    total = 0
    for prof in compositions(n, len(indices)):
        total += 1
        pw, bw = winners(prof, indices)
        key = (pw, bw)
        counts[key] = counts.get(key, 0) + 1
    return counts, total

def disagreement(counts):
    """Count profiles where both rules have unique winners and they differ."""
    return sum(v for (p,b), v in counts.items() if p and b and p != b)

def both_unique(counts):
    return sum(v for (p,b), v in counts.items() if p and b)


if __name__ == "__main__":
    print("IAC (m=3, 6 ranking types)")
    print(f"{'n':>3} {'D(n)':>10} {'BothUnique(n)':>16} {'Total C(n+5,5)':>18}")
    iac_d, iac_total, iac_both = [], [], []
    for n in range(0, 21):
        counts, total = enumerate_events(n, IAC_INDICES)
        d = disagreement(counts)
        bu = both_unique(counts)
        iac_d.append(d); iac_total.append(total); iac_both.append(bu)
        print(f"{n:>3} {d:>10} {bu:>16} {total:>18}")

    print("\n=== Single-peaked m=3 on axis A<B<C (4 ranking types) ===")
    print(f"{'n':>3} {'D(n)':>10} {'BothUnique(n)':>16} {'Total C(n+3,3)':>18}")
    sp_d, sp_total, sp_both = [], [], []
    for n in range(0, 41):
        counts, total = enumerate_events(n, SP_INDICES)
        d = disagreement(counts)
        bu = both_unique(counts)
        sp_d.append(d); sp_total.append(total); sp_both.append(bu)
        print(f"{n:>3} {d:>10} {bu:>16} {total:>18}")


    print("\n=== Finite differences of D^SP(n) ===")
    seq = sp_d[:]
    for order in range(5):
        print(f"order {order}: {seq[:12]}")
        seq = [seq[i+1] - seq[i] for i in range(len(seq)-1)]
