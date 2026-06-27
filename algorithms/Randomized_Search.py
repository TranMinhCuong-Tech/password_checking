try:
    from ..coverage_problem import load_passwords, run_solver, solve_randomized_search
except ImportError:
    from coverage_problem import load_passwords, run_solver, solve_randomized_search


# Ham solve_max_coverage: chay tim kiem ngau nhien de lay loi giai tot nhat.
def solve_max_coverage(k, passwords):
    return run_solver("Randomized Search", solve_randomized_search, k, passwords, "output_randomized")


# Ham check_password: ham goi chung de kiem tra mat khau.
def check_password(k, passwords=None):
    if passwords is None:
        passwords = load_passwords()
    if not passwords:
        return []
    return solve_max_coverage(k, passwords)

