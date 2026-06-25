def identity(password):
    return password


<<<<<<< HEAD
def _pad_to_length(password, target_length, pad_char="0"):
    if len(password) >= target_length:
        return password
    return password.ljust(target_length, pad_char)


def _ensure_prefix(password, prefix):
    if password.startswith(prefix):
        return password
    return prefix + password


def _ensure_suffix(password, suffix):
    if password.endswith(suffix):
        return password
    return password + suffix


def first_char_upper(password):
    if not password:
        return password
    return password[0].upper() + password[1:]


def all_upper(password):
    return password.upper()


def all_lower(password):
    return password.lower()


def ends_with_digit(password):
    return _ensure_suffix(password, "1")


def ends_with_special(password):
    return _ensure_suffix(password, "!")


def starts_with_special(password):
    return _ensure_prefix(password, "!")


def contains_digit(password):
    if any(ch.isdigit() for ch in password):
        return password
    return f"{password}1"


def contains_special(password):
    if any(ch in string.punctuation for ch in password):
        return password
    return f"{password}!"


def contains_upper(password):
    if any(ch.isupper() for ch in password):
        return password
    if not password:
        return "A"
    return password[0].upper() + password[1:]


def contains_lower(password):
    if any(ch.islower() for ch in password):
        return password
    return password.lower() if password else "a"


def length_at_least_8(password):
    return _pad_to_length(password, 8)


def length_at_least_12(password):
    return _pad_to_length(password, 12)


def length_at_least_16(password):
    return _pad_to_length(password, 16)


def has_year_pattern(password):
    if any(str(year) in password for year in range(1990, 2031)):
        return password
    return f"{password}2024"


def has_common_word(password):
    common_words = (
        "admin",
        "pass",
        "password",
        "welcome",
        "login",
        "user",
        "root",
        "qwerty",
        "server",
        "security",
        "database",
        "network",
    )
    lowered = password.lower()
    if any(word in lowered for word in common_words):
        return password
    return f"{password}password"


def has_keyboard_sequence(password):
    sequences = ("123", "234", "345", "456", "567", "678", "789", "qwe", "asd", "zxc")
    lowered = password.lower()
    if any(sequence in lowered for sequence in sequences):
        return password
    return f"{password}123"


def has_repeated_character(password):
    if any(password[index] == password[index - 1] for index in range(1, len(password))):
        return password
    return f"{password}{password[-1] if password else 'a'}"


def has_mixed_case(password):
    if any(ch.isupper() for ch in password) and any(ch.islower() for ch in password):
        return password
    if not password:
        return "Aa"
    return password[:1].upper() + password[1:].lower()


def starts_with_letter(password):
    if password and password[0].isalpha():
        return password
    return f"a{password}"


def strong_password(password):
    transformed = has_mixed_case(password)
    transformed = contains_digit(transformed)
    transformed = contains_special(transformed)
    transformed = length_at_least_12(transformed)
    return transformed
=======
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
>>>>>>> 13434496e7a9dc624ff952d4c59d945491d27061


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
<<<<<<< HEAD
    1: {"label": "First character becomes uppercase", "transform": first_char_upper},
    2: {"label": "Convert to uppercase", "transform": all_upper},
    3: {"label": "Convert to lowercase", "transform": all_lower},
    4: {"label": "Ensure the last character is a digit", "transform": ends_with_digit},
    5: {"label": "Ensure the last character is a special symbol", "transform": ends_with_special},
    6: {"label": "Ensure the first character is a special symbol", "transform": starts_with_special},
    7: {"label": "Ensure the password contains at least one digit", "transform": contains_digit},
    8: {"label": "Ensure the password contains at least one special symbol", "transform": contains_special},
    9: {"label": "Ensure the password contains at least one uppercase letter", "transform": contains_upper},
    10: {"label": "Ensure the password contains at least one lowercase letter", "transform": contains_lower},
    11: {"label": "Pad password to length at least 8", "transform": length_at_least_8},
    12: {"label": "Pad password to length at least 12", "transform": length_at_least_12},
    13: {"label": "Pad password to length at least 16", "transform": length_at_least_16},
    14: {"label": "Append a year pattern", "transform": has_year_pattern},
    15: {"label": "Append a common password word", "transform": has_common_word},
    16: {"label": "Append a keyboard or number sequence", "transform": has_keyboard_sequence},
    17: {"label": "Create a repeated adjacent character", "transform": has_repeated_character},
    18: {"label": "Create mixed uppercase and lowercase", "transform": has_mixed_case},
    19: {"label": "Ensure the password starts with a letter", "transform": starts_with_letter},
    20: {"label": "Generate a strong password style", "transform": strong_password},
=======
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
>>>>>>> 13434496e7a9dc624ff952d4c59d945491d27061
}

RULE_IDS = tuple(RULES.keys())


def printRuleCatalog():
<<<<<<< HEAD
    print("\nCandidate transformation rules:")
=======
    print("\nCandidate mutation rules:")
>>>>>>> 13434496e7a9dc624ff952d4c59d945491d27061
    for rule_id in RULE_IDS:
        print(f"    [{rule_id}] {RULES[rule_id]['label']}")


def checkPassword(algorithm_module, k, password_files):
    print(f"\n[+] Total candidate rules: {len(RULES)}")
    print(f"[+] Number of rules to select: {k}")

    try:
<<<<<<< HEAD
        real_passwords, mutated_passwords = algorithm_module.load_passwords(password_files)
    except AttributeError:
        real_passwords, mutated_passwords = [], []

    if not real_passwords:
        print("[!] No real passwords loaded. Returning...")
        return None
    if not mutated_passwords:
        print("[!] No mutated passwords loaded. Returning...")
        return None

    print(f"[+] Loaded real passwords   : {len(real_passwords)}")
    print(f"[+] Loaded mutated passwords: {len(mutated_passwords)}")
    print("[*] Solving Maximum Coverage over real passwords using transformed mutated passwords...\n")
    return algorithm_module.solve_max_coverage(k, real_passwords, mutated_passwords)
=======
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
>>>>>>> 13434496e7a9dc624ff952d4c59d945491d27061
