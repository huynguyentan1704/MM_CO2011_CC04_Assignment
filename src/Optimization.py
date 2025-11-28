# src/Optimization.py

from typing import List, Optional, Tuple
import numpy as np
from pyeda.inter import BinaryDecisionDiagram


def max_reachable_marking(
    P: List[str],
    bdd: BinaryDecisionDiagram,
    c: np.ndarray,
) -> Tuple[Optional[List[int]], Optional[int]]:
    """
    Maximize c^T M over all 0/1-markings M that satisfy the BDD `bdd`.

    Tối ưu cục bộ đã dùng:
    - Special-case: bdd == 1
    - Bound chỉ cộng trọng số dương của biến trong BDD.support
    - Greedy cho biến không xuất hiện trong support
    - Thứ tự nhánh phụ thuộc dấu trọng số (ưu tiên nhánh "hứa hẹn" hơn)
    - Cache restrict(node, var, val)

    Parameters
    ----------
    P   : list[str]
        Danh sách tên place, thứ tự dùng cho vector marking.
    bdd : BinaryDecisionDiagram
        BDD biểu diễn tập reachable markings.
    c   : np.ndarray
        Vector trọng số (shape (len(P),)).

    Returns
    -------
    marking : list[int] or None
        Marking tối ưu (0/1 theo thứ tự P), hoặc None nếu BDD không thỏa được.
    value   : int or None
        Giá trị max c^T M, hoặc None nếu không có marking.
    """
    n = len(P)
    if c.shape[0] != n:
        raise ValueError("Length of c must equal number of places P")

    weights = [int(v) for v in c]

    # 1) BDD = 0 -> vô nghiệm
    if bdd.is_zero():
        return None, None

    # 2) BDD = 1 -> mọi marking đều hợp lệ, chọn greedy theo dấu trọng số
    if bdd.is_one():
        marking = [1 if w > 0 else 0 for w in weights]
        value = int(np.dot(weights, marking))
        return marking, value

    # 3) Chuẩn bị info về support (các biến thực sự xuất hiện trong BDD)
    support = getattr(bdd, "support", frozenset())
    var_in_bdd = {v.name: v for v in support}              # name -> BDDVariable
    in_support = [P[i] in var_in_bdd for i in range(n)]    # bool list

    # 4) suffix_pos[i] = tổng trọng số dương của các biến trong support từ i..n-1
    suffix_pos = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        if in_support[i] and weights[i] > 0:
            suffix_pos[i] = suffix_pos[i + 1] + weights[i]
        else:
            suffix_pos[i] = suffix_pos[i + 1]

    best_value: Optional[int] = None
    best_marking: Optional[List[int]] = None
    current = [0] * n

    # 5) Cache cho restrict để tránh gọi lại nhiều lần
    restrict_cache = {}

    def restrict_node(node: BinaryDecisionDiagram, var_obj, val: int) -> BinaryDecisionDiagram:
        key = (id(node), id(var_obj), val)
        if key in restrict_cache:
            return restrict_cache[key]
        new_node = node.restrict({var_obj: val})
        restrict_cache[key] = new_node
        return new_node

    def dfs(node: BinaryDecisionDiagram, idx: int, partial: int) -> None:
        """
        node   : BDD sau khi đã gán P[0..idx-1]
        idx    : đang xét place P[idx]
        partial: giá trị c^T M với các biến đã gán
        """
        nonlocal best_value, best_marking

        # Không còn nghiệm
        if node.is_zero():
            return

        # Đã gán hết biến: nếu node != 0 thì đây là một nghiệm hợp lệ
        if idx == n:
            if not node.is_zero():
                if best_value is None or partial > best_value:
                    best_value = partial
                    best_marking = current.copy()
            return

        # Upper bound từ đây trở đi
        bound = partial + suffix_pos[idx]
        if best_value is not None and bound <= best_value:
            return

        var_name = P[idx]
        w = weights[idx]

        # Biến không xuất hiện trong support: BDD không phụ thuộc nó
        # → Greedy: nếu w > 0 thì set 1, ngược lại set 0
        if not in_support[idx]:
            if w > 0:
                current[idx] = 1
                dfs(node, idx + 1, partial + w)
            else:
                current[idx] = 0
                dfs(node, idx + 1, partial)
            return

        # Biến có trong support -> cần rẽ 2 nhánh
        var_obj = var_in_bdd[var_name]

        # Quyết định nhánh nào xét trước: nếu w >= 0, thử HIGH trước.
        if w >= 0:
            # Nhánh HIGH (var = 1)
            current[idx] = 1
            high_node = restrict_node(node, var_obj, 1)
            dfs(high_node, idx + 1, partial + w)

            # Nhánh LOW (var = 0)
            current[idx] = 0
            low_node = restrict_node(node, var_obj, 0)
            dfs(low_node, idx + 1, partial)
        else:
            # Trọng số âm -> thử LOW trước (thường tốt hơn)
            current[idx] = 0
            low_node = restrict_node(node, var_obj, 0)
            dfs(low_node, idx + 1, partial)

            current[idx] = 1
            high_node = restrict_node(node, var_obj, 1)
            dfs(high_node, idx + 1, partial + w)

    dfs(bdd, 0, 0)

    return best_marking, best_value
