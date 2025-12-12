import time
from src.PetriNet import PetriNet
from src.BDD import bdd_reachable
from src.Optimization import max_reachable_marking
from src.BFS import bfs_reachable
from src.DFS import dfs_reachable
from src.Deadlock import deadlock_reachable_marking
import numpy as np
from pyeda.inter import *

def main():
    # ------------------------------------------------------
    # 1. Load Petri Net from PNML file
    # ------------------------------------------------------
    filename = "example.pnml"
    print(f"Loading PNML: {filename}...")

    t_start = time.time()  # Start Timer
    pn = PetriNet.from_pnml(filename)
    t_end = time.time()    # Stop Timer
    
    print("\n--- Petri Net Loaded ---")
    print(f"Time taken: {t_end - t_start:.6f} seconds")
    print(pn)

    # ------------------------------------------------------
    # 2. BFS reachable
    # ------------------------------------------------------
    print("\n--- BFS Reachable Markings ---")
    
    t_start = time.time()
    bfs_set = bfs_reachable(pn)
    t_end = time.time()
    
    for m in bfs_set:
        print(np.array(m))
    print("Total BFS reachable =", len(bfs_set))
    print(f"Time taken: {t_end - t_start:.6f} seconds")

    # ------------------------------------------------------
    # 3. DFS reachable
    # ------------------------------------------------------
    print("\n--- DFS Reachable Markings ---")
    
    t_start = time.time()
    dfs_set = dfs_reachable(pn)
    t_end = time.time()
    
    for m in dfs_set:
        print(np.array(m))
    print("Total DFS reachable =", len(dfs_set))
    print(f"Time taken: {t_end - t_start:.6f} seconds")

    # ------------------------------------------------------
    # 4. BDD reachable
    # ------------------------------------------------------
    print("\n--- BDD Reachable ---")
    
    t_start = time.time()
    bdd, count = bdd_reachable(pn)
    t_end = time.time()
    
    print("Satisfying all:", list(bdd.satisfy_all()))
    print("Minimized =", espresso_exprs(bdd2expr(bdd)))
    print("BDD reachable markings =", count)
    print(f"Time taken: {t_end - t_start:.6f} seconds")

    # ------------------------------------------------------
    # 5. Deadlock detection
    # ------------------------------------------------------
    print("\n--- Deadlock reachable marking ---")
    
    t_start = time.time()
    dead = deadlock_reachable_marking(pn, bdd)
    t_end = time.time()
    
    if dead is not None:
        print("Deadlock marking:", dead)
    else:
        print("No deadlock reachable.")
    print(f"Time taken: {t_end - t_start:.6f} seconds")

    # ------------------------------------------------------
    # 6. Optimization: maximize c·M
    # ------------------------------------------------------
    # Note: Make sure the size of 'c' matches the number of places in your PNML!
    c = np.array([1, -2, 3, -1, 1, 2]) 
    
    # Auto-adjust c if it doesn't match the Petri Net size to prevent crash
    if len(c) != len(pn.place_ids):
        print(f"\n[Warning] adjusting weight vector c from size {len(c)} to {len(pn.place_ids)}")
        c = np.ones(len(pn.place_ids), dtype=int)

    print("\n--- Optimize c·M ---")
    
    t_start = time.time()
    max_mark, max_val = max_reachable_marking(
        pn.place_ids, bdd, c
    )
    t_end = time.time()
    
    print("c:", c)
    print("Max marking:", max_mark)
    print("Max value:", max_val)
    print(f"Time taken: {t_end - t_start:.6f} seconds")


if __name__ == "__main__":
    main()