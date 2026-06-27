try:
    from ..coverage_problem import load_passwords, run_solver, solve_hill_climbing
except ImportError:
    from coverage_problem import load_passwords, run_solver, solve_hill_climbing


def solve_max_coverage(k, passwords):
    return run_solver("Hill Climbing", solve_hill_climbing, k, passwords, "output_hill")


def check_password(k, passwords=None):
    if passwords is None:
        passwords = load_passwords()
    if not passwords:
        return []
    return solve_max_coverage(k, passwords)

