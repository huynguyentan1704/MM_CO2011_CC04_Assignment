import collections
from typing import Tuple, List, Optional
from pyeda.inter import *
from collections import deque
from .PetriNet import PetriNet
import numpy as np
from itertools import product
# ----------------------
# Helpers
# ----------------------
def _normalize_matrices(pn):
    """
    Ensure I and O are numpy arrays with shape (P, T).
    If given as (T, P) they will be transposed.
    Returns I, O, M0 as numpy arrays (int dtype).
    """
    P = len(pn.place_ids)
    T = len(pn.trans_ids)

    I = np.array(pn.I, copy=True)
    O = np.array(pn.O, copy=True)
    M0 = np.array(pn.M0, copy=True)

    # If shapes are flipped, transpose
    if I.shape == (T, P):
        I = I.T
    if O.shape == (T, P):
        O = O.T

    # Ensure shapes now match (P, T)
    if I.shape != (P, T) or O.shape != (P, T) or M0.shape[0] != P:
        # Try to coerce to correct shapes, or raise informative error
        try:
            I = I.reshape((P, T))
            O = O.reshape((P, T))
            M0 = M0.reshape((P,))
        except Exception as e:
            raise ValueError(f"Cannot normalize I/O/M0 shapes: I={I.shape}, O={O.shape}, M0={M0.shape}") from e

    # Convert to integer arrays
    I = I.astype(int)
    O = O.astype(int)
    M0 = M0.astype(int)

    return I, O, M0


def _parse_bdd_assignment(assg: dict, P: int) -> dict:
    """
    Parse one satisfying assignment dict returned by pyeda.bdd.satisfy_all().
    The BDD variables in tests are 'p1','p2',... (1-based). We support names
    'p0' (0-based) as well.
    Returns a mapping {place_index: 0 or 1} for those variables explicitly assigned.
    """
    cons = {}
    for var, val in assg.items():
        # val may be a BoolConstant, int 0/1, or Python bool
        try:
            v = int(bool(val))
        except Exception:
            try:
                v = int(val)
            except Exception:
                continue

        name = str(var)
        if not name.startswith('p'):
            continue
        idx_str = name[1:]
        if not idx_str.isdigit():
            continue
        idx = int(idx_str)
        # try zero-based first, else 1-based
        if 0 <= idx < P:
            cons[idx] = v
        elif 1 <= idx <= P:
            cons[idx - 1] = v
    return cons


def _is_transition_enabled_for_marking(M: np.ndarray, I: np.ndarray, O: np.ndarray, t_idx: int) -> bool:
    """
    Check whether transition t_idx is enabled at marking M under 1-safe semantics.
    Conditions:
      - For all p: M[p] >= I[p,t]
      - After firing, for all p: M[p] - I[p,t] + O[p,t] <= 1  (1-safe constraint)
    """
    P, T = I.shape[0], I.shape[1]
    # check inputs
    for p in range(P):
        if M[p] < I[p, t_idx]:
            return False
    # check resulting marking respects 1-safety
    for p in range(P):
        new_tok = M[p] - I[p, t_idx] + O[p, t_idx]
        if new_tok > 1:
            return False
        if new_tok < 0:
            return False
    return True


def _is_dead_marking(M: np.ndarray, I: np.ndarray, O: np.ndarray) -> bool:
    """
    A marking is dead if no transition is enabled at it.
    """
    P, T = I.shape[0], I.shape[1]
    for t in range(T):
        if _is_transition_enabled_for_marking(M, I, O, t):
            return False
    return True


def _is_reachable_by_bfs(M_target: np.ndarray, I: np.ndarray, O: np.ndarray, M0: np.ndarray) -> bool:
    """
    Explicit BFS over marking graph using firing rules defined by I and O.
    Returns True if M_target (exact equality) is reachable from M0.
    """
    P, T = I.shape[0], I.shape[1]
    start = tuple(int(x) for x in M0.tolist())
    target = tuple(int(x) for x in M_target.tolist())
    if start == target:
        return True

    visited = set([start])
    q = deque([start])

    while q:
        cur = q.popleft()
        cur_arr = np.array(cur, dtype=int)
        for t in range(T):
            if not _is_transition_enabled_for_marking(cur_arr, I, O, t):
                continue
            # fire
            nxt = cur_arr - I[:, t] + O[:, t]
            if np.any(nxt < 0):
                continue
            nxt_t = tuple(int(x) for x in nxt.tolist())
            if nxt_t == target:
                return True
            if nxt_t not in visited:
                visited.add(nxt_t)
                q.append(nxt_t)
    return False


# ----------------------
# Main function 
# ----------------------
def deadlock_reachable_marking(
    pn,
    bdd: BinaryDecisionDiagram,
) -> Optional[List[int]]:
    """
    Combine a lightweight bounded integer search (partial ILP) with BDD expansion.

    For each satisfying assignment from the BDD:
      - interpret assigned place variables as constraints (0 or >=1)
      - search small bounded firing-count vectors x (nonnegative integers)
        that satisfy M = M0 + C * x (C = O - I)
      - for each candidate M:
          * ensure it respects the BDD-assignment constraints
          * check it is a dead marking (no enabled transition under 1-safe)
          * verify reachability from M0 by explicit BFS
          * if so, return M as a Python list of ints

    If no reachable dead marking satisfying the BDD exists, return None.
    """
    # Normalize matrices
    I, O, M0 = _normalize_matrices(pn)
    P = I.shape[0]
    T = I.shape[1]

    # State-change matrix
    C = O - I

    # Small bounded search (heuristic)
    # Heuristic bound: at least 4; proportional to sum(M0)+3*P; cap to 8 for safety
    heuristic = int(max(4, int(np.sum(M0)) + 3 * P))
    if heuristic <= 6:
        BOUND = 6
    else:
        BOUND = min(heuristic, 8)

    # Acquire iterator over satisfying assignments
    try:
        sat_iter = bdd.satisfy_all()
    except Exception:
        # If bdd object doesn't provide satisfy_all, give up gracefully
        return None

    # Iterate assignments from BDD (partial boolean constraints)
    for sat in sat_iter:
        # sat is a dict-like mapping var->value (0/1 or booleans)
        constraints = _parse_bdd_assignment(sat, P)

        # Now brute-force small integer firing counts x in [0..BOUND]^T
        # If T is zero (no transitions), then only consider x = [] and M = M0
        ranges = [range(BOUND + 1) for _ in range(T)] if T > 0 else [()]

        # If T == 0, handle special case: check M0 only
        if T == 0:
            M_candidate = M0.copy()
            # check constraints
            violates = False
            for p_idx, val in constraints.items():
                if val == 0 and M_candidate[p_idx] != 0:
                    violates = True
                    break
                if val == 1 and M_candidate[p_idx] < 1:
                    violates = True
                    break
            if violates:
                continue
            if _is_dead_marking(M_candidate, I, O) and _is_reachable_by_bfs(M_candidate, I, O, M0):
                return [int(x) for x in M_candidate.tolist()]
            else:
                continue

        # iterate over firing-count vectors
        for x_tuple in product(*ranges):
            x_arr = np.array(x_tuple, dtype=int).reshape((T,))
            M_candidate = M0 + C.dot(x_arr)

            # require non-negative and integer
            if np.any(M_candidate < 0):
                continue

            # Enforce BDD constraints: assigned 0 -> exact 0; assigned 1 -> at least 1
            violated = False
            for p_idx, v in constraints.items():
                if v == 0:
                    if M_candidate[p_idx] != 0:
                        violated = True
                        break
                else:
                    if M_candidate[p_idx] < 1:
                        violated = True
                        break
            if violated:
                continue

            # Check dead marking
            if not _is_dead_marking(M_candidate, I, O):
                continue

            # Verify reachable from M0 by BFS (actual firing sequences)
            if _is_reachable_by_bfs(M_candidate, I, O, M0):
                # Return as python list of ints
                return [int(x) for x in M_candidate.tolist()]

    # No reachable dead marking found
    return None
