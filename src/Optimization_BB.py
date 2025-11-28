from typing import List, Optional, Tuple
import numpy as np
from pyeda.inter import BinaryDecisionDiagram


def max_reachable_marking(
    P: List[str],
    bdd: BinaryDecisionDiagram,
    c: np.ndarray,
) -> Tuple[Optional[List[int]], Optional[int]]:
    """
    Maximize c^T M subject to M satisfies given BDD.
    Branch & Bound on decision tree of variables P.

    Parameters
    ----------
    P   : list of place names, defines variable order
    bdd : pyeda BinaryDecisionDiagram representing reachable markings
    c   : numpy array of integer weights, aligned with P

    Returns
    -------
    (marking, value)
        marking: list[int] of 0/1, or None if BDD is unsatisfiable
        value  : optimal objective value, or None if no marking
    """
    n = len(P)
    if c.shape[0] != n:
        raise ValueError("Length of c must equal number of places P")

    # Nếu BDD = 0 -> không có marking nào thỏa
    if bdd.is_zero():
        return None, None

    # Map tên biến -> object var thực sự trong BDD (nếu có)
    # để dùng đúng object khi restrict
    var_in_bdd = {v.name: v for v in bdd.support}

    # Precompute suffix upper bound: tại depth i,
    # phần tốt nhất còn lại <= sum of positive weights từ i..n-1
    suffix_pos = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        suffix_pos[i] = suffix_pos[i + 1] + max(0, int(c[i]))

    best_value: Optional[int] = None
    best_marking: Optional[List[int]] = None
    current = [0] * n  # marking đang xây

    def dfs(f: BinaryDecisionDiagram, idx: int, partial: int) -> None:
        """
        f    : BDD hiện tại sau khi đã gán P[0..idx-1]
        idx  : đang xét biến P[idx]
        partial : giá trị c^T M với các biến đã gán
        """
        nonlocal best_value, best_marking

        # Nếu f đã là 0 -> không còn nghiệm
        if f.is_zero():
            return

        # Nếu đã gán hết biến
        if idx == n:
            # Lúc này, nếu f không 0 thì phải là 1 (vì mọi biến đã gán)
            if not f.is_zero():
                if best_value is None or partial > best_value:
                    best_value = partial
                    best_marking = current.copy()
            return

        # Branch & Bound: upper bound cho nhánh này
        bound = partial + suffix_pos[idx]
        if best_value is not None and bound <= best_value:
            # Dù gán tốt nhất các biến còn lại cũng không vượt best hiện tại
            return

        var_name = P[idx]
        var_obj = var_in_bdd.get(var_name, None)

        # --- Nhánh high: P[idx] = 1 ---
        current[idx] = 1
        if var_obj is not None:
            f_high = f.restrict({var_obj: 1})
        else:
            # BDD không phụ thuộc biến này
            f_high = f
        dfs(f_high, idx + 1, partial + int(c[idx]))

        # --- Nhánh low: P[idx] = 0 ---
        current[idx] = 0
        if var_obj is not None:
            f_low = f.restrict({var_obj: 0})
        else:
            f_low = f
        dfs(f_low, idx + 1, partial)

    # Bắt đầu từ root BDD, depth 0, giá trị 0
    dfs(bdd, 0, 0)

    return best_marking, best_value
