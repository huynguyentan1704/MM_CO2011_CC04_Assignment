# MHH Win-to-Win – BTL HK251 Tasks

This repository contains multiple tasks for the BTL HK251 course.  
Each task is stored on a separate Git branch:

- `task1`
- `task2`
- `task3`
- `task4`
- `task5`
- `task6`

You can choose to work with:

- **Conda** (Python 3.9.20), or  
- **Built-in virtual environment (venv)**

Each task can be cloned individually or the entire repo can be cloned once and switched branches.

---

## 1. Clone Tasks

### Option A — Clone repo once and switch branches

```bash
git clone https://github.com/huynguyentan1704/MHH_win-to-win.git
cd MHH_win-to-win

# List branches
git branch -a

# Checkout branch for each task
git checkout task1
# git checkout task2
# git checkout task3
# git checkout task4
# git checkout task5
# git checkout task6
Option B — Clone each task into its own folder
bash
Copy code
git clone -b task1 --single-branch https://github.com/huynguyentan1704/MHH_win-to-win.git task1
git clone -b task2 --single-branch https://github.com/huynguyentan1704/MHH_win-to-win.git task2
git clone -b task3 --single-branch https://github.com/huynguyentan1704/MHH_win-to-win.git task3
git clone -b task4 --single-branch https://github.com/huynguyentan1704/MHH_win-to-win.git task4
git clone -b task5 --single-branch https://github.com/huynguyentan1704/MHH_win-to-win.git task5
git clone -b task6 --single-branch https://github.com/huynguyentan1704/MHH_win-to-win.git task6
2. Environment Setup
You only need ONE environment: Conda or venv.

2.1. Setup using Conda (Python 3.9.20)
Create environment
bash
Copy code
conda create -n mhh_btl_env python=3.9.20
Activate environment
bash
Copy code
conda activate mhh_btl_env
Install dependencies for the task
bash
Copy code
pip install -r requirements.txt
Make sure you are inside the correct task folder or branch.

2.2. Setup using built-in venv (no Conda required)
Create venv
bash
Copy code
python3 -m venv venv
Activate venv
macOS / Linux

bash
Copy code
source venv/bin/activate
Windows (PowerShell)

bash
Copy code
venv\Scripts\Activate.ps1
Windows (CMD)

bash
Copy code
venv\Scripts\activate.bat
Install dependencies
bash
Copy code
pip install -r requirements.txt
3. Running the Code
Run from task folder:

bash
Copy code
python main.py
Or run tests:

bash
Copy code
pytest -vv
Or:

bash
Copy code
python -m pytest tests/ -v
(Some tasks use run.py or custom test files — check the task folder.)
