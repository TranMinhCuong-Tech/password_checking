def identity_short(password):
    if len(password) <= 6:
        return password
    return []


def identity_medium(password):
    if 7 <= len(password) <= 10:
        return password
    return []


def identity_long(password):
    if len(password) >= 11:
        return password
    return []


def capitalize(password):
    candidate = password.capitalize()
    if candidate == password:
        return []
    return candidate


def uppercase_all(password):
    candidate = password.upper()
    if candidate == password:
        return []
    return candidate


def append_single_digit(password):
    return [f"{password}{digit}" for digit in range(10)]


def append_double_digit(password):
    return [f"{password}{digit}{digit}" for digit in range(10)]


def append_123(password):
    return f"{password}123"


def append_year(password):
    return [f"{password}{year}" for year in range(1990, 2031)]


def append_special(password):
    return [f"{password}{symbol}" for symbol in ("!", "@", "#", "$", "%")]


def prepend_single_digit(password):
    return [f"{digit}{password}" for digit in range(10)]


def prepend_123(password):
    return f"123{password}"


def reverse(password):
    candidate = password[::-1]
    if candidate == password:
        return []
    return candidate


def leet_a4(password):
    candidate = password.replace("a", "4").replace("A", "4")
    if candidate == password:
        return []
    return candidate


def leet_o0(password):
    candidate = password.replace("o", "0").replace("O", "0")
    if candidate == password:
        return []
    return candidate


def leet_e3(password):
    candidate = password.replace("e", "3").replace("E", "3")
    if candidate == password:
        return []
    return candidate


def leet_s_dollar(password):
    candidate = password.replace("s", "$").replace("S", "$")
    if candidate == password:
        return []
    return candidate


def mixed_leet(password):
    candidate = (
        password.replace("a", "@")
        .replace("A", "@")
        .replace("o", "0")
        .replace("O", "0")
        .replace("i", "1")
        .replace("I", "1")
        .replace("e", "3")
        .replace("E", "3")
        .replace("s", "$")
        .replace("S", "$")
    )
    if candidate == password:
        return []
    return candidate


def keyboard_walk(password):
    return [f"{password}{walk}" for walk in ("qwerty", "asdf", "zxcv", "123qwe")]


def duplicate_last_char(password):
    if not password:
        return []
    return f"{password}{password[-1]}"


RULES = {
    1: {"name": "identity_short", "label": "identity_short", "transform": identity_short},
    2: {"name": "identity_medium", "label": "identity_medium", "transform": identity_medium},
    3: {"name": "identity_long", "label": "identity_long", "transform": identity_long},
    4: {"name": "capitalize", "label": "capitalize", "transform": capitalize},
    5: {"name": "uppercase_all", "label": "uppercase_all", "transform": uppercase_all},
    6: {"name": "append_single_digit", "label": "append_single_digit", "transform": append_single_digit},
    7: {"name": "append_double_digit", "label": "append_double_digit", "transform": append_double_digit},
    8: {"name": "append_123", "label": "append_123", "transform": append_123},
    9: {"name": "append_year", "label": "append_year", "transform": append_year},
    10: {"name": "append_special", "label": "append_special", "transform": append_special},
    11: {"name": "prepend_single_digit", "label": "prepend_single_digit", "transform": prepend_single_digit},
    12: {"name": "prepend_123", "label": "prepend_123", "transform": prepend_123},
    13: {"name": "reverse", "label": "reverse", "transform": reverse},
    14: {"name": "leet_a4", "label": "leet_a4", "transform": leet_a4},
    15: {"name": "leet_o0", "label": "leet_o0", "transform": leet_o0},
    16: {"name": "leet_e3", "label": "leet_e3", "transform": leet_e3},
    17: {"name": "leet_s$", "label": "leet_s$", "transform": leet_s_dollar},
    18: {"name": "mixed_leet", "label": "mixed_leet", "transform": mixed_leet},
    19: {"name": "keyboard_walk", "label": "keyboard_walk", "transform": keyboard_walk},
    20: {"name": "duplicate_last_char", "label": "duplicate_last_char", "transform": duplicate_last_char},
}

RULE_IDS = tuple(RULES.keys())


def printRuleCatalog():
    print("\nCandidate mutation rules:")
    for rule_id in RULE_IDS:
        print(f"    [{rule_id}] {RULES[rule_id]['label']}")
    print("    [0] Exit")


def checkPassword(algorithm_module, k, password_files):
    print(f"\n[+] Total candidate rules: {len(RULES)}")
    print(f"[+] Number of rules to select: {k}")

    try:
        password_data = algorithm_module.load_passwords(password_files)
    except AttributeError:
        password_data = {}

    real_count = len(password_data.get("real", [])) if isinstance(password_data, dict) else 0
    mutated_count = len(password_data.get("mutated", [])) if isinstance(password_data, dict) else 0

    if real_count == 0 or mutated_count == 0:
        print("[!] No password data loaded. Returning...")
        return None

    print(f"[+] Loaded real passwords: {real_count}")
    print(f"[+] Loaded mutated passwords: {mutated_count}")
    print("[*] Solving Maximum Coverage...\n")
    return algorithm_module.solve_max_coverage(k, password_data)
