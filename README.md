# TASK 2 BTL MHH

**Explicit computation of reachable markings:** Implement a basic breadth-first search
(BFS) algorithm to enumerate all reachable 1-safety markings starting
from the initial marking.

## Requirements

- Create virtual environment
```
python -m venv venv
```

- Activate virtual environment
```
# Windows
venv\Scripts\Activate.ps1

# Linux / macOS:
source venv/bin/activate
```

- Install required library from `requirements.txt`
```
pip install -r requirements.txt
```
## Visualization
<p align="center">
  <img src = "task2.jpg"/>
</p>


##  Running tests

- Run run.py
```
python run.py
```
<p align="center">
  <img src = "https://github.com/user-attachments/assets/b4bcd905-4edc-4333-a8e3-3e44c93af1d5"/>
</p>

- Run all BFS test

```
python -m pytest -vv test_BFS.py
```
<p align="center">
  <img src = "https://github.com/user-attachments/assets/0d2ef84e-fb01-4d82-b9c8-a92d5d3247df"/>
</p>

- Run a single BFS test
```
python -m pytest -vv test_BFS.py::test_001
```
<p align="center">
  <img src = "https://github.com/user-attachments/assets/f508acc3-0611-4a1d-94f0-7fbb2e61de07"/>
</p>
