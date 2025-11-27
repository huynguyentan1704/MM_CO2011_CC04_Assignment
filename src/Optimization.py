import collections
from typing import Tuple, List, Optional
from pyeda.inter import *
from collections import deque
import numpy as np

def max_reachable_marking(
    place_ids: List[str], 
    bdd: BinaryDecisionDiagram, 
    c: np.ndarray
) -> Tuple[Optional[List[int]], Optional[int]]:
    pass