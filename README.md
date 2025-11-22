# TASK 2 BTL MHH

**Explicit computation of reachable markings:** Implement a basic breadth-first search
(BFS) or depth-first search (DFS) algorithm to enumerate all reachable markings starting
from the initial marking

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
python3 -m pytest -vv test_DFS.py

python3 -m pytest -vv test_BFS.py
```

- Run a single test function

```
python3 -m pytest -vv test_DFS.py::test_001
```