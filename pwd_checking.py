try:
    from . import rules
<<<<<<< HEAD
    from .algorithms import Beam_Search as beam_search
    from .algorithms import Dynamic_Programming as dynamic_programming
    from .algorithms import Greedy as greedy
    from .algorithms import Hill_Climbing as hill_climbing
    from .algorithms import ILP_PuLP_CBC as ilp_pulp_cbc
    from .algorithms import Lagrangian_Relaxation as lagrangian_relaxation
    from .algorithms import Local_Search as local_search
    from .algorithms import Randomized_Search as randomized_search
    from .coverage_problem import load_passwords
except ImportError:
    import rules
    import algorithms.Beam_Search as beam_search
    import algorithms.Dynamic_Programming as dynamic_programming
    import algorithms.Greedy as greedy
    import algorithms.Hill_Climbing as hill_climbing
    from coverage_problem import load_passwords
    import algorithms.ILP_PuLP_CBC as ilp_pulp_cbc
    import algorithms.Lagrangian_Relaxation as lagrangian_relaxation
    import algorithms.Local_Search as local_search
    import algorithms.Randomized_Search as randomized_search


# This module is the algorithm menu controller.
# It does not solve the problem itself.
# It only:
# - loads the input data
# - shows the solver menu
# - forwards the user's choice to the correct solver module
ALGORITHMS = {
    1: ("Greedy", greedy),
    2: ("Randomized Search", randomized_search),
    3: ("Hill Climbing", hill_climbing),
    4: ("Local Search", local_search),
    5: ("Beam Search", beam_search),
    6: ("Dynamic Programming", dynamic_programming),
    7: ("ILP + PuLP + CBC", ilp_pulp_cbc),
    8: ("Lagrangian Relaxation", lagrangian_relaxation),
=======
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
>>>>>>> 30a8b8fd0e6fbf6277d0085b7730970b7b55067c
}


def printMenuAlgorithms():
<<<<<<< HEAD
    # Keep the menu text in one place so it is easy to update.
=======
>>>>>>> 30a8b8fd0e6fbf6277d0085b7730970b7b55067c
    menu = """
    [1] Greedy
    [2] Randomized Search
    [3] Hill Climbing
    [4] Local Search
    [5] Beam Search
    [6] Dynamic Programming
    [7] ILP + PuLP + CBC
    [8] Lagrangian Relaxation
    [0] Return to the previous menu
    [-1] Exit
    """
    print(menu)


def load_password_data(password_files):
<<<<<<< HEAD
    # Load both password files before the user selects an algorithm.
=======
>>>>>>> 30a8b8fd0e6fbf6277d0085b7730970b7b55067c
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
<<<<<<< HEAD
    # Map menu choice -> solver module.
=======
>>>>>>> 30a8b8fd0e6fbf6277d0085b7730970b7b55067c
    algorithm_name, algorithm_module = ALGORITHMS[choice]
    print(f"[*] Running {algorithm_name} with k = {k}...\n")
    return algorithm_module.solve_max_coverage(k, password_data)


def runAlgorithms(k, password_files):
<<<<<<< HEAD
    # This loop keeps asking until the user exits or goes back.
=======
>>>>>>> 30a8b8fd0e6fbf6277d0085b7730970b7b55067c
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
                # Support typing "e" as a quick exit.
                print("[*] Exiting...\n")
                return "exit"

            choice = int(choice_raw)

            if choice == 0:
<<<<<<< HEAD
                # Go back to the previous menu in __init__.py.
=======
                # Quay ve menu truoc.
>>>>>>> 30a8b8fd0e6fbf6277d0085b7730970b7b55067c
                print("[*] Returning to the previous menu...\n")
                return "back"

            if choice == -1:
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
