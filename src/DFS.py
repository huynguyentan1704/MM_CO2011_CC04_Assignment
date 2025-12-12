from collections import deque
import numpy as np
from .PetriNet import PetriNet
from typing import Set, Tuple


def dfs_reachable(pn: PetriNet) -> Set[Tuple[int, ...]]:
    """
    DFS reachable cho Petri Net 1-safe.
    - I: (T, P)
    - O: (T, P)
    - M0: (P,)
    """
    I = pn.I       # (T, P)
    O = pn.O       # (T, P)
    M0 = pn.M0     # (P,)

    if I is None or O is None or M0 is None:
        raise ValueError("PetriNet missing I, O, or M0")

    num_trans, num_places = I.shape

    start = tuple(int(x) for x in M0.tolist())

    visited: Set[Tuple[int, ...]] = set()
    stack: list[Tuple[int, ...]] = [start]
    visited.add(start)

    while stack:
        current = stack.pop()
        M = np.array(current, dtype=int)

        # theo đúng DFS pseudo-code → duyệt reversed transitions
        for t in reversed(range(num_trans)):
            need = I[t, :]          # điều kiện cần token
            if not np.all(M >= need):
                continue

            # firing
            M_new = M - need + O[t, :]

            # 1-safe: không được có place nào >1 token hoặc <0
            if np.any(M_new < 0) or np.any(M_new > 1):
                continue

            m_tuple = tuple(int(x) for x in M_new.tolist())

            if m_tuple not in visited:
                visited.add(m_tuple)
                stack.append(m_tuple)

    return visited
