import numpy as np
from src.Optimization import max_reachable_marking
from pyeda.inter import *



def test_large_state_space_strong_pruning():
    # 10 boolean places → worst case 2^10 = 1024 states
    P = [f"p{i}" for i in range(10)]
    vars = [exprvar(p) for p in P]

    # Create a large reachable space:
    # - p0 determines high-value states
    # - Other places generate many combinations = large exploration cost
    #
    # This expression creates:
    #   - Many states where p0 = 0 (low-value)
    #   - Some states where p0 = 1 (high-value → B&B prunes everything else)
    #
    # B&B very fast: finds p0=1 early → prune ~99% of search tree
    # Exhaustive very slow: must enumerate almost all 1024 states
    #
    import itertools
    terms = []

    # Many low-value states: p0 = 0 with many combinations
    for bits in itertools.product([0, 1], repeat=9):
        term = And(~vars[0], *[
            vars[i+1] if bits[i] else ~vars[i+1]
            for i in range(9)
        ])
        terms.append(term)

    # A few high-value states: p0 = 1
    terms.append(And(vars[0], vars[1], vars[2], vars[3]))

    reachable_expr = Or(*terms)

    bdd = expr2bdd(reachable_expr)

    # Very skewed weights: p0 guarantees a huge score → pruning is strong
    c = np.array([1000] + [1] * 9)

    marking, value = max_reachable_marking(P, bdd, c)

    # Expected: best reachable marking must have p0 = 1
    assert marking[0] == 1
    assert value >= 1000
