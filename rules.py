try:
    from .coverage_problem import RULES
except ImportError:
    from coverage_problem import RULES


def printRuleCatalog():
    """
    In danh sach rule ung vien.
    Day la tap cac set co the duoc chon trong bai toan maximum coverage.
    """
    menu = """
    Candidate rules:
    [1] First character is uppercase
    [2] All characters are uppercase
    [3] All characters are lowercase
    [4] Last character is a digit
    [5] Last character is a special symbol
    [6] First character is a special symbol
    [7] Standard password
    [0] Return to previous menu
    """
    print(menu)


def _prompt_k():
    """Nhap so rule can chon va kiem tra hop le."""
    while True:
        try:
            k = int(input(f"[+] Enter your choice: "))
            if 0 <= k <= len(RULES):
                return k
            print(f"[!] Please enter a number between 0 and {len(RULES)}.")
        except ValueError:
            print("[!] Please enter a valid number!")


def checkPassword(algorithm_module):
    """
    Chon k rule va goi solver.
    Ket qua in ra chi gom cac rule da chon va cac password duoc phu.
    Nguoi dung co the nhap lai k neu muon chay tiep.
    """
    try:
        passwords = algorithm_module.load_passwords()
    except AttributeError:
        passwords = []

    if not passwords:
        print("[!] No passwords loaded. Returning...")
        return

    while True:
        printRuleCatalog()
        print(f"[+] Total candidate rules: {len(RULES)}")
        k = _prompt_k()

        if k == 0:
            # Quay lai menu truoc neu nguoi dung chon 0.
            print("[*] Returning to previous menu...\n")
            break

        # Goi solver theo thuat toan da chon.
        print("[*] Solving maximum coverage...\n")
        algorithm_module.solve_max_coverage(k, passwords)
