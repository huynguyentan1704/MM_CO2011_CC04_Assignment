# TASK 2 BTL MHH

**Explicit computation of reachable markings:** Implement a basic breadth-first search
(BFS) algorithm to enumerate all reachable 1-safety markings starting
from the initial marking.

## Requirements

- Tạo môi trường ảo (virtual environment)
```
python -m venv venv
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

---
<p align="center">
  <a href="https://www.facebook.com/Shiba.Vo.Tien">
    <img src="https://img.shields.io/badge/Facebook-1877F2?style=for-the-badge&logo=facebook&logoColor=white" alt="Facebook"/>
  </a>
  <a href="https://www.tiktok.com/@votien_shiba">
    <img src="https://img.shields.io/badge/TikTok-000000?style=for-the-badge&logo=tiktok&logoColor=white" alt="TikTok"/>
  </a>
  <a href="https://www.facebook.com/groups/khmt.ktmt.cse.bku?locale=vi_VN">
    <img src="https://img.shields.io/badge/Facebook%20Group-4267B2?style=for-the-badge&logo=facebook&logoColor=white" alt="Facebook Group"/>
  </a>
  <a href="https://www.facebook.com/CODE.MT.BK">
    <img src="https://img.shields.io/badge/Page%20CODE.MT.BK-0057FF?style=for-the-badge&logo=facebook&logoColor=white" alt="Facebook Page"/>
  </a>
  <a href="https://github.com/VoTienBKU">
    <img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"/>
  </a>
</p>
