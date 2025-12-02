from typing import List, Optional, Tuple
import numpy as np
from pyeda.inter import BinaryDecisionDiagram

def max_reachable_marking(
    P: List[str],
    bdd: BinaryDecisionDiagram,
    c: np.ndarray,
) -> Tuple[Optional[List[int]], Optional[int]]:
    """
    Maximize c^T M over all 0/1 markings M that satisfy the BDD, using exhaustive search.

    Parameters
    ----------
    P   : list of place names
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

    # Early exit if BDD is empty
    if bdd.is_zero():
        return None, None

    var_in_bdd = {v.name: v for v in bdd.support}

    best_value: Optional[int] = None
    best_marking: Optional[List[int]] = None

    # Generate all possible 0/1 assignments
    for i in range(2 ** n):
        # Convert i to binary marking
        marking = [(i >> j) & 1 for j in range(n)]
        # Restrict BDD according to this marking
        restricted_bdd = bdd
        for var_name, val in zip(P, marking):
            var_obj = var_in_bdd.get(var_name)
            if var_obj is not None:
                restricted_bdd = restricted_bdd.restrict({var_obj: val})
        # If marking satisfies BDD, check objective
        if not restricted_bdd.is_zero():
            value = int(np.dot(c, marking))
            if best_value is None or value > best_value:
                best_value = value
                best_marking = marking.copy()

    return best_marking, best_value
