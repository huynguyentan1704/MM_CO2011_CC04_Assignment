# Symbolic and Algebraic Reasoning in Petri Nets 

```mermaid
flowchart TD

    %% Places
    P1(("TASK1"))
    P2(("TASK2"))
    P3(("TASK3"))
    P4(("TASK4"))
    P5(("TASK5"))

    %% Transitions
    T12([T1_to_T2])
    T13([T1_to_T3])
    T134([T1_T3_to_T4])
    T135([T1_T3_to_T5])

    %% Arcs
    P1 --> T12
    T12 --> P2

    P1 --> T13
    T13 --> P3

    P1 --> T134
    P3 --> T134
    T134 --> P4

    P1 --> T135
    P3 --> T135
    T135 --> P5
```

## Requirements

- Create virtual environment
```sh
python3 -m venv venv
```

- Activate virtual environment
```sh
# Windows
venv\Scripts\Activate.ps1

# Linux / macOS:
source venv/bin/activate
```

- Install required library from `requirements.txt`
```sh
pip install -r requirements.txt
```

## Running Code

```sh
python run.py
```

##  Running tests

- Run all tests
```sh
python -m pytest tests/ -v
```
(I want to add run_test_all.png picture)

- Run a single test File (PetriNet)

```sh
python -m pytest tests/test_petriNet.py -v
```

- Run a single test File (BDD)

```sh
python -m pytest tests/test_BDD.py -v
```