#!/usr/bin/env python3
"""
mcs_practical.py

Practical Python examples implementing key concepts across ~25 lectures
of MIT 6.042J "Mathematics for Computer Science".

Run:
    python mcs_practical.py

Each section corresponds to a lecture/topic and prints a short demo.
"""

from itertools import product, permutations, combinations
from math import comb, factorial, gcd
from fractions import Fraction
import random
from functools import lru_cache

# ---------------------------
# Lecture 1: Propositional Logic & Truth Tables
# ---------------------------
def truth_table(expr_func, vars_names):
    """Print truth table for a boolean function expr_func taking len(vars_names) args."""
    n = len(vars_names)
    print(f"\n=== Lecture 1 — Truth table for: {vars_names} ===")
    header = " | ".join(vars_names) + " | result"
    print(header)
    print("-" * len(header))
    for vals in product([False, True], repeat=n):
        result = expr_func(*vals)
        row = " | ".join(str(v) for v in vals) + f" | {result}"
        print(row)

def example_lecture1():
    # Example: (P AND Q) OR (NOT P)
    expr = lambda p, q: (p and q) or (not p)
    truth_table(expr, ["P", "Q"])

# ---------------------------
# Lecture 2: Logical Equivalences & De Morgan
# ---------------------------
def check_de_morgan():
    print("\n=== Lecture 2 — De Morgan check ===")
    combos = list(product([False, True], repeat=2))
    ok = True
    for p, q in combos:
        left = not (p and q)
        right = (not p) or (not q)
        print(f"P={p}, Q={q} : not(P and Q)={left}, (not P) or (not Q)={right}")
        ok &= (left == right)
    print("De Morgan law holds for all combinations:", ok)

# ---------------------------
# Lecture 3: Sets, Operations, Power Set
# ---------------------------
def powerset(s):
    lst = list(s)
    ps = []
    for r in range(len(lst)+1):
        for combi in combinations(lst, r):
            ps.append(set(combi))
    return ps

def example_lecture3():
    S = {1, 2, 3}
    print("\n=== Lecture 3 — Sets and power set ===")
    print("S =", S)
    print("P(S) contains", len(powerset(S)), "subsets:", powerset(S))

# ---------------------------
# Lecture 4: Proof techniques (direct, contrapositive, contradiction)
# (Demonstrated via simple assertions and small automated checks)
# ---------------------------
def example_lecture4():
    print("\n=== Lecture 4 — Proof ideas (demo) ===")
    # Example proposition: If n^2 is even => n is even (contrapositive proof verified by check)
    def prop(n):
        return (n*n) % 2 == 0 and n % 2 != 0
    # show there is no n violating the theorem in a reasonable range
    found = [n for n in range(0,100) if prop(n)]
    print("Counterexamples found (should be none):", found)

# ---------------------------
# Lecture 5: Induction — proof by induction illustration
# ---------------------------
def sum_formula_n(n):
    # sum 1..n = n(n+1)/2
    return sum(range(1, n+1))

def example_lecture5():
    print("\n=== Lecture 5 — Induction demo ===")
    for n in range(1, 11):
        formula = n*(n+1)//2
        brute = sum_formula_n(n)
        print(f"n={n}: formula={formula}, brute={brute}, OK={formula==brute}")

# ---------------------------
# Lecture 6: Relations & Functions (equivalence relations, partitions)
# ---------------------------
def is_equivalence_relation(universe, relation):
    # relation is set of pairs (a,b)
    # reflexive, symmetric, transitive
    rel = set(relation)
    reflexive = all((x,x) in rel for x in universe)
    symmetric = all(((b,a) in rel) for (a,b) in rel)
    transitive = all(((a,c) in rel) for (a,b) in rel for (c,d) in rel if b==c)
    return reflexive, symmetric, transitive

def example_lecture6():
    print("\n=== Lecture 6 — Relations ===")
    U = {1,2,3}
    R = {(1,1),(2,2),(3,3),(1,2),(2,1)}
    print("Relation R on U:", R)
    print("reflexive,symmetric,transitive:", is_equivalence_relation(U,R))

# ---------------------------
# Lecture 7: Graphs — BFS / DFS basics
# ---------------------------
def bfs(graph, start):
    visited = []
    queue = [start]
    while queue:
        v = queue.pop(0)
        if v not in visited:
            visited.append(v)
            queue.extend([u for u in graph.get(v, []) if u not in visited and u not in queue])
    return visited

def example_lecture7():
    print("\n=== Lecture 7 — Graph BFS demo ===")
    G = { 'A': ['B','C'], 'B': ['A','D'], 'C': ['A','D'], 'D': ['B','C'] }
    print("BFS from A:", bfs(G, 'A'))

# ---------------------------
# Lecture 8: Counting — permutations, combinations, binomial coefficients
# ---------------------------
def example_lecture8():
    print("\n=== Lecture 8 — Counting examples ===")
    print("C(5,2) =", comb(5,2))
    print("5! =", factorial(5))
    print("Permutations of 'ABC':", list(permutations('ABC')))

# ---------------------------
# Lecture 9: Pigeonhole principle
# ---------------------------
def example_lecture9():
    print("\n=== Lecture 9 — Pigeonhole demonstration ===")
    pigeons = 10
    holes = 3
    min_per_hole = pigeons // holes + (1 if pigeons % holes else 0)
    print(f"With {pigeons} pigeons and {holes} holes, some hole has at least {min_per_hole} pigeons.")

# ---------------------------
# Lecture 10: Probability basics (sample space, events)
# ---------------------------
def coin_sim(n=10000):
    heads = 0
    for _ in range(n):
        heads += random.choice([0,1])
    return heads / n

def example_lecture10():
    print("\n=== Lecture 10 — Probability sampling (coin) ===")
    print("Empirical P(heads) ~", coin_sim(20000))

# ---------------------------
# Lecture 11: Conditional probability, Bayes (small numeric example)
# ---------------------------
def example_lecture11():
    print("\n=== Lecture 11 — Bayes small example ===")
    # disease prevalence 1%, test sensitivity 99%, false positive 5%
    p_d = 0.01
    p_pos_d = 0.99
    p_pos_notd = 0.05
    p_pos = p_d*p_pos_d + (1-p_d)*p_pos_notd
    p_d_given_pos = p_d*p_pos_d / p_pos
    print("P(disease|positive) =", p_d_given_pos)

# ---------------------------
# Lecture 12: Discrete distributions / expectation
# ---------------------------
def example_lecture12():
    print("\n=== Lecture 12 — Expectation example ===")
    # expected value of fair die
    exp = sum(i * (1/6) for i in range(1,7))
    print("E[die] =", exp)

# ---------------------------
# Lecture 13: Number theory basics — gcd, modular inverse, extended gcd
# ---------------------------
def extended_gcd(a, b):
    if b == 0:
        return (a, 1, 0)
    g, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return g, x, y

def modinv(a, m):
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        return None
    return x % m

def example_lecture13():
    print("\n=== Lecture 13 — Number theory ===")
    a, m = 17, 3120
    inv = modinv(a, m)
    print(f"modinv({a},{m}) = {inv}")

# ---------------------------
# Lecture 14: Congruences, CRT (Chinese Remainder) simple solver
# ---------------------------
def crt(pairs):
    # pairs: list of (ai, ni), find x ≡ ai (mod ni), naive search (sufficient for small numbers)
    x = 0
    N = 1
    for _, n in pairs:
        N *= n
    total = 0
    for ai, ni in pairs:
        Ni = N // ni
        inv = modinv(Ni, ni)
        total += ai * Ni * inv
    return total % N

def example_lecture14():
    print("\n=== Lecture 14 — CRT example ===")
    pairs = [(2,3),(3,5),(2,7)]
    print("Solution x ≡ 2 (mod3), 3 (mod5), 2 (mod7) -> x =", crt(pairs))

# ---------------------------
# Lecture 15: Recurrences — solve simple recurrence by DP and closed form check
# ---------------------------
@lru_cache(None)
def fib(n):
    if n < 2:
        return n
    return fib(n-1) + fib(n-2)

def example_lecture15():
    print("\n=== Lecture 15 — Recurrence (Fibonacci) ===")
    for i in range(10):
        print(f"fib({i})={fib(i)}", end=", ")
    print()

# ---------------------------
# Lecture 16: Generating functions (simple example: generating function for binomial coefficients)
# (Demonstrated numerically via coefficients)
# ---------------------------
def binomial_coeffs(n):
    return [comb(n, k) for k in range(n+1)]

def example_lecture16():
    print("\n=== Lecture 16 — Generating function (binomial) ===")
    n = 5
    print("Coefficients of (1+x)^5:", binomial_coeffs(n))

# ---------------------------
# Lecture 17: Asymptotics and big-O (examples and checks)
# ---------------------------
def example_lecture17():
    print("\n=== Lecture 17 — Asymptotics example ===")
    # Compare n^2 and n*log n empirically
    import math
    for n in [10,100,1000,10000]:
        print(n, "n^2=", n*n, "n log n=", n*math.log(n))

# ---------------------------
# Lecture 18: Counting advanced — inclusion-exclusion
# ---------------------------
def inclusion_exclusion_union(*sets):
    # compute |union|
    total = 0
    n = len(sets)
    from itertools import combinations
    for r in range(1, n+1):
        for combo in combinations(sets, r):
            inter = set.intersection(*combo)
            if r % 2 == 1:
                total += len(inter)
            else:
                total -= len(inter)
    return total

def example_lecture18():
    print("\n=== Lecture 18 — Inclusion-Exclusion ===")
    A = {1,2,3,4}
    B = {3,4,5}
    C = {4,5,6}
    print("Union size (calc):", inclusion_exclusion_union(A,B,C))
    print("Union size (direct):", len(A|B|C))

# ---------------------------
# Lecture 19: Randomized algorithms / expectation method
# ---------------------------
def randomized_partition_example(n=1000):
    arr = list(range(n))
    random.shuffle(arr)
    pivot = arr[0]
    left = [x for x in arr if x < pivot]
    right = [x for x in arr if x > pivot]
    return len(left), len(right), pivot

def example_lecture19():
    print("\n=== Lecture 19 — Randomized partition example ===")
    print("Left/Right sizes and pivot:", randomized_partition_example(1000))

# ---------------------------
# Lecture 20: Graph algorithms — shortest paths (Dijkstra simple for positive weights)
# ---------------------------
import heapq
def dijkstra(graph, start):
    # graph as adjacency dict: node -> list of (neighbor, weight)
    dist = {start: 0}
    pq = [(0, start)]
    while pq:
        d, u = heapq.heappop(pq)
        if d != dist[u]:
            continue
        for v,w in graph.get(u,[]):
            nd = d + w
            if v not in dist or nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return dist

def example_lecture20():
    print("\n=== Lecture 20 — Dijkstra demo ===")
    G = {
        'A':[('B',1),('C',4)],
        'B':[('C',2),('D',5)],
        'C':[('D',1)],
        'D':[]
    }
    print("Distances from A:", dijkstra(G,'A'))

# ---------------------------
# Lecture 21: Linear algebra basics (vectors, dot product) — small demo
# ---------------------------
def dot(u, v):
    return sum(x*y for x,y in zip(u,v))

def example_lecture21():
    print("\n=== Lecture 21 — Linear algebra basics ===")
    u = [1,2,3]; v=[4,5,6]
    print("u·v =", dot(u,v))

# ---------------------------
# Lecture 22: Algorithms — correctness idea and invariants (demonstrated by selection sort invariant)
# ---------------------------
def selection_sort(arr):
    a = arr[:] 
    n = len(a)
    for i in range(n):
        minj = i
        for j in range(i+1,n):
            if a[j] < a[minj]:
                minj = j
        a[i], a[minj] = a[minj], a[i]
    return a

def example_lecture22():
    print("\n=== Lecture 22 — Algorithm invariant demo (selection sort) ===")
    arr = [5,2,9,1,5,6]
    print("Before:", arr)
    print("After :", selection_sort(arr))

# ---------------------------
# Lecture 23: Combinatorial proofs (illustrate with bijection idea)
# ---------------------------
def example_lecture23():
    print("\n=== Lecture 23 — Combinatorial bijection idea ===")
    # bijection between subsets of size k and combinations: show counts match
    n, k = 5, 2
    subsets = list(combinations(range(n), k))
    print(f"Number of {k}-subsets of {n}-set:", len(subsets), "== C(n,k) =", comb(n,k))

# ---------------------------
# Lecture 24: Cryptography basics (RSA toy example)
# ---------------------------
def rsa_example():
    print("\n=== Lecture 24 — RSA toy example ===")
    # small primes (toy)
    p, q = 61, 53
    n = p * q
    phi = (p-1)*(q-1)
    e = 17
    d = modinv(e, phi)
    msg = 42
    c = pow(msg, e, n)
    m = pow(c, d, n)
    print("n,phi,e,d:", n, phi, e, d)
    print("message:", msg, "cipher:", c, "decrypted:", m)

# ---------------------------
# Lecture 25: Putting it together — small project harness / testing framework
# ---------------------------
def run_all_examples():
    example_lecture1()
    check_de_morgan()
    example_lecture3()
    example_lecture4()
    example_lecture5()
    example_lecture6()
    example_lecture7()
    example_lecture8()
    example_lecture9()
    example_lecture10()
    example_lecture11()
    example_lecture12()
    example_lecture13()
    example_lecture14()
    example_lecture15()
    example_lecture16()
    example_lecture17()
    example_lecture18()
    example_lecture19()
    example_lecture20()
    example_lecture21()
    example_lecture22()
    example_lecture23()
    rsa_example()
    print("\n=== Lecture 25 — End: Complete run of examples ===")

# ---------------------------
# If run as script, execute all
# ---------------------------
if __name__ == "__main__":
    run_all_examples()
