from src.PetriNet import PetriNet
from src.BFS import bfs_reachable
import numpy as np

if __name__ == "__main__":
    P = ["p1", "p2", "p3"]
    T = ["t1", "t2", "t3"]
    I = np.array([[1,0,0],
                  [0,1,0],
                  [0,0,1]])
    O = np.array([[0,1,0],
                  [0,0,1],
                  [1,0,0]])
    M0 = np.array([1,0,1])

    output= bfs_reachable(PetriNet(P, T, P, T, I, O, M0))

    expected = {
        (1, 1, 0),
        (0, 1, 1),
        (1, 0, 1)
    }
    print("Output:", output)