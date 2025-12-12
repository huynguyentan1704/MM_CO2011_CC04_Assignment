from typing import List, Optional
import numpy as np
import pulp
import itertools
from pyeda.inter import BinaryDecisionDiagram
from .PetriNet import PetriNet


def deadlock_reachable_marking(
    pn: PetriNet,
    reach_bdd: BinaryDecisionDiagram,
) -> Optional[List[int]]:
    """
    Deadlock detection bằng hybrid BDD + ILP (trên tập reachable):

    - BDD (Task 3) cho ta tập marking reachable (0/1, safe).
    - Ta liệt kê tất cả reachable marking M^(k).
      Nếu BDD không phụ thuộc vào 1 số place (don’t care),
      ta expand 0/1 cho các place đó.
    - Precompute enabled[t][k]:
          t enabled tại M^(k) nếu:
            + đủ token: M[p] >= I[t,p] với mọi p
            + successor M' = M - I_t + O_t cũng thuộc tập reachable
              (theo tập đã liệt kê)
    - ILP:
        + Biến y_k ∈ {0,1}, chọn đúng 1 marking reachable
        + Với mọi t: Σ_k enabled[t][k] * y_k = 0 (không t nào enabled)
    - Nếu ILP feasible -> marking chọn ra là deadlock reachable.
    """

    # Không có reachable marking
    if reach_bdd.is_zero():
        return None

    I = pn.I  # |T| x |P|
    O = pn.O
    place_ids = pn.place_ids
    n_trans, n_places = I.shape

    # ---------------------------------------------------------
    # 1) Liệt kê tất cả marking reachable từ BDD
    #    (kể cả expand các place không nằm trong support)
    # ---------------------------------------------------------
    support_vars = list(reach_bdd.support)
    name_to_var = {v.name: v for v in support_vars}
    support_names = set(name_to_var.keys())

    missing_place_ids = [pid for pid in place_ids if pid not in support_names]

    reachable_markings_set = set()
    reachable_markings: List[List[int]] = []

    for assignment in reach_bdd.satisfy_all():
        # assignment: {bddvar: 0/1} -> {name: 0/1}
        base_assign = {v.name: int(val) for v, val in assignment.items()}

        if not missing_place_ids:
            full_assign = base_assign
            m_vec = [full_assign.get(pid, 0) for pid in place_ids]
            t = tuple(m_vec)
            if t not in reachable_markings_set:
                reachable_markings_set.add(t)
                reachable_markings.append(m_vec)
        else:
            # Expand 0/1 cho các place không nằm trong support (don’t care)
            for bits in itertools.product([0, 1], repeat=len(missing_place_ids)):
                extra = dict(zip(missing_place_ids, bits))
                full_assign = dict(base_assign)
                full_assign.update(extra)

                m_vec = [full_assign.get(pid, 0) for pid in place_ids]
                t = tuple(m_vec)
                if t not in reachable_markings_set:
                    reachable_markings_set.add(t)
                    reachable_markings.append(m_vec)

    K = len(reachable_markings)
    if K == 0:
        return None

    reachable_arr = np.array(reachable_markings, dtype=int)  # K x P

    # ---------------------------------------------------------
    # 2) Precompute enabled[t][k]:
    #    t enabled tại M^(k) nếu:
    #      - M[p] >= I[t,p] (đủ token)
    #      - M_next = M - I_t + O_t nằm trong reachable_markings_set
    # ---------------------------------------------------------
    enabled = np.zeros((n_trans, K), dtype=int)

    for t in range(n_trans):
        need = I[t]                                # (P,)
        ok1 = (reachable_arr >= need).all(axis=1)  # (K,)

        M_next = reachable_arr - I[t] + O[t]       # (K,P)

        ok2 = np.array([
            tuple(M_next[k].tolist()) in reachable_markings_set
            for k in range(K)
        ])

        enabled[t] = (ok1 & ok2).astype(int)

    # ---------------------------------------------------------
    # 3) ILP: chọn deadlock từ tập reachable
    # ---------------------------------------------------------
    prob = pulp.LpProblem("Deadlock_On_Reachable", pulp.LpMinimize)

    y = [pulp.LpVariable(f"y_{k}", lowBound=0, upBound=1, cat="Binary")
         for k in range(K)]

    # chọn đúng 1 marking
    prob += pulp.lpSum(y[k] for k in range(K)) == 1

    # Deadlock: không transition nào enabled
    for t in range(n_trans):
        prob += pulp.lpSum(enabled[t][k] * y[k] for k in range(K)) == 0

    status = prob.solve(pulp.PULP_CBC_CMD(msg=False))
    if pulp.LpStatus[status] != "Optimal":
        return None

    # ---------------------------------------------------------
    # 4) Lấy marking được chọn (y_k = 1)
    # ---------------------------------------------------------
    chosen_k = None
    for k in range(K):
        val = y[k].value()
        if val is not None and val > 0.5:
            chosen_k = k
            break

    if chosen_k is None:
        return None

    return [int(x) for x in reachable_markings[chosen_k]]
