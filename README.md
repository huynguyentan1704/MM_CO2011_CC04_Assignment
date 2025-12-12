# Symbolic and Algebraic Reasoning in Petri Nets 

```mermaid
flowchart TD

    %% Places (Tasks)
    P1(("TASK1"))
    P2(("TASK2"))
    P3(("TASK3"))
    P4(("TASK4"))
    P5(("TASK5"))

    %% Transitions (Dependencies)
    T12([Use T1 → T2])
    T13([Use T1 → T3])
    T34([Use T3 → T4])
    T135([Use T1,T3 → T5])

    %% Arcs
    %% Task1 -> Task2
    P1 --> T12
    T12 --> P2

    %% Task1 -> Task3
    P1 --> T13
    T13 --> P3

    %% Task3 -> Task4
    P3 --> T34
    T34 --> P4

    %% Task1, Task2, Task3 -> Task5
    P1 --> T135
    P2 --> T135
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
<p align="center">
  <img src = "https://github.com/huynguyentan1704/MHH_win-to-win/blob/task6/run_code.png"/>
</p>

##  Running tests

- Run all tests
```sh
python -m pytest tests/ -v
```
<p align="center">
  <img src = "https://github.com/huynguyentan1704/MHH_win-to-win/blob/task6/run_test_all.png"/>
</p>


- Run a single test File (PetriNet)

```sh
python -m pytest tests/test_petriNet.py -v
```
<p align="center">
  <img src = "https://github.com/huynguyentan1704/MHH_win-to-win/blob/task6/run_test_PetriNet.png"/>
</p>

- Run a single test File (BDD)

```sh
python -m pytest tests/test_BDD.py -v
```
<p align="center">
  <img src = "https://github.com/huynguyentan1704/MHH_win-to-win/blob/task6/run_test_BDD.png"/>
</p>
