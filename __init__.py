REAL_PASSWORD_FILE = "real_passwords_500_NCSC_breach_derived.txt"
MUTATED_PASSWORD_FILE = "mutated_passwords_1500.txt"
PASSWORD_FILES = (REAL_PASSWORD_FILE, MUTATED_PASSWORD_FILE)


def showBanner():
    banner = """
            ██████▄ ▄█████▄ ▄█████▄ ▄█████▄ ██ ██ ██ ▄█████▄ ██████▄ ██████▄
            ██▄▄▄██ ██▄▄▄██ ██▄▄▄▄  ██▄▄▄▄  ██ ██ ██ ██   ██ ██   ██ ██   ██
            ██▀▀▀▀  ██▀▀▀██  ▀▀▀▀██  ▀▀▀▀██ ██ ██ ██ ██   ██ ██████  ██   ██
            ██      ██   ██ ▀█████▀ ▀█████▀ ▀██████▀ ▀█████▀ ██  ▀██ ██████▀

            ▄█████▄ ██   ██ ▄██████ ▄█████▄ ██  ▄██ ▐██▌ ▄█████▄ ▄█████▄
            ██      ██▄▄▄██ ██▄▄▄▄  ██      ██▄██▀   ██  ██   ██ ██  ▄▄▄
            ██      ██▀▀▀██ ██▀▀▀▀  ██      ██▀██▄   ██  ██   ██ ██   ██
            ▀█████▀ ██   ██ ▀██████ ▀█████▀ ██  ▀██ ▐██▌ ██   ██ ▀█████▀
    """
    print(banner)

    description = """
    Universe:
        - real_passwords_500_NCSC_breach_derived.txt: original password dataset
        - mutated_passwords_1500.txt: transformed password dataset

    Goal:
        Select at most k transformation rules from rules.py so the covered real passwords are maximized.
    """
    print(description)


def prompt_k():
    while True:
        try:
            k = int(input(f"\n[+] Enter number of rules k (1-{len(rules.RULES)}): "))
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
    while True:
        rules.printRuleCatalog()
        selected_k = prompt_k()
        pwd_checking.runAlgorithms(selected_k, PASSWORD_FILES)
        user_choice = input("[+] Press Enter to choose another k, or type 0 to exit: ").strip()
        if user_choice == "0":
            print("[*] Exiting...\n")
            break
