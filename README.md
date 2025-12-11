# TASK 4 BTL MHH

**Deadlock detection by using ILP and BDD:** Combine ILP formulation and the
BDD obtained in Task 3 to detect a deadlock if it exists. More specifically, output one
deadlock if found, otherwise report none. Note that a dead marking is a marking where
no transition is enabled, whereas a deadlock is a dead marking that is reachable from the
initial marking [17]. Report the running time on some example models.

## Requirements

- Tạo môi trường ảo (virtual environment)
```
python3 -m venv venv
```

- Kích hoạt môi trường ảo
```
# Windows
venv\Scripts\Activate.ps1

# Linux / macOS:
source venv/bin/activate
```

- Cài đặt các thư viện từ `requirements.txt`
```
pip install -r requirements.txt
```


##  Running tests

- Run all tests
```
python3 -m pytest -vv test_Deadlock.py
```

- Run a single test function

```
python3 -m pytest -vv test_Deadlock.py::test_001
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
## Output
<p align="center">
  <img src="images/bdd.png" alt="BDD" width="500">
</p>

<p align="center">
  <img src="images/OP_testcase.png" alt="OP Testcase" width="500">
</p>

<p align="center">
  <img src="images/OP_run.png" alt="OP Run" width="500">
</p>
