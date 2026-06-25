REAL_PASSWORD_FILE = "real_passwords.txt"
MUTATED_PASSWORD_FILE = "mutated_passwords.txt"
PASSWORD_FILES = (REAL_PASSWORD_FILE, MUTATED_PASSWORD_FILE)


def showBanner():
    banner = """
    ==========================================
       PASSWORD CHECKING MAXIMUM COVERAGE
    ==========================================
    """
    print(banner)

    description = """
    Universe:
        - real_passwords.txt: original password dataset
        - mutated_passwords.txt: transformed password dataset

    Goal:
        Select at most k rules from rules.py so the covered passwords are maximized.
    """
    print(description)


def prompt_k():
    while True:
        try:
            k = int(input(f"[+] Enter number of rules k (1-{len(rules.RULES)}): "))
            if 1 <= k <= len(rules.RULES):
                return k
            print(f"[!] Please enter a number between 1 and {len(rules.RULES)}.")
        except ValueError:
            print("[!] Please enter a valid number.")


try:
    from . import pwd_checking
    from . import rules
except ImportError:
    import pwd_checking
    import rules


if __name__ == "__main__":
    showBanner()
    rules.printRuleCatalog()
    selected_k = prompt_k()
    pwd_checking.runAlgorithms(selected_k, PASSWORD_FILES)
