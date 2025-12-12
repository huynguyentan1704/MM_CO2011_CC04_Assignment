# MM 251 – Assignment
- Task 1 PNML Parsing: Reads and parses a Petri Net from a PNML file, extracting places, transitions, arcs, and initial markings.

- Task 2 Reachability (BFS/DFS): Computes the reachable markings of the Petri Net using explicit-state search via BFS and DFS.

- Task 3 BDD Reachability Analysis: Uses Binary Decision Diagrams (BDD) to compute the symbolic reachable state space efficiently.

- Task 4 Deadlock Detection: Identifies deadlock markings by checking reachable states where no transition is enabled.

- Task 5 Optimization (Max cᵀM): Finds the maximum value of a weighted marking using exhaustive search and Branch-and-Bound pruning.

- Task 6 Full Project Runner: Runs all components together: parsing, reachability (BFS/DFS/BDD), deadlock detection, and optimization.

## Workload
| Name               | Student ID | Task            |
|--------------------|------------|-----------------|
| Nguyen Cong Thanh  | 2353100    | Task 1, Task 6  |
| Ngo Quoc Hung      | 2352432    | Task 2          |
| Nguyen Tan Huy     | 2252258    | Task 3          |
| Le Minh Tri        | 2353228    | Task 4          |
| Nguyen Dang Khoa   | 2452543    | Task 5          |


## Repository Design

This repository is organized using a branch-per-task structure.  
Each task required in the BTL HK251 assignment is implemented on its own Git branch:

- `task1` – PNML parsing  
- `task2` – BFS/DFS reachability  
- `task3` – BDD reachability  
- `task4` – Deadlock detection  
- `task5` – Optimization (max cᵀM)  
- `task6` – Full project runner - the final source for submit

All branches share the same base layout so that each task can be developed and tested independently while still building on the same underlying Petri Net model.

At the root level, the repository includes:

- a unified `src/` folder containing core logic (Petri Net, BFS/DFS, BDD, Optimization, etc.),  
- a `tests/` folder for validation,  
- and a single `main.py` file whose behavior changes depending on the branch.

This design ensures:
- **modularity** (each task works on its own branch),  
- **reusability** (common code stays in `src/`),  
- **clean separation** between assignment requirements,  
- and **consistent structure** across all tasks.

Branch-Specific Operations & Demo Notes:
Each branch contains only the implementations required for that task,but all branches rely on the shared environment described below.

# Environment Setup

You can set up the environment in one of the following ways:

### Option 1 – Conda (recommended)

```bash
conda create -n mhh_btl_env python=3.9.20
conda activate mhh_btl_env
pip install -r requirements.txt
```

### Option 2 – Built-in venv
```bash
python3 -m venv venv
```

```bash
source venv/bin/activate  #macOS / Linux
venv\Scripts\Activate.ps1 #Windows PowerShell
venv\Scripts\activate.bat #Windows CMD
```

then
```bash
pip install -r requirements.txt
```

### Option 3 – Docker
This repository includes a ready-to-use **Dockerfile** that allows you to run all tasks without installing Python or dependencies on your local machine.  
The Docker image contains:

- Python 3.9  
- All required libraries from `requirements.txt`  
- The project source code mounted at runtime  

This ensures that every task (task1 → task6) runs in a clean and identical environment.

## Version & Dependencies

This project is implemented using **Python 3.9.x**, which is required for full compatibility with the Petri Net libraries used (especially `pyeda`).  
All tasks share the same dependency set, installed automatically from `requirements.txt`.

### Python Version
- **Python 3.9.x** (strictly required)  
  PyEDA and some BDD backends do not support Python 3.10+.

### Required Libraries

| Library | Purpose |
|--------|---------|
| **numpy** | Matrix operations, Pre/Post/Incidence matrices |
| **pyeda** | Binary Decision Diagrams (BDD) for symbolic reachability |
| **pytest** | Automated unit testing for all tasks |
| **xml.etree.ElementTree** | Parsing PNML files (places, transitions, arcs) |
| **collections** | BFS/DFS queues, deques |
| **typing** | Type annotations |
| **pulp** | Optimization framework (only for certain variants) |

### Installation
All dependencies can be installed via:

```bash
pip install -r requirements.txt


