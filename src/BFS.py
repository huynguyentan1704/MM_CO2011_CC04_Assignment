from collections import deque
import numpy as np
from .PetriNet import PetriNet
from typing import Set, Tuple


def bfs_reachable(pn: PetriNet) -> Set[Tuple[int, ...]]:
    """
    Tính tập reachable markings từ M0 của PetriNet bằng BFS.

    Giả định:
        - pn.I: shape (T, P)  # mỗi hàng là 1 transition (input)
        - pn.O: shape (T, P)  # mỗi hàng là 1 transition (output)
        - pn.M0: shape (P,)   # marking ban đầu (mỗi phần tử là token của 1 place)

    Net là 1-safe:
        - Nếu firing làm xuất hiện token > 1 ở bất kỳ place nào,
          thì transition đó KHÔNG HỢP LỆ tại marking hiện tại.
    """
    I = pn.I       # (T, P)
    O = pn.O       # (T, P)
    M0 = pn.M0     # (P,)

    if I is None or O is None or M0 is None:
        raise ValueError("PetriNet must have I, O, M0 initialized")

    num_trans, num_places = I.shape

    start = tuple(int(x) for x in M0.tolist())

    visited: Set[Tuple[int, ...]] = set()
    queue: deque[Tuple[int, ...]] = deque()

    visited.add(start)
    queue.append(start)

    while queue:
        current = queue.popleft()
        M = np.array(current, dtype=int)  # (P,)

        # thử bắn TẤT CẢ transition tại marking hiện tại
        for t in range(num_trans):
            need = I[t, :]  # tokens cần ở mỗi place để bắn t

            # check enabled theo input: M >= need
            if not np.all(M >= need):
                continue

            # firing: M' = M - need + O[t, :]
            M_new = M - need + O[t, :]

            # 1-safe net: nếu place nào >1 token → trạng thái không hợp lệ
            if np.any(M_new < 0) or np.any(M_new > 1):
                continue

            m_tuple = tuple(int(x) for x in M_new.tolist())

            if m_tuple not in visited:
                visited.add(m_tuple)
                queue.append(m_tuple)

    return visited
