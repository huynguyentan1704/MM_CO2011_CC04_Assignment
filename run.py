from src.PetriNet import PetriNet
from src.BDD import bdd_reachable
from pyeda.inter import *
import numpy as np
import time

def main():
    # ------------------------------------------------------
    # 1. Load Petri Net từ file PNML
    # ------------------------------------------------------
    filename = "example.pnml"
    print("Loading PNML:", filename)

    t0 = time.time()
    pn = PetriNet.from_pnml(filename)
    t1 = time.time()

    print(f"[TIME] Load PNML: {t1 - t0:.6f} s")
    print("\n--- Petri Net Loaded ---")
    print(pn)

    # ------------------------------------------------------
    # 4. BDD reachable
    # ------------------------------------------------------
    print("\n--- BDD Reachable ---")
    t0 = time.time()
    bdd, count = bdd_reachable(pn)
    t1 = time.time()
    print(f"[TIME] BDD reachable: {t1 - t0:.6f} s")

    print("Satisfying all:", list(bdd.satisfy_all()))
    print("Minimized =", espresso_exprs(bdd2expr(bdd)))
    print("BDD reachable markings =", count)


if __name__ == "__main__":
    main()
