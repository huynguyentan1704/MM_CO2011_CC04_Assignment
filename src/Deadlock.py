import collections
from typing import Tuple, List, Optional
from pyeda.inter import *
from collections import deque
from .PetriNet import PetriNet
import numpy as np

def deadlock_reachable_marking(
    pn: PetriNet, 
    bdd: BinaryDecisionDiagram, 
) -> Optional[List[int]]:
    pass