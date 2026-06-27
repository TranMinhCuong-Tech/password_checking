try:
    from ..coverage_problem import load_passwords, run_solver, solve_lagrangian_relaxation
except ImportError:
    from coverage_problem import load_passwords, run_solver, solve_lagrangian_relaxation


def solve_max_coverage(k, passwords):
    return run_solver("Lagrangian Relaxation", solve_lagrangian_relaxation, k, passwords, "output_lagrangian")


def check_password(k, passwords=None):
    if passwords is None:
        passwords = load_passwords()
    if not passwords:
        return []
    return solve_max_coverage(k, passwords)

