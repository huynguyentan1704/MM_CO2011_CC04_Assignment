# TASK 5 BTL MHH

**Optimization over reachable markings:** Given a linear objective function
maximize c⊤M, M ∈Reach(M0),
where Reach(M0) denotes the set of markings reachable from the initial marking M0 and c
assigns integer weights to places, determine a reachable marking if it exists that optimizes
the objective function. If there is no such a marking, report none. Report the running
time on some example models.

## Requirements

- Create a virtual environment
```
python3 -m venv venv
```

- Virtual Environment activation
```
# Windows
venv\Scripts\Activate.ps1

# Linux / macOS:
source venv/bin/activate
```

- Install libraries from `requirements.txt`
```
pip install -r requirements.txt
```


##  Running tests

- Run all tests
```
python3 -m pytest -vv test_Optimization.py
```

- Run a single test function

```
python3 -m pytest -vv test_Optimization.py::test_001
```
## Running run.py
Make sure you have Python 3.8+ installed.
Install required packages:
```
pip install pyeda graphviz pytest
```

You must also install Graphviz on your system so that .png images can be generated.

To generate the BDD visualization and the minimized Boolean expression, run:
```
python run.py
```
This file is used to visualize and analyze the logical structure of reachable markings.
## Outputs

<img width="184" height="479" alt="image" src="https://github.com/user-attachments/assets/eb6dc9a9-49c2-4c2d-9899-9e3962cbe621" />

<img width="1253" height="240" alt="image" src="https://github.com/user-attachments/assets/550e13a2-f883-404d-813f-79403df1dfb6" />

<img width="706" height="125" alt="image" src="https://github.com/user-attachments/assets/13c04220-3ff3-4bc4-a296-ef73f6972df7" />

