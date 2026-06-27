try:
    from . import rules
    from .algorithms import Brute_Force as brute_force
    from .algorithms import Dynamic_Programming as dynamic_programming
    from .algorithms import Greedy as greedy
    from .algorithms import ILP_PuLP_CBC as ilp_pulp_cbc
    from .coverage_problem import load_passwords
except ImportError:
    import rules
    import algorithms.Brute_Force as brute_force
    import algorithms.Dynamic_Programming as dynamic_programming
    import algorithms.Greedy as greedy
    from coverage_problem import load_passwords
    import algorithms.ILP_PuLP_CBC as ilp_pulp_cbc


ALGORITHMS = {
    1: ("Brute Force", brute_force),
    2: ("Greedy", greedy),
    3: ("ILP_PuLP_CBC", ilp_pulp_cbc),
    4: ("Dynamic Programming", dynamic_programming),
}


def printMenuAlgorithms():
    menu = """
    [1] Brute Force
    [2] Greedy
    [3] ILP_PuLP_CBC (PuLP + CBC)
    [4] Dynamic Programming
    [0] Return to the previous menu
    [-1] Exit
    """
    print(menu)


def load_password_data(password_files):
    password_data = load_passwords(password_files)
    real_count = len(password_data.get("real", []))
    mutated_count = len(password_data.get("mutated", []))

    print(f"[+] Loaded real passwords    : {real_count}")
    print(f"[+] Loaded mutated passwords : {mutated_count}")

    if real_count == 0 or mutated_count == 0:
        print("[!] Missing password data. Please check input files.")
        return None

    return password_data


def run_selected_algorithm(choice, k, password_data):
    algorithm_name, algorithm_module = ALGORITHMS[choice]
    print(f"[*] Running {algorithm_name} with k = {k}...\n")
    return algorithm_module.solve_max_coverage(k, password_data)


def runAlgorithms(k, password_files):
    password_data = load_password_data(password_files)
    if password_data is None:
        return

    print(f"[+] Total candidate rules    : {len(rules.RULES)}")
    print(f"[+] Fixed selected rules k   : {k}")

    while True:
        try:
            printMenuAlgorithms()
            choice_raw = input("\n[+] Enter your choice: ").strip().lower()

            if choice_raw == "e":
                # Thoat chuong trinh.
                print("[*] Exiting...\n")
                return "exit"

            choice = int(choice_raw)

            if choice == 0:
                # Quay ve menu truoc.
                print("[*] Returning to the previous menu...\n")
                return "back"

            elif choice == -1:
                # Thoat chuong trinh.
                print("[*] Exiting...\n")
                return "exit"

            if choice not in ALGORITHMS:
                print("[!] Invalid choice!")
                continue

            run_selected_algorithm(choice, k, password_data)

        except ValueError:
            print("[!] Please enter a valid number!")


if __name__ == "__main__":
    runAlgorithms(3, ("real_passwords.txt", "mutated_passwords.txt"))
