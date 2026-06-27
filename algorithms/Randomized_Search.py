try:
    from ..coverage_problem import load_passwords, run_solver, solve_randomized_search
except ImportError:
    from coverage_problem import load_passwords, run_solver, solve_randomized_search


def solve_max_coverage(k, passwords):
    return run_solver("Randomized Search", solve_randomized_search, k, passwords, "output_randomized")


def check_password(k, passwords=None):
    if passwords is None:
        passwords = load_passwords()
    if not passwords:
        return []
    return solve_max_coverage(k, passwords)

