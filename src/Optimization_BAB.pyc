from typing import List, Optional, Tuple
import numpy as np
from pyeda.inter import BinaryDecisionDiagram


def max_reachable_marking(
    P: List[str],
    bdd: BinaryDecisionDiagram,
    c: np.ndarray,
) -> Tuple[Optional[List[int]], Optional[int]]:
    """
    Maximize c^T M over all 0/1 markings satisfying the BDD.

    Parameters
    ----------
    P : list[str]
        Place/variable names in order.
    bdd : BinaryDecisionDiagram
        BDD representing allowed reachable markings.
    c : np.ndarray
        Integer weights aligned with P.

    Returns
    -------
    (marking, value)
        marking : list[int] or None
        value   : integer or None
    """

    n = len(P)
    if c.shape[0] != n:
        raise ValueError("Length of c must equal number of places P")

    # If the BDD is unsatisfiable → no marking
    if bdd.is_zero():
        return None, None

    # Map var name → actual BDD variable object
    var_map = {v.name: v for v in bdd.support}

    # Precompute upper bound of positive weights from suffix
    suffix_pos = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        suffix_pos[i] = suffix_pos[i + 1] + max(0, int(c[i]))

    best_value: Optional[int] = None
    best_marking: Optional[List[int]] = None
    current = [0] * n

    def dfs(f: BinaryDecisionDiagram, idx: int, partial: int) -> None:
        nonlocal best_value, best_marking

        if f.is_zero():
            return

        if idx == n:
            # If f != 0, it must be 1 (all vars assigned)
            if not f.is_zero():
                if best_value is None or partial > best_value:
                    best_value = partial
                    best_marking = current.copy()
            return

        # Branch & Bound pruning
        if best_value is not None:
            if partial + suffix_pos[idx] <= best_value:
                return

        var_name = P[idx]
        bdd_var = var_map.get(var_name, None)

        # ---- assign 1 ----
        current[idx] = 1
        if bdd_var is not None:
            f_high = f.restrict({bdd_var: 1})
        else:
            f_high = f
        dfs(f_high, idx + 1, partial + int(c[idx]))

        # ---- assign 0 ----
        current[idx] = 0
        if bdd_var is not None:
            f_low = f.restrict({bdd_var: 0})
        else:
            f_low = f
        dfs(f_low, idx + 1, partial)

    dfs(bdd, 0, 0)
    return best_marking, best_value
