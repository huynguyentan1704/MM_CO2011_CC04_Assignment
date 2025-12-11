from collections import deque
import numpy as np
from .PetriNet import PetriNet 
from typing import Set, Tuple, Deque

def bfs_safe_reachable(pn:PetriNet) -> Set[Tuple[int,...]]:

    I = pn.I
    O = pn.O
    M0 = pn.M0

    # Check valid I, O, M0:
    if I is None or O is None or M0 is None:
        raise ValueError("Invalid I, O or M0 in PetriNet")
    
    C = O - I #Incidence Matrix

    numTrans, numPlaces = I.shape

    # Set Initial
    start = tuple(M0.astype(int).tolist())
    visited: Set[Tuple[int,...]] = {start}
    queue: deque[tuple[int,...]] = deque([start])

    while queue:
        current_queue = queue.popleft()
        M = np.array(current_queue, dtype=np.int8)

        for t in range(numTrans):
            need = I[t,:]

            if np.all(M >= need):
                M_prime = M + C[t,:]

                if np.all(M_prime >= 0) and np.all(M_prime <= 1):
                    M_tuple = tuple(M_prime.tolist())
                    
                    if M_tuple not in visited:
                        visited.add(M_tuple)
                        queue.append(M_tuple)
    return visited
