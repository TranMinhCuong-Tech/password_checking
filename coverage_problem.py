import itertools
import time
import tracemalloc
from functools import lru_cache

try:
    from .rules import RULES, RULE_IDS
except ImportError:
    from rules import RULES, RULE_IDS


<<<<<<< HEAD
DEFAULT_REAL_PASSWORD_FILE = "real_passwords_500_NCSC_breach_derived.txt"
DEFAULT_MUTATED_PASSWORD_FILE = "mutated_passwords_1500.txt"


def load_password_file(filename):
    """
    Load one password file. Empty lines are ignored.
    """
    passwords = []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            passwords.extend(line.strip() for line in f if line.strip())
    except FileNotFoundError:
        print(f"[!] File '{filename}' not found.")
    return passwords
=======
def load_passwords(filenames=("real_passwords.txt", "mutated_passwords.txt")):
    """
    Doc file password that va file password bien tau.
    Moi dong la mot password. Dong trong se bi bo qua.
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
            print(f"[!] File '{filename}' not found.")
    return data


def get_universe_passwords(password_data):
    if isinstance(password_data, dict):
        return password_data.get("real", [])
    return password_data


def get_mutated_passwords(password_data):
    if isinstance(password_data, dict):
        return set(password_data.get("mutated", []))
    return set(password_data)


def normalize_candidates(candidates):
    if isinstance(candidates, str):
        return (candidates,)
    return tuple(candidates)
>>>>>>> 13434496e7a9dc624ff952d4c59d945491d27061


def load_passwords(filenames=(DEFAULT_REAL_PASSWORD_FILE, DEFAULT_MUTATED_PASSWORD_FILE)):
    """
<<<<<<< HEAD
    Load the real and mutated password datasets.

    The function accepts either:
    - no arguments, using the default project files
    - a tuple/list of exactly two filenames
    """
    if isinstance(filenames, (tuple, list)):
        if len(filenames) != 2:
            raise ValueError("Expected exactly two filenames: (real_file, mutated_file)")
        real_filename, mutated_filename = filenames
    else:
        real_filename, mutated_filename = filenames, DEFAULT_MUTATED_PASSWORD_FILE
    return load_password_file(real_filename), load_password_file(mutated_filename)


def _iter_candidates(transformed_value):
    if transformed_value is None:
        return ()
    if isinstance(transformed_value, str):
        return (transformed_value,)
    try:
        return tuple(transformed_value)
    except TypeError:
        return (transformed_value,)


def build_rule_masks(real_passwords, mutated_passwords):
    """
    Convert each transformation rule into a bitmask over the real-password universe.

    Bit i = 1 if at least one mutated password transformed by the rule matches
    real_passwords[i] exactly.
    """
    real_index = {password: index for index, password in enumerate(real_passwords)}
=======
    Chuyen moi rule thanh bitmask.
    Bit i = 1 neu password that thu i tao ra it nhat mot bien the
    nam trong mutated_passwords.txt khi ap dung rule do.
    """
    real_passwords = get_universe_passwords(passwords)
    mutated_passwords = get_mutated_passwords(passwords)
>>>>>>> 13434496e7a9dc624ff952d4c59d945491d27061
    masks = {}
    matched_sources = {}

    for rule_id in RULE_IDS:
<<<<<<< HEAD
        transformer = RULES[rule_id]["transform"]
        mask = 0
        seen_real_indices = set()
        rule_examples = []

        for source_password in mutated_passwords:
            for candidate in _iter_candidates(transformer(source_password)):
                real_index_pos = real_index.get(candidate)
                if real_index_pos is None:
                    continue

                mask |= 1 << real_index_pos
                if real_index_pos not in seen_real_indices:
                    seen_real_indices.add(real_index_pos)
                    rule_examples.append(
                        {
                            "source": source_password,
                            "transformed": candidate,
                            "matched_real": real_passwords[real_index_pos],
                        }
                    )

=======
        transform = RULES[rule_id]["transform"]
        mask = 0
        for index, password in enumerate(real_passwords):
            candidates = normalize_candidates(transform(password))
            if any(candidate in mutated_passwords for candidate in candidates):
                mask |= 1 << index
>>>>>>> 13434496e7a9dc624ff952d4c59d945491d27061
        masks[rule_id] = mask
        matched_sources[rule_id] = rule_examples

    return masks, matched_sources


def mask_to_passwords(passwords, mask):
    real_passwords = get_universe_passwords(passwords)
    return [password for index, password in enumerate(real_passwords) if mask & (1 << index)]


def rule_names(rule_ids):
    return [f"[{rule_id}] {RULES[rule_id]['label']}" for rule_id in rule_ids]


<<<<<<< HEAD
def result_payload(method_name, k, selected_rule_ids, real_passwords, mutated_passwords, covered_mask, matched_sources=None):
    covered_passwords = mask_to_passwords(real_passwords, covered_mask)
    payload = {
=======
def result_payload(method_name, k, selected_rule_ids, passwords, covered_mask):
    covered_passwords = mask_to_passwords(passwords, covered_mask)
    total_passwords = len(get_universe_passwords(passwords))
    return {
>>>>>>> 13434496e7a9dc624ff952d4c59d945491d27061
        "method": method_name,
        "k": k,
        "selected_rule_ids": selected_rule_ids,
        "selected_rules": rule_names(selected_rule_ids),
        "covered_mask": covered_mask,
        "covered_passwords": covered_passwords,
        "coverage_count": len(covered_passwords),
<<<<<<< HEAD
        "total_passwords": len(real_passwords),
        "total_real_passwords": len(real_passwords),
        "total_mutated_passwords": len(mutated_passwords),
=======
        "total_passwords": total_passwords,
>>>>>>> 13434496e7a9dc624ff952d4c59d945491d27061
    }
    if matched_sources is not None:
        payload["matched_sources"] = matched_sources
    return payload


def save_answer(filename, result):
    """
<<<<<<< HEAD
    Save the selected rules and the real passwords covered by those rules.
=======
    Ghi ket qua theo format:
    - Method
    - Fixed k
    - Selected rules
    - Covered passwords
    - Coverage
>>>>>>> 13434496e7a9dc624ff952d4c59d945491d27061
    """
    with open(filename, "w", encoding="utf-8") as f:
        f.write("Method:\n")
        f.write(f"{result['method']}\n")

        f.write("\nFixed number of selected rules:\n")
        f.write(f"{result['k']}\n")

        f.write("\nSelected rules:\n")
        if result["selected_rules"]:
            for rule in result["selected_rules"]:
                f.write(f"{rule}\n")
        else:
            f.write("null\n")

        f.write("\nCovered real passwords:\n")
        if result["covered_passwords"]:
            for password in result["covered_passwords"]:
                f.write(f"{password}\n")
        else:
            f.write("null\n")

        f.write("\nCoverage:\n")
        f.write(f"{result['coverage_count']} / {result['total_real_passwords']}\n")

    print(f"[+] Results saved to: {filename}")


def run_solver(method_name, solver, k, real_passwords, mutated_passwords, output_prefix):
    """
    Run solver, measure time/memory, and save the result to disk.
    """
    tracemalloc.start()
    start_time = time.perf_counter()

    result = solver(real_passwords, mutated_passwords, k)

    end_time = time.perf_counter()
    current_memory, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    output_file = f"{output_prefix}_k{k}.txt"
    save_answer(output_file, result)

    print(f"\n============= {method_name.upper()} =============")
    print("[+] Selected Rules :")
    if result["selected_rules"]:
        for rule in result["selected_rules"]:
            print(f"    {rule}")
    else:
        print("    null")
    print(f"[+] Covered(real)  : {result['coverage_count']}/{result['total_real_passwords']}")
    print(f"[+] Mutated input  : {result['total_mutated_passwords']}")
    print(f"[+] Execution Time : {end_time - start_time:.6f} s")
    print(f"[+] Memory Used    : {current_memory / 1024:.2f} KB | {current_memory / (1024 * 1024):.4f} MB")
    print(f"[+] Peak Memory    : {peak_memory / 1024:.2f} KB | {peak_memory / (1024 * 1024):.4f} MB")
    print("==============================================")
    return result


def solve_bruteforce(real_passwords, mutated_passwords, k):
    """
    Exact search: enumerate every combination of exactly k rules.
    """
    rule_masks, matched_sources = build_rule_masks(real_passwords, mutated_passwords)
    rule_ids = list(RULE_IDS)
    k = max(0, min(k, len(rule_ids)))

<<<<<<< HEAD
    if k == 0 or not real_passwords or not mutated_passwords:
        return result_payload("brute force", k, [], real_passwords, mutated_passwords, 0, matched_sources)
=======
    if k == 0 or not get_universe_passwords(passwords):
        return result_payload("brute force", k, [], passwords, 0)
>>>>>>> 13434496e7a9dc624ff952d4c59d945491d27061

    best_rule_ids = []
    best_mask = 0
    best_count = -1

    for combo in itertools.combinations(rule_ids, k):
        mask = 0
        for rule_id in combo:
            mask |= rule_masks[rule_id]
        count = mask.bit_count()
        if count > best_count:
            best_count = count
            best_mask = mask
            best_rule_ids = list(combo)

    return result_payload("brute force", k, best_rule_ids, real_passwords, mutated_passwords, best_mask, matched_sources)


def solve_greedy(real_passwords, mutated_passwords, k):
    """
    Greedy: choose the rule with the largest marginal gain at each step.
    """
    rule_masks, matched_sources = build_rule_masks(real_passwords, mutated_passwords)
    remaining_rule_ids = set(RULE_IDS)
    selected_rule_ids = []
    covered_mask = 0
    k = max(0, min(k, len(RULE_IDS)))

    while len(selected_rule_ids) < k and remaining_rule_ids:
        best_rule_id = None
        best_mask = covered_mask
        best_gain = -1

        for rule_id in sorted(remaining_rule_ids):
            candidate_mask = covered_mask | rule_masks[rule_id]
            gain = candidate_mask.bit_count() - covered_mask.bit_count()
            if gain > best_gain:
                best_gain = gain
                best_rule_id = rule_id
                best_mask = candidate_mask

        if best_rule_id is None:
            break

        selected_rule_ids.append(best_rule_id)
        remaining_rule_ids.remove(best_rule_id)
        covered_mask = best_mask

    return result_payload("greedy", k, selected_rule_ids, real_passwords, mutated_passwords, covered_mask, matched_sources)


def solve_math_model(real_passwords, mutated_passwords, k):
    """
    Exact bitmask model: enumerate every subset of exactly k rules.
    """
    rule_masks, matched_sources = build_rule_masks(real_passwords, mutated_passwords)
    rule_ids = list(RULE_IDS)
    k = max(0, min(k, len(rule_ids)))

<<<<<<< HEAD
    if k == 0 or not real_passwords or not mutated_passwords:
        return result_payload("math model", k, [], real_passwords, mutated_passwords, 0, matched_sources)
=======
    if k == 0 or not get_universe_passwords(passwords):
        return result_payload("math model", k, [], passwords, 0)
>>>>>>> 13434496e7a9dc624ff952d4c59d945491d27061

    best_subset_mask = 0
    best_coverage_mask = 0
    best_count = -1
    total_subsets = 1 << len(rule_ids)

    for subset_mask in range(total_subsets):
        if subset_mask.bit_count() != k:
            continue

        coverage_mask = 0
        for index, rule_id in enumerate(rule_ids):
            if subset_mask & (1 << index):
                coverage_mask |= rule_masks[rule_id]

        coverage_count = coverage_mask.bit_count()
        if coverage_count > best_count:
            best_count = coverage_count
            best_subset_mask = subset_mask
            best_coverage_mask = coverage_mask

    selected_rule_ids = [
        rule_id
        for index, rule_id in enumerate(rule_ids)
        if best_subset_mask & (1 << index)
    ]
    return result_payload("math model", k, selected_rule_ids, real_passwords, mutated_passwords, best_coverage_mask, matched_sources)


def solve_dp(real_passwords, mutated_passwords, k):
    """
    Exact search with memoization.
    """
    rule_masks, matched_sources = build_rule_masks(real_passwords, mutated_passwords)
    rule_ids = list(RULE_IDS)
    k = max(0, min(k, len(rule_ids)))

<<<<<<< HEAD
    if k == 0 or not real_passwords or not mutated_passwords:
        return result_payload("dynamic programming", k, [], real_passwords, mutated_passwords, 0, matched_sources)
=======
    if k == 0 or not get_universe_passwords(passwords):
        return result_payload("dynamic programming", k, [], passwords, 0)
>>>>>>> 13434496e7a9dc624ff952d4c59d945491d27061

    @lru_cache(maxsize=None)
    def best_solution(start_index, remaining):
        if remaining == 0:
            return 0, ()

        best_mask = 0
        best_selected = ()
        last_start = len(rule_ids) - remaining + 1
        for index in range(start_index, last_start):
            rule_id = rule_ids[index]
            rest_mask, rest_selected = best_solution(index + 1, remaining - 1)
            candidate_mask = rule_masks[rule_id] | rest_mask
            if candidate_mask.bit_count() > best_mask.bit_count() or not best_selected:
                best_mask = candidate_mask
                best_selected = (rule_id,) + rest_selected
        return best_mask, best_selected

    covered_mask, selected_rules = best_solution(0, k)
    return result_payload("dynamic programming", k, list(selected_rules), real_passwords, mutated_passwords, covered_mask, matched_sources)
