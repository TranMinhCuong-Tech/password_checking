import string


def first_char_upper(password):
    return len(password) > 0 and password[0].isupper()


def all_upper(password):
    return len(password) > 0 and password.isupper()


def all_lower(password):
    return len(password) > 0 and password.islower()


def ends_with_digit(password):
    return len(password) > 0 and password[-1].isdigit()


def ends_with_special(password):
    return len(password) > 0 and password[-1] in string.punctuation


def starts_with_special(password):
    return len(password) > 0 and password[0] in string.punctuation


def contains_digit(password):
    return any(ch.isdigit() for ch in password)


def contains_special(password):
    return any(ch in string.punctuation for ch in password)


def contains_upper(password):
    return any(ch.isupper() for ch in password)


def contains_lower(password):
    return any(ch.islower() for ch in password)


def length_at_least_8(password):
    return len(password) >= 8


def length_at_least_12(password):
    return len(password) >= 12


def length_at_least_16(password):
    return len(password) >= 16


def has_year_pattern(password):
    return any(str(year) in password for year in range(1990, 2031))


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
    return any(word in lowered for word in common_words)


def has_keyboard_sequence(password):
    sequences = ("123", "234", "345", "456", "567", "678", "789", "qwe", "asd", "zxc")
    lowered = password.lower()
    return any(sequence in lowered for sequence in sequences)


def has_repeated_character(password):
    return any(password[index] == password[index - 1] for index in range(1, len(password)))


def has_mixed_case(password):
    return contains_upper(password) and contains_lower(password)


def starts_with_letter(password):
    return len(password) > 0 and password[0].isalpha()


def strong_password(password):
    return (
        len(password) >= 12
        and contains_upper(password)
        and contains_lower(password)
        and contains_digit(password)
        and contains_special(password)
    )


RULES = {
    1: {"label": "First character is uppercase", "predicate": first_char_upper},
    2: {"label": "All characters are uppercase", "predicate": all_upper},
    3: {"label": "All characters are lowercase", "predicate": all_lower},
    4: {"label": "Last character is a digit", "predicate": ends_with_digit},
    5: {"label": "Last character is a special symbol", "predicate": ends_with_special},
    6: {"label": "First character is a special symbol", "predicate": starts_with_special},
    7: {"label": "Contains at least one digit", "predicate": contains_digit},
    8: {"label": "Contains at least one special symbol", "predicate": contains_special},
    9: {"label": "Contains at least one uppercase letter", "predicate": contains_upper},
    10: {"label": "Contains at least one lowercase letter", "predicate": contains_lower},
    11: {"label": "Length is at least 8", "predicate": length_at_least_8},
    12: {"label": "Length is at least 12", "predicate": length_at_least_12},
    13: {"label": "Length is at least 16", "predicate": length_at_least_16},
    14: {"label": "Contains a year from 1990 to 2030", "predicate": has_year_pattern},
    15: {"label": "Contains a common password word", "predicate": has_common_word},
    16: {"label": "Contains a keyboard or number sequence", "predicate": has_keyboard_sequence},
    17: {"label": "Contains repeated adjacent characters", "predicate": has_repeated_character},
    18: {"label": "Contains mixed uppercase and lowercase", "predicate": has_mixed_case},
    19: {"label": "Starts with a letter", "predicate": starts_with_letter},
    20: {"label": "Strong password pattern", "predicate": strong_password},
}

RULE_IDS = tuple(RULES.keys())


def printRuleCatalog():
    print("\nCandidate rules:")
    for rule_id in RULE_IDS:
        print(f"    [{rule_id}] {RULES[rule_id]['label']}")


def checkPassword(algorithm_module, k, password_files):
    printRuleCatalog()
    print(f"\n[+] Total candidate rules: {len(RULES)}")
    print(f"[+] Number of rules to select: {k}")

    try:
        passwords = algorithm_module.load_passwords(password_files)
    except AttributeError:
        passwords = []

    if not passwords:
        print("[!] No passwords loaded. Returning...")
        return None

    print(f"[+] Loaded passwords: {len(passwords)}")
    print("[*] Solving Maximum Coverage...\n")
    return algorithm_module.solve_max_coverage(k, passwords)
