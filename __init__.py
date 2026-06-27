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
                ██████╗  █████╗ ███████╗███████╗██╗    ██╗ ██████╗ ██████╗ ██████╗ 
                ██╔══██╗██╔══██╗██╔════╝██╔════╝██║    ██║██╔═══██╗██╔══██╗██╔══██╗
                ██████╔╝███████║███████╗███████╗██║ █╗ ██║██║   ██║██████╔╝██║  ██║
                ██╔═══╝ ██╔══██║╚════██║╚════██║██║███╗██║██║   ██║██╔══██╗██║  ██║
                ██║     ██║  ██║███████║███████║╚███╔███╔╝╚██████╔╝██║  ██║██████╔╝
                ╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝ ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═════╝ 
                                                                                
                 ██████╗██╗  ██╗███████╗ ██████╗██╗  ██╗██╗███╗   ██╗ ██████╗      
                ██╔════╝██║  ██║██╔════╝██╔════╝██║ ██╔╝██║████╗  ██║██╔════╝      
                ██║     ███████║█████╗  ██║     █████╔╝ ██║██╔██╗ ██║██║  ███╗     
                ██║     ██╔══██║██╔══╝  ██║     ██╔═██╗ ██║██║╚██╗██║██║   ██║     
                ╚██████╗██║  ██║███████╗╚██████╗██║  ██╗██║██║ ╚████║╚██████╔╝     
                 ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝                             
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
            k_raw = input(f"[+] Enter number of rules k (1-{max_rules}, 0 to exit): ").strip().lower()
            k = int(k_raw)
            if k == 0:
                return "exit"

            if 1 <= k <= max_rules:
                return k
            print(f"[!] Please enter a number between 1 and {max_rules}.")
        except ValueError:
            print("[!] Please enter a valid number.")


def main():
    showBanner()
    while True:
        rules.printRuleCatalog()
        selected_k = prompt_k()
        if selected_k == "exit":
            print("[*] Exiting...\n")
            break
        print(f"\n[+] Fixed number of selected rules: {selected_k}")
        print("[+] Now choose an algorithm to find the best coverage.")
        result = pwd_checking.runAlgorithms(selected_k, PASSWORD_FILES)
        if result == "exit":
            break


if __name__ == "__main__":
    main()
