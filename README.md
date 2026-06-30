# Password Checking Maximum Coverage

Project nay mo hinh hoa bai toan password checking thanh **Maximum Coverage**.
Muc tieu la chon dung `k` rules de phu duoc nhieu real passwords nhat co the.

## Algorithms

Project hien co 6 solver:

1. Brute Force
2. Greedy
3. Dynamic Programming
4. ILP + PuLP + CBC
5. Randomized Search
6. Hill Climbing

## Files

- `__init__.py`: diem vao chuong trinh
- `pwd_checking.py`: menu chon solver
- `coverage_problem.py`: logic core va tat ca solver
- `rules.py`: danh sach 20 rules
- `algorithms/`: wrapper cho tung solver
- `real_passwords.txt`: tap password that
- `mutated_passwords.txt`: tap password bien doi

## Quick Start

### 1. Cai dependency

```bash
pip install -r requirements.txt
```

### 2. Chay project

```bash
python __init__.py
```

Neu dung virtualenv cua repo, chay:

```bash
.venv\Scripts\python.exe __init__.py
```

## Menu

### Rules menu

- `1` to `20`: chon so rules `k`
- `0` hoac `e`: thoat

### Algorithm menu

- `1`: Brute Force
- `2`: Greedy
- `3`: Dynamic Programming
- `4`: ILP + PuLP + CBC
- `5`: Randomized Search
- `6`: Hill Climbing
- `0`: quay lai
- `-1` hoac `e`: thoat

## Output

Moi solver ghi ket qua ra mot file rieng, vi du:

- `output_brute_k3.txt`
- `output_greedy_k3.txt`
- `output_dp_k3.txt`
- `output_ILP_PuLP_CBC_k3.txt`
- `output_randomized_k3.txt`
- `output_hill_k3.txt`

## Notes

- `pulp` la dependency cho solver ILP.
- Project dung `set` va `frozenset`, khong dung bitmask so nguyen.
- Tat ca tai lieu khac trong repo deu nen khop voi 6 solver tren.
