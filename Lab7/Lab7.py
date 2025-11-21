# baby_step_giant_step.py
# Solve for smallest x: G^x ≡ H (mod Q) using Baby-step Giant-step
# Usage: provide three integers G H Q on one line (stdin)

import sys
import math

def baby_step_giant_step(g, h, p):
    """
    Solve g^x = h (mod p) for x, with p prime (or general modulus).
    Returns smallest nonnegative x if exists, otherwise None.
    """
    # handle trivial cases
    g %= p
    h %= p
    if h == 1:
        return 0
    if g == 0:
        return 0 if h == 0 else None

    m = int(math.isqrt(p)) + 1  # m ~ ceil(sqrt(p))

    # baby steps: store value -> j for g^j
    baby = {}
    cur = 1
    for j in range(m):
        # keep only the smallest j for collisions
        if cur not in baby:
            baby[cur] = j
        cur = (cur * g) % p

    # compute g^{-m} mod p using Fermat (p prime): g^{-m} == g^{(p-1)-m}
    # For a non-prime modulus, we'd need modular inverse; but Q is prime in problem.
    inv_factor = pow(g, (p - 1) - m % (p - 1), p)

    # giant steps: look for h * (g^{-m})^i in baby
    gamma = h
    for i in range(m + 1):
        if gamma in baby:
            x = i * m + baby[gamma]
            # x is a solution in [0, p-2]; because we scanned i increasing and stored smallest j,
            # this will be the minimal nonnegative solution found by BSGS.
            return x
        gamma = (gamma * inv_factor) % p

    return None

def main():
    data = sys.stdin.read().strip().split()
    if len(data) < 3:
        print("Missing input")
        return
    G, H, Q = map(int, data[:3])
    x = baby_step_giant_step(G, H, Q)
    if x is None:
        print("No solution")
    else:
        print(x)

if __name__ == "__main__":
    main()
