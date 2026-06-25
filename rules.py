import string


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


RULES = {
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
}

RULE_IDS = tuple(RULES.keys())


def printRuleCatalog():
    print("\nCandidate transformation rules:")
    for rule_id in RULE_IDS:
        print(f"    [{rule_id}] {RULES[rule_id]['label']}")


def checkPassword(algorithm_module, k, password_files):
    printRuleCatalog()
    print(f"\n[+] Total candidate rules: {len(RULES)}")
    print(f"[+] Number of rules to select: {k}")

    try:
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
