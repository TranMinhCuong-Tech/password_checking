# Wiki: Password Checking Maximum Coverage

## 1. Overview

Project nay dung de minh hoa cach bien mot bai toan check password thanh bai toan toi uu to hop.
Thay vi tim tung password bang tay, project:

- doc `real_passwords.txt` va `mutated_passwords.txt`
- coi moi rule la mot phep bien doi chuoi
- xay dung tap phu cho tung rule
- chon dung `k` rules sao cho so password that duoc phu la lon nhat

Bai toan trung tam la **Maximum Coverage**.

## 2. Du lieu dau vao

### 2.1. `real_passwords.txt`

Day la universe `U`.
Moi dong la mot password that.

### 2.2. `mutated_passwords.txt`

Day la tap candidate sau khi bien doi.
Neu mot rule sinh ra mot candidate co mat trong tap nay, password that tuong ung duoc xem la covered.

### 2.3. Quy mo hien tai

- 500 real passwords
- 1500 mutated passwords
- 20 rules trong `rules.py`

## 3. Mo hinh Maximum Coverage

Goi:

- `U` la tap tat ca real passwords
- `S_i` la tap cac password that ma rule `i` co the cover
- `k` la so rule duoc phep chon

Muc tieu:

```text
maximize |S_i1 U S_i2 U ... U S_ik|
subject to choose exactly k rules
```

Y nghia:

- co the overlap giua cac tap con
- mot rule tot rieng le chua chac tot khi dat cung nhung rule khac
- bai toan can can bang giua coverage va overlap

## 4. Cach code mo hinh hoa bai toan

### 4.1. `rules.py`

File nay dinh nghia 20 rules. Moi rule co:

- `name`
- `label`
- `transform`

### 4.2. `coverage_problem.py`

Day la file trung tam.
No chua:

- `load_passwords()`
- `build_rule_coverages()`
- `coverage_of_rules()`
- `coverage_counts()`
- `result_payload()`
- `run_solver()`
- cac solver cua project

Quan trong nhat:

- `rule_coverages[rule_id]` la `frozenset` chi so password that duoc rule do cover
- `password_to_rules[index]` la danh sach rule co the cover password do

### 4.3. `pwd_checking.py`

Day la menu chon solver.
No:

- tai du lieu
- in menu
- map lua chon sang module wrapper
- goi `solve_max_coverage(k, passwords)`

### 4.4. `algorithms/`

Moi file trong `algorithms/` chi la wrapper mỏng cho mot solver:

- `Brute_Force.py`
- `Greedy.py`
- `Dynamic_Programming.py`
- `ILP_PuLP_CBC.py`
- `Randomized_Search.py`
- `Hill_Climbing.py`

## 5. Danh sach 6 solver

### 5.1. Brute Force

Thu tat ca to hop dung `k` rules.
Day la exact solver co ban nhat.

### 5.2. Greedy

Moi buoc chon rule co marginal gain lon nhat.
Nhanh, de hieu, thuong cho ket qua tot tren dataset nay.

### 5.3. Dynamic Programming

Dung memoization de tranh tinh lai trang thai da gap.
Exact solver, nhung state space tang rat nhanh.

### 5.4. ILP + PuLP + CBC

Mo hinh hoa bai toan thanh 0-1 ILP:

- `x_i` = co chon rule `i` hay khong
- `y_j` = password `j` co duoc cover hay khong

Day la exact solver neu CBC giai toi uu thanh cong.

### 5.5. Randomized Search

Lay mau nhieu tap `k` rules ngau nhien va giu phuong an tot nhat.

### 5.6. Hill Climbing

Khoi dau tu loi giai tot, sau do thu cac swap `1-1` de tang coverage.

## 6. Luong chay

1. Chay `__init__.py`
2. Hien thi banner va catalog rules
3. Nguoi dung chon `k`
4. Chon solver
5. `pwd_checking.py` tai du lieu
6. Solver duoc chon duyet `coverage_problem.py`
7. Ket qua duoc in ra va luu vao file output

## 7. Output format

Moi ket qua gom:

- solver name
- `k`
- danh sach rules da chon
- danh sach password duoc cover
- so luong cover / tong so password

`save_answer()` trong `coverage_problem.py` ghi cac thong tin nay vao file.

## 8. Ghi chu

- Project khong dung bitmask
- Project hien tai chi giu 6 solver trong menu
- `pulp` la dependency bat buoc cho solver ILP
- `real_passwords.txt` va `mutated_passwords.txt` la 2 file input chinh
