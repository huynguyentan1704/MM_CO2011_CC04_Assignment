# MHH Win-to-Win – BTL HK251 Tasks

This repository contains multiple tasks for the BTL HK251 course.  
Each task is stored on a separate Git branch:

- task1  
- task2  
- task3  
- task4  
- task5  
- task6  

You can choose to work with:

- Conda (Python 3.9.20), or  
- Built-in virtual environment (venv)

Each task can be cloned individually or the entire repo can be cloned once and switched branches.

---

## 1. Clone Tasks

### Option A — Clone repo once and switch branches

```bash
git clone https://github.com/huynguyentan1704/MHH_win-to-win.git
cd MHH_win-to-win

git branch -a

git checkout task1
# git checkout task2
# git checkout task3
# git checkout task4
# git checkout task5
# git checkout task6
```

---

### Option B — Clone each task into its own folder

```bash
git clone -b task1 --single-branch https://github.com/huynguyentan1704/MHH_win-to-win.git task1
git clone -b task2 --single-branch https://github.com/huynguyentan1704/MHH_win-to-win.git task2
git clone -b task3 --single-branch https://github.com/huynguyentan1704/MHH_win-to-win.git task3
git clone -b task4 --single-branch https://github.com/huynguyentan1704/MHH_win-to-win.git task4
git clone -b task5 --single-branch https://github.com/huynguyentan1704/MHH_win-to-win.git task5
git clone -b task6 --single-branch https://github.com/huynguyentan1704/MHH_win-to-win.git task6
```

---

## 2. Environment Setup

Choose ONE of the two methods below.

---

## 2.1. Setup using Conda (Python 3.9.20)

### Create environment

```bash
conda create -n mhh_btl_env python=3.9.20
```

### Activate environment

```bash
conda activate mhh_btl_env
```

### Install requirements

```bash
pip install -r requirements.txt
```

---

## 2.2. Setup using built-in venv (virtual environment)

### Create venv

```bash
python3 -m venv venv
```

### Activate venv

macOS / Linux:
```bash
source venv/bin/activate
```

Windows PowerShell:
```bash
venv\Scripts\Activate.ps1
```

Windows CMD:
```bash
venv\Scripts\activate.bat
```

### Install requirements

```bash
pip install -r requirements.txt
```

---

## 3. Running Code

```bash
python main.py
```

Running tests:

```bash
pytest -vv
```

or:

```bash
python -m pytest tests/ -v
```

---

## 4. Summary

1. Clone repo (one repo → switch branches, or separate clones per task)  
2. Create Conda env or venv  
3. Activate environment  
4. Install dependencies  
5. Run code or tests  

---

## 5. Notes

- Required Python version: 3.9.x  
- Conda env name: mhh_btl_env  
- venv folder name: venv  
- Each task lives on its own Git branch to avoid conflicts  
