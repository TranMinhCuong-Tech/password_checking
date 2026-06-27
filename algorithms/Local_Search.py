try:
    from ..coverage_problem import load_passwords, run_solver, solve_local_search
except ImportError:
    from coverage_problem import load_passwords, run_solver, solve_local_search


def solve_max_coverage(k, passwords):
    return run_solver("Local Search", solve_local_search, k, passwords, "output_local")


def check_password(k, passwords=None):
    if passwords is None:
        passwords = load_passwords()
    if not passwords:
        return []
    return solve_max_coverage(k, passwords)

