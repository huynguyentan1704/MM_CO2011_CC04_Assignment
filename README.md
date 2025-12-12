# TASK 1 BTL MHH

**Reading Petri nets from PNML files**: Implement a parser that reads a 1-safe Petri
net from a standard PNML file1 and constructs the internal representation of places,
transitions, and flow relations. The program should verify consistency (e.g., no missing
arcs or nodes).

https://www.pnml.org/version-2009/version-2009.php

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
  <img src = "https://github.com/huynguyentan1704/MHH_win-to-win/blob/task1/run_code.png"/>
</p>

##  Running tests

- Run all tests
```sh
python -m pytest tests/ -v
```
<p align="center">
  <img src = "https://github.com/huynguyentan1704/MHH_win-to-win/blob/task1/run_test.png"/>
</p>


- Run a single test File 

```sh
python -m pytest tests/test_petriNet.py -v
```
