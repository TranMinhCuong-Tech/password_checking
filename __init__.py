REAL_PASSWORD_FILE = "real_passwords.txt"
MUTATED_PASSWORD_FILE = "mutated_passwords.txt"
PASSWORD_FILES = (REAL_PASSWORD_FILE, MUTATED_PASSWORD_FILE)

try:
    from . import pwd_checking
    from . import rules
except ImportError:
    import pwd_checking
    import rules


def showBanner():
    banner = """
    ==========================================
       PASSWORD CHECKING MAXIMUM COVERAGE
    ==========================================
    """
    print(banner)

    print("    Input files:")
    print(f"        - Real passwords    : {REAL_PASSWORD_FILE}")
    print(f"        - Mutated passwords : {MUTATED_PASSWORD_FILE}")
    print("\n    Goal:")
    print("        Choose exactly k mutation rules that cover the most real passwords.")


def prompt_k():
    max_rules = len(rules.RULES)
    print("\n[+] Choose fixed number of rules before selecting an algorithm.")

    while True:
        try:
            k = int(input(f"[+] Enter k (1-{max_rules}): "))
            if 1 <= k <= max_rules:
                return k
            print(f"[!] Please enter a number between 1 and {max_rules}.")
        except ValueError:
            print("[!] Please enter a valid number.")


def main():
    showBanner()
    rules.printRuleCatalog()
    selected_k = prompt_k()

    print(f"\n[+] Fixed k: {selected_k}")
    print("[+] Select an algorithm to solve Maximum Coverage.")
    pwd_checking.runAlgorithms(selected_k, PASSWORD_FILES)


if __name__ == "__main__":
    main()
