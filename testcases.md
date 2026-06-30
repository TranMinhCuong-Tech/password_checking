# Test Cases for Password Checking Maximum Coverage

Tai lieu nay gom bo test gon nhung bao phu cho project.

## 1. Testing goals

- kiem tra input boundary
- kiem tra rule coverage
- kiem tra tinh nhat quan giua cac solver
- kiem tra output format

## 2. Boundary tests

| Test | Muc tieu | Ky vong |
|---|---|---|
| B1 | `k = 1` | Chuong trinh chay binh thuong va tra ve 1 rule |
| B2 | `k = 3` | Solver exact cho ket qua toi uu tren dataset nho |
| B3 | `k = 20` | Hop le voi gioi han lon nhat cua rules |
| B4 | `k = 0` | Quay lai menu hoac thoat theo flow hien tai |
| B5 | `k > 20` | Input phai bi chan o menu |
| B6 | file rong | Bao loi du lieu thieu |

## 3. Coverage tests

| Test | Rule | Ky vong |
|---|---|---|
| C1 | `identity_short` | Cover password co do dai <= 6 |
| C2 | `identity_medium` | Cover password co do dai 7..10 |
| C3 | `identity_long` | Cover password co do dai >= 11 |
| C4 | `append_single_digit` | Sinh candidate them 0..9 o cuoi |
| C5 | `append_double_digit` | Sinh candidate them 00..99 co lap |
| C6 | `append_123` | Sinh candidate them `123` |
| C7 | `append_year` | Sinh candidate them nam 1990..2030 |
| C8 | `append_special` | Sinh candidate them ky tu dac biet |
| C9 | `prepend_single_digit` | Sinh candidate them so o dau |
| C10 | `prepend_123` | Sinh candidate them `123` o dau |
| C11 | `reverse` | Dao chuoi chinh xac |
| C12 | leet rules | Thay the a/o/e/s dung mapping |
| C13 | `mixed_leet` | Ket hop nhieu thay the trong mot lan |
| C14 | `keyboard_walk` | Sinh dung danh sach walk |
| C15 | `duplicate_last_char` | Lap ky tu cuoi neu chuoi khong rong |

## 4. Solver consistency tests

| Test | So sanh | Ky vong |
|---|---|---|
| A1 | Brute Force vs Greedy | Greedy khong vuot brute force tren dataset nho |
| A2 | Brute Force vs Dynamic Programming | Coverage phai khop nhau |
| A3 | Brute Force vs ILP + PuLP + CBC | Coverage phai khop nhau neu CBC giai toi uu |
| A4 | Brute Force vs Randomized Search | Heuristic khong nen vuot exact solver tren test nho |
| A5 | Brute Force vs Hill Climbing | Ket qua phai hop le va on dinh |

## 5. Suggested test matrix

| Dataset | k | Solvers |
|---|---:|---|
| Small exact set | 1..3 | Brute Force, DP, ILP |
| Small mixed set | 1..3 | Greedy, Randomized, Hill Climbing |
| Full dataset | 1..5 | Tat ca 6 solver |

## 6. Pass criteria

- khong crash
- output file duoc tao dung ten
- `coverage_count <= total_passwords`
- exact solvers khop nhau tren dataset nho
- menu chi hien thi 6 solver da xac dinh
