import string
import time
import tracemalloc

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


def standard_password(password):
    """
    Standard Password:
    - First character is uppercase
    - Contains at least one digit
    - Contains at least one special character
    - Length > 15
    """
    return (
        len(password) > 15
        and password[0].isupper()
        and any(c.isdigit() for c in password)
        and any(c in string.punctuation for c in password)
    )


RULES = {
    1: (first_char_upper,    "output_brute_first_char_upper.txt"),
    2: (all_upper,           "output_brute_all_upper.txt"),
    3: (all_lower,           "output_brute_all_lower.txt"),
    4: (ends_with_digit,     "output_brute_ends_with_digit.txt"),
    5: (ends_with_special,   "output_brute_ends_with_special.txt"),
    6: (starts_with_special, "output_brute_starts_with_special.txt"),
    7: (standard_password,   "output_brute_standard_password.txt"),
}



def load_passwords(filename="passwords.txt"):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[!] File '{filename}' not found.")
        return []


def save_results(passwords, filename):
    with open(filename, "w", encoding="utf-8") as f:
        for password in passwords:
            f.write(password + "\n")
    print(f"[+] Results saved to: {filename}")



def benchmark(rule_function, passwords, output_file):
    tracemalloc.start()
    start_time = time.perf_counter()

    # Brute Force: duyệt toàn bộ, không bỏ qua bất kỳ phần tử nào
    matched = []
    for password in passwords:
        if rule_function(password):
            matched.append(password)

    end_time = time.perf_counter()
    current_memory, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    save_results(matched, output_file)

    print("\n============= BRUTE FORCE RESULT =============")
    print(f"[+] Rule            : {rule_function.__name__}")
    print(f"[+] Solutions Found : {len(matched)}")
    print(f"[+] Execution Time  : {end_time - start_time:.6f} s")
    print(f"[+] Current Memory  : {current_memory / 1024:.2f} KB")
    print(f"[+] Peak Memory     : {peak_memory / 1024:.2f} KB")
    print("===============================================")

    return matched


def check_password(choice, passwords=None):
    if passwords is None:
        passwords = load_passwords()
    if not passwords:
        return []

    if choice == 0:
        print("[*] Exiting...")
        return []

    if choice not in RULES:
        print("[!] Invalid choice!")
        return []

    rule_function, output_file = RULES[choice]
    return benchmark(rule_function, passwords, output_file)