try:
    from ..coverage_problem import load_passwords, run_solver, solve_lagrangian_relaxation
except ImportError:
    from coverage_problem import load_passwords, run_solver, solve_lagrangian_relaxation


# Ham solve_max_coverage: chay lagrangian relaxation de tim loi giai gan dung.
def solve_max_coverage(k, passwords):
    return run_solver("Lagrangian Relaxation", solve_lagrangian_relaxation, k, passwords, "output_lagrangian")


# Ham check_password: ham goi chung de kiem tra mat khau.
def check_password(k, passwords=None):
    if passwords is None:
        passwords = load_passwords()
    if not passwords:
        return []
    return solve_max_coverage(k, passwords)

