def identity(password):
    return password


def capitalize(password):
    return password.capitalize()


def uppercase_all(password):
    return password.upper()


def append_1(password):
    return f"{password}1"


def append_12(password):
    return f"{password}12"


def append_123(password):
    return f"{password}123"


def append_year(password):
    return [f"{password}{year}" for year in range(1990, 2031)]


def prepend_1(password):
    return f"1{password}"


def prepend_123(password):
    return f"123{password}"


def reverse(password):
    return password[::-1]


def leet_a4(password):
    return password.replace("a", "4").replace("A", "4")


def leet_o0(password):
    return password.replace("o", "0").replace("O", "0")


def leet_e3(password):
    return password.replace("e", "3").replace("E", "3")


def leet_s_dollar(password):
    return password.replace("s", "$").replace("S", "$")


def mixed_leet(password):
    return (
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


def keyboard_walk(password):
    return f"{password}qwerty"


def keyboard_walk_number(password):
    return f"{password}qwerty123"


def numeric_sequence(password):
    return f"{password}123456"


def repeated_digit(password):
    return [f"{password}{digit}{digit}{digit}" for digit in range(10)]


def duplicate_last_char(password):
    if not password:
        return password
    return f"{password}{password[-1]}"


RULES = {
    1: {"name": "identity", "label": "identity", "transform": identity},
    2: {"name": "capitalize", "label": "capitalize", "transform": capitalize},
    3: {"name": "uppercase_all", "label": "uppercase_all", "transform": uppercase_all},
    4: {"name": "append_1", "label": "append_1", "transform": append_1},
    5: {"name": "append_12", "label": "append_12", "transform": append_12},
    6: {"name": "append_123", "label": "append_123", "transform": append_123},
    7: {"name": "append_year", "label": "append_year", "transform": append_year},
    8: {"name": "prepend_1", "label": "prepend_1", "transform": prepend_1},
    9: {"name": "prepend_123", "label": "prepend_123", "transform": prepend_123},
    10: {"name": "reverse", "label": "reverse", "transform": reverse},
    11: {"name": "leet_a4", "label": "leet_a4", "transform": leet_a4},
    12: {"name": "leet_o0", "label": "leet_o0", "transform": leet_o0},
    13: {"name": "leet_e3", "label": "leet_e3", "transform": leet_e3},
    14: {"name": "leet_s$", "label": "leet_s$", "transform": leet_s_dollar},
    15: {"name": "mixed_leet", "label": "mixed_leet", "transform": mixed_leet},
    16: {"name": "keyboard_walk", "label": "keyboard_walk", "transform": keyboard_walk},
    17: {"name": "keyboard_walk_number", "label": "keyboard_walk_number", "transform": keyboard_walk_number},
    18: {"name": "numeric_sequence", "label": "numeric_sequence", "transform": numeric_sequence},
    19: {"name": "repeated_digit", "label": "repeated_digit", "transform": repeated_digit},
    20: {"name": "duplicate_last_char", "label": "duplicate_last_char", "transform": duplicate_last_char},
}

RULE_IDS = tuple(RULES.keys())


def printRuleCatalog():
    print("\nCandidate mutation rules:")
    for rule_id in RULE_IDS:
        print(f"    [{rule_id}] {RULES[rule_id]['label']}")


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
