try:
    from ..coverage_problem import load_passwords, run_solver, solve_hill_climbing
except ImportError:
    from coverage_problem import load_passwords, run_solver, solve_hill_climbing


# Ham solve_max_coverage: chay hill climbing de toi uu tap luat.
def solve_max_coverage(k, passwords):
    return run_solver("Hill Climbing", solve_hill_climbing, k, passwords, "output_hill")


# Ham check_password: ham goi chung de kiem tra mat khau.
def check_password(k, passwords=None):
    if passwords is None:
        passwords = load_passwords()
    if not passwords:
        return []
    return solve_max_coverage(k, passwords)

