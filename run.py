from src.PetriNet import PetriNet


if __name__ == "__main__":
    pn = PetriNet.from_pnml("tests/test_2/example.pnml")
    print(pn)