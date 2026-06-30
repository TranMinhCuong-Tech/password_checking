import itertools
import random
import time
import tracemalloc
from collections import Counter
from functools import lru_cache

try:
    import pulp
except ImportError:  # pragma: no cover - phu thuoc la tuy chon cho den khi cai dat
    pulp = None

try:
    from .rules import RULES, RULE_IDS
except ImportError:
    from rules import RULES, RULE_IDS

# ------------------------------------------------------------
# Y tuong chinh cua du an:
# - real_passwords.txt  = tap du lieu can duoc phu
# - mutated_passwords.txt = cac muc tieu duoc tao ra boi cac luat bien doi
# - moi luat tro thanh mot "tap phu" cua cac mat khau that ma no co the khop
# - moi bo giai se co gang chon k luat de phu duoc nhieu mat khau nhat co the
# ------------------------------------------------------------

# Ham load_passwords: doc danh sach mat khau that va mat khau bien doi tu file.
def load_passwords(filenames=("real_passwords.txt", "mutated_passwords.txt")):
    """
    Doc danh sach mat khau that va mat khau bien doi.
    Bo qua cac dong trong.
    """
    if isinstance(filenames, str):
        filenames = (filenames, "mutated_passwords.txt")

    real_file = filenames[0] if len(filenames) > 0 else "real_passwords.txt"
    mutated_file = filenames[1] if len(filenames) > 1 else "mutated_passwords.txt"

    data = {"real": [], "mutated": []}
    for key, filename in (("real", real_file), ("mutated", mutated_file)):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data[key] = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"[!] Khong tim thay file '{filename}'.")
    return data

# Ham get_universe_passwords: lay danh sach mat khau that tu du lieu dau vao.
def get_universe_passwords(password_data):
    # Chap nhan ca dict {"real": ..., "mutated": ...} hoac danh sach thong thuong.
    if isinstance(password_data, dict):
        return password_data.get("real", [])
    return password_data

# Ham get_mutated_passwords: lay tap mat khau bien doi tu du lieu dau vao.
def get_mutated_passwords(password_data):
    # Mat khau bien doi duoc luu trong set vi thao tac kiem tra xuat hien lap lai nhieu lan.
    if isinstance(password_data, dict):
        return set(password_data.get("mutated", []))
    return set(password_data)

# Ham normalize_candidates: chuan hoa ket qua ung vien ve dang tuple.
def normalize_candidates(candidates):
    if candidates is None:
        return ()
    if isinstance(candidates, str):
        return (candidates,)
    return tuple(candidates)

# Ham clamp_k: gioi han k trong khoang hop le cua so luat.
def clamp_k(k, rule_count):
    return max(0, min(k, rule_count))

# Ham build_rule_coverages: xay dung cau truc phu cho tung luat.
def build_rule_coverages(passwords):
    """
    Xay dung cau truc phu duoi dang tap hop.
    rule_coverages[rule_id] = frozenset cac chi so mat khau duoc luat do phu.
    password_to_rules[index] = tuple cac id luat phu mat khau do.
    """
    real_passwords = list(get_universe_passwords(passwords))
    mutated_passwords = get_mutated_passwords(passwords)

    rule_coverages = {}
    password_to_rules = {index: [] for index in range(len(real_passwords))}

    for rule_id in RULE_IDS:
        transform = RULES[rule_id]["transform"]
        covered_indices = set()
        for index, password in enumerate(real_passwords):
            # Mot luat co the tra ve mot chuoi hoac nhieu chuoi ung vien.
            candidates = normalize_candidates(transform(password))
            if any(candidate in mutated_passwords for candidate in candidates):
                covered_indices.add(index)
        frozen_coverage = frozenset(covered_indices)
        rule_coverages[rule_id] = frozen_coverage
        for index in frozen_coverage:
            password_to_rules[index].append(rule_id)

    for index in password_to_rules:
        password_to_rules[index].sort()

    return rule_coverages, password_to_rules, real_passwords

# Ham coverage_of_rules: hop tat ca tap phu cua cac luat da chon.
def coverage_of_rules(rule_coverages, selected_rule_ids):
    # Hop tat ca tap phu cua cac luat da chon.
    covered = set()
    for rule_id in selected_rule_ids:
        covered.update(rule_coverages[rule_id])
    return covered

# Ham coverage_counts: dem so luat phu tung chi so mat khau.
def coverage_counts(rule_coverages, selected_rule_ids):
    # Dem xem moi chi so mat khau duoc bao nhieu luat da chon phu.
    # Dieu nay huu ich cho local search dua tren phep doi cho.
    counts = Counter()
    for rule_id in selected_rule_ids:
        counts.update(rule_coverages[rule_id])
    return counts

# Ham covered_passwords_from_indices: doi chi so da phu thanh danh sach mat khau.
def covered_passwords_from_indices(real_passwords, covered_indices):
    return [real_passwords[index] for index in sorted(covered_indices)]

# Ham rule_names: tao danh sach ten luat tu danh sach id luat.
def rule_names(rule_ids):
    return [f"[{rule_id}] {RULES[rule_id]['label']}" for rule_id in rule_ids]

# Ham result_payload: dong goi ket qua cua cac bo giai theo cung dinh dang.
def result_payload(method_name, k, selected_rule_ids, passwords, covered_indices):
    # Chuan hoa tat ca thanh mot object tra ve duy nhat de moi bo giai
    # deu co cung dinh dang dau ra.
    real_passwords = get_universe_passwords(passwords)
    covered_passwords = covered_passwords_from_indices(real_passwords, covered_indices)
    total_passwords = len(real_passwords)
    mutated_count = len(passwords.get("mutated", [])) if isinstance(passwords, dict) else 0
    covered_set = frozenset(covered_indices)
    return {
        "method": method_name,
        "k": k,
        "selected_rule_ids": selected_rule_ids,
        "selected_rules": rule_names(selected_rule_ids),
        "covered_set": covered_set,
        "covered_indices": covered_set,
        "covered_passwords": covered_passwords,
        "coverage_count": len(covered_set),
        "total_passwords": total_passwords,
        "mutated_passwords": mutated_count,
    }

# Ham save_answer: ghi ket qua ra file output.
def save_answer(filename, result):
    """
    Ghi ket qua ra file.
    """
    with open(filename, "w", encoding="utf-8") as f:
        f.write("Method:\n")
        f.write(f"{result['method']}\n")

        f.write("\nFixed number of selected rules (k):\n")
        f.write(f"{result['k']}\n")

        f.write("\nInput summary:\n")
        f.write(f"Real passwords: {result['total_passwords']}\n")
        f.write(f"Mutated passwords: {result['mutated_passwords']}\n")

        f.write("\nSelected rules:\n")
        if result["selected_rules"]:
            for rule in result["selected_rules"]:
                f.write(f"{rule}\n")
        else:
            f.write("null\n")

        f.write("\nCovered passwords:\n")
        if result["covered_passwords"]:
            for password in result["covered_passwords"]:
                f.write(f"{password}\n")
        else:
            f.write("null\n")

        f.write("\nCoverage:\n")
        f.write(f"{result['coverage_count']} / {result['total_passwords']}\n")

    print(f"[+] Da luu ket qua vao: {filename}")

# Ham run_solver: chay bo giai, do thoi gian bo nho, va luu ket qua.
def run_solver(method_name, solver, k, passwords, output_prefix):
    """
    Chay mot bo giai, do thoi gian va bo nho, sau do luu ket qua.
    """
    # Ban than bo giai chi tra ve dap an.
    # Ham phu nay lo phan do thoi gian, do bo nho, in ket qua va ghi file.
    tracemalloc.start()
    start_time = time.perf_counter()

    result = solver(passwords, k)

    end_time = time.perf_counter()
    current_memory, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    output_file = f"{output_prefix}_k{k}.txt"
    save_answer(output_file, result)

    print(f"\n============= {method_name.upper()} =============")
    print("[+] Cac luat da chon :")
    if result["selected_rules"]:
        for rule in result["selected_rules"]:
            print(f"    {rule}")
    else:
        print("    null")
    print(f"[+] Da phu        : {result['coverage_count']}/{result['total_passwords']}")
    print(f"[+] Thoi gian chay : {end_time - start_time:.6f} s")
    print(f"[+] Bo nho da dung : {current_memory / 1024:.2f} KB | {current_memory / (1024 * 1024):.4f} MB")
    print(f"[+] Bo nho dinh    : {peak_memory / 1024:.2f} KB | {peak_memory / (1024 * 1024):.4f} MB")
    print("==============================================")
    return result

# Ham gain_of_rule: tinh so mat khau moi ma mot luat co the them vao.
def gain_of_rule(rule_coverages, covered_indices, rule_id):
    # Luat nay se them bao nhieu mat khau MOI?
    return len(rule_coverages[rule_id] - covered_indices)

# Ham best_rule_by_gain: tim luat co loi ich bien bi lon nhat.
def best_rule_by_gain(rule_coverages, covered_indices, candidate_rule_ids):
    # Dung cho chien luoc tham lam: chon luat co loi ich bien bi lon nhat.
    best_rule_id = None
    best_coverage = frozenset(covered_indices)
    best_gain = -1
    for rule_id in candidate_rule_ids:
        candidate_coverage = covered_indices | rule_coverages[rule_id]
        gain = len(candidate_coverage) - len(covered_indices)
        if gain > best_gain:
            best_gain = gain
            best_rule_id = rule_id
            best_coverage = candidate_coverage
    return best_rule_id, best_coverage, best_gain

# Ham random_selection: chon ngau nhien dung k luat tu tap ung vien.
def random_selection(rule_ids, k, rng):
    # Lay mau ngau nhien dung k luat, giu thu tu sap xep de dau ra on dinh.
    if k <= 0:
        return []
    if k >= len(rule_ids):
        return list(rule_ids)
    return sorted(rng.sample(rule_ids, k))

# Ham solve_bruteforce: giai chinh xac bang cach duyet tat ca to hop.
def solve_bruteforce(passwords, k):
    """
    Tim kiem chinh xac bang cach thu moi to hop dung k luat.
    """
    # Day la phuong phap chinh xac co ban.
    # No don gian nhung tro nen ton kem rat nhanh vi phai liet ke moi to hop.
    rule_coverages, _, real_passwords = build_rule_coverages(passwords)
    rule_ids = list(RULE_IDS)
    k = clamp_k(k, len(rule_ids))

    if k == 0 or not real_passwords:
        return result_payload("brute force", k, [], passwords, frozenset())

    best_rule_ids = []
    best_coverage = frozenset()
    best_count = -1

    for combo in itertools.combinations(rule_ids, k):
        coverage = coverage_of_rules(rule_coverages, combo)
        count = len(coverage)
        if count > best_count:
            best_count = count
            best_coverage = frozenset(coverage)
            best_rule_ids = list(combo)

    return result_payload("brute force", k, best_rule_ids, passwords, best_coverage)

# Ham solve_greedy: giai bang chien luoc tham lam.
def solve_greedy(passwords, k):
    """
    Tham lam: moi buoc chon luat bo sung phu moi lon nhat.
    """
    # Bat dau tu loi giai rong va lien tuc them luat tot nhat o moi vong lap.
    rule_coverages, _, real_passwords = build_rule_coverages(passwords)
    remaining_rule_ids = list(RULE_IDS)
    selected_rule_ids = []
    covered_indices = set()
    k = clamp_k(k, len(RULE_IDS))

    while len(selected_rule_ids) < k and remaining_rule_ids:
        best_rule_id = None
        best_coverage = frozenset(covered_indices)
        best_gain = -1

        for rule_id in remaining_rule_ids:
            candidate_coverage = covered_indices | rule_coverages[rule_id]
            gain = len(candidate_coverage) - len(covered_indices)
            if gain > best_gain:
                best_gain = gain
                best_rule_id = rule_id
                best_coverage = candidate_coverage

        if best_rule_id is None:
            break

        selected_rule_ids.append(best_rule_id)
        remaining_rule_ids.remove(best_rule_id)
        covered_indices = set(best_coverage)

    return result_payload("greedy", k, selected_rule_ids, passwords, covered_indices)

# Ham solve_randomized_search: tim kiem ngau nhien cac tap luat hop le.
def solve_randomized_search(passwords, k, iterations=None, seed=None):
    """
    Tim kiem ngau nhien: lay mau nhieu tap con hop le gom k luat va giu phuong an tot nhat.
    """
    # Y tuong heuristic:
    # thu nhieu tap con ngau nhien, nhung khoi tao dap an tot nhat bang mot loi giai tham lam.
    rule_coverages, _, real_passwords = build_rule_coverages(passwords)
    rule_ids = list(RULE_IDS)
    k = clamp_k(k, len(rule_ids))

    if k == 0 or not real_passwords:
        return result_payload("randomized search", k, [], passwords, frozenset())

    if iterations is None:
        iterations = max(40, len(rule_ids) * max(1, k) * 2)

    base_seed = seed if seed is not None else (len(rule_ids) * 1009 + k * 97 + len(real_passwords))
    rng = random.Random(base_seed)

    greedy_result = solve_greedy(passwords, k)
    best_rule_ids = list(greedy_result["selected_rule_ids"])
    best_coverage = frozenset(greedy_result["covered_indices"])
    best_count = len(best_coverage)

    for _ in range(iterations):
        candidate_rule_ids = random_selection(rule_ids, k, rng)
        candidate_coverage = coverage_of_rules(rule_coverages, candidate_rule_ids)
        candidate_count = len(candidate_coverage)
        if candidate_count > best_count:
            best_rule_ids = list(candidate_rule_ids)
            best_coverage = frozenset(candidate_coverage)
            best_count = candidate_count

    return result_payload("randomized search", k, best_rule_ids, passwords, best_coverage)

# Ham solve_dp: giai chinh xac bang quy hoach dong va memoization.
def solve_dp(passwords, k):
    """
    Tim kiem chinh xac voi memoization.
    Cach nay phu hop cho bai toan nho vi khong gian trang thai tang rat nhanh.
    """
    # DP o day luu trang thai dua tren:
    # - chi so luat nao duoc phep dung tiep theo
    # - con can bao nhieu luat
    # - nhung mat khau nao da duoc phu
    rule_coverages, _, real_passwords = build_rule_coverages(passwords)
    rule_ids = list(RULE_IDS)
    k = clamp_k(k, len(rule_ids))

    if k == 0 or not real_passwords:
        return result_payload("dynamic programming", k, [], passwords, frozenset())

    @lru_cache(maxsize=None)
    def best_solution(start_index, remaining, covered_state):
        covered_indices = set(covered_state)
        if remaining == 0:
            return len(covered_indices), ()

        best_count = len(covered_indices)
        best_selected = ()
        last_start = len(rule_ids) - remaining + 1

        for index in range(start_index, last_start):
            rule_id = rule_ids[index]
            next_covered = frozenset(covered_indices | rule_coverages[rule_id])
            candidate_count, rest_selected = best_solution(index + 1, remaining - 1, next_covered)
            if candidate_count > best_count or not best_selected:
                best_count = candidate_count
                best_selected = (rule_id,) + rest_selected

        return best_count, best_selected

    _, selected_rules = best_solution(0, k, frozenset())
    covered_indices = coverage_of_rules(rule_coverages, selected_rules)
    return result_payload("dynamic programming", k, list(selected_rules), passwords, covered_indices)

# Ham solve_hill_climbing: toi uu cuc bo voi chien luoc cai tien tot nhat.
def solve_hill_climbing(passwords, k):
    """
    Hill climbing voi cac buoc doi 1-1 tot nhat, khoi dau tu mot loi giai tham lam.
    """
    rule_coverages, _, real_passwords = build_rule_coverages(passwords)
    rule_ids = list(RULE_IDS)
    k = clamp_k(k, len(rule_ids))

    if k == 0 or not real_passwords:
        return result_payload("hill climbing", k, [], passwords, frozenset())

    current_rule_ids = sorted(solve_greedy(passwords, k)["selected_rule_ids"])
    current_covered = coverage_of_rules(rule_coverages, current_rule_ids)

    improved = True
    while improved:
        improved = False
        current_score = len(current_covered)
        best_rule_ids = list(current_rule_ids)
        best_covered = set(current_covered)

        selected_set = set(current_rule_ids)
        remaining_rule_ids = [rule_id for rule_id in rule_ids if rule_id not in selected_set]

        for remove_index, removed_rule in enumerate(current_rule_ids):
            for added_rule in remaining_rule_ids:
                candidate_rule_ids = list(current_rule_ids)
                candidate_rule_ids[remove_index] = added_rule
                candidate_covered = coverage_of_rules(rule_coverages, candidate_rule_ids)
                candidate_score = len(candidate_covered)
                if candidate_score > current_score and candidate_score > len(best_covered):
                    best_rule_ids = sorted(candidate_rule_ids)
                    best_covered = candidate_covered
                    improved = True

        current_rule_ids = best_rule_ids
        current_covered = set(best_covered)

    return result_payload("hill climbing", k, current_rule_ids, passwords, current_covered)

# Ham solve_ilp_pulp_cbc: giai Maximum Coverage bang mo hinh ILP.
def solve_ilp_pulp_cbc(passwords, k):
    """
    Mo hinh quy hoach tuyen tinh nguyen 0-1 chinh xac cho Maximum Coverage.
    """
    # ILP bien bai toan thanh cac bien quyet dinh nhi phan:
    # x_i = chon luat i hay khong
    # y_j = mat khau j co duoc phu hay khong
    if pulp is None:
        raise RuntimeError(
            "PuLP is required for ILP_PuLP_CBC. Install it with `pip install pulp`."
        )

    rule_coverages, password_to_rules, real_passwords = build_rule_coverages(passwords)
    rule_ids = list(RULE_IDS)
    k = clamp_k(k, len(rule_ids))

    if k == 0 or not real_passwords:
        return result_payload("ILP + PuLP + CBC", k, [], passwords, frozenset())

    problem = pulp.LpProblem("MaximumCoverage", pulp.LpMaximize)
    x_vars = {
        rule_id: pulp.LpVariable(f"x_{rule_id}", cat=pulp.LpBinary)
        for rule_id in rule_ids
    }
    y_vars = {
        index: pulp.LpVariable(f"y_{index}", cat=pulp.LpBinary)
        for index in range(len(real_passwords))
    }

    problem += pulp.lpSum(y_vars[index] for index in range(len(real_passwords)))
    problem += pulp.lpSum(x_vars[rule_id] for rule_id in rule_ids) == k

    for index, covering_rule_ids in password_to_rules.items():
        if covering_rule_ids:
            problem += y_vars[index] <= pulp.lpSum(x_vars[rule_id] for rule_id in covering_rule_ids)
        else:
            problem += y_vars[index] == 0

    solver = pulp.PULP_CBC_CMD(msg=False)
    status = problem.solve(solver)
    if pulp.LpStatus[status] != "Optimal":
        raise RuntimeError(
            f"CBC did not find an optimal solution. Status: {pulp.LpStatus[status]}"
        )

    selected_rule_ids = [
        rule_id
        for rule_id in rule_ids
        if pulp.value(x_vars[rule_id]) and pulp.value(x_vars[rule_id]) > 0.5
    ]

    covered_indices = coverage_of_rules(rule_coverages, selected_rule_ids)
    return result_payload(
        "ILP + PuLP + CBC",
        k,
        selected_rule_ids,
        passwords,
        covered_indices,
    )

