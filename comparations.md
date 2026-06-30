# Algorithm Comparisons

Tai lieu nay tom tat ket qua so sanh 6 solver tren cung bo du lieu hien tai:

- 500 real passwords
- 1500 mutated passwords
- 20 rules

## How metrics were collected

- `time.perf_counter()` de do thoi gian
- `tracemalloc` de do memory hien tai va peak memory
- cung mot input cho tat ca solver o moi muc `k`

## High-level summary

- `Brute Force`, `Dynamic Programming`, va `ILP + PuLP + CBC` la cac exact solver
- `Greedy` la baseline nhanh nhat va on dinh nhat
- `Randomized Search` va `Hill Climbing` la heuristic
- Tren dataset nay, nhieu muc `k` cho ket qua coverage rat gan nhau giua cac solver

## Representative results

### k = 1

Tat ca solver deu chon rule `6` (`append_single_digit`) va dat `155 / 500`.

### k = 3

Tat ca solver deu dat `296 / 500`.

Rule set thuong gap:

- Brute Force / DP / ILP / Hill Climbing: `[2, 4, 6]`
- Greedy / Randomized Search: `[6, 2, 4]`

### k = 4

Tat ca solver deu dat `345 / 500`.

Thuong gap:

- `[2, 4, 6, 12]` hoac bien the thu tu cua no

### k = 5

Tat ca solver deu dat `384 / 500`.

Thuong gap:

- `[2, 4, 6, 12, 14]` hoac bien the thu tu cua no

## Observations

- `Greedy` co runtime tot va rat de giai thich
- `Dynamic Programming` tieu ton memory manh khi `k` tang
- `ILP + PuLP + CBC` co overhead tu solver backend nhung cho ket qua chinh xac
- `Randomized Search` va `Hill Climbing` co ket qua on tren dataset nay, nhung khong bao dam toi uu trong tong quat

## Reproducibility

Neu can cap nhat bang so lieu moi, chay project qua tung solver va luu output theo mau:

- `output_brute_k*.txt`
- `output_greedy_k*.txt`
- `output_dp_k*.txt`
- `output_ILP_PuLP_CBC_k*.txt`
- `output_randomized_k*.txt`
- `output_hill_k*.txt`
