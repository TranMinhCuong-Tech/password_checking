try:
    from ..coverage_problem import run_solver, load_passwords, solve_dp
except ImportError:
    from coverage_problem import run_solver, load_passwords, solve_dp


def solve_max_coverage(k, real_passwords, mutated_passwords=None):
    # Goi giai phap exact co memoization
    if mutated_passwords is None and isinstance(real_passwords, (tuple, list)):
        real_passwords, mutated_passwords = real_passwords
    return run_solver("dynamic programming", solve_dp, k, real_passwords, mutated_passwords, "output_dp")


def check_password(k, passwords=None):
    # Ham goi chung de giu cau truc dong nhat voi module khac
    if passwords is None:
        passwords = load_passwords()
    if not passwords or len(passwords) != 2:
        return []
    real_passwords, mutated_passwords = passwords
    if not real_passwords or not mutated_passwords:
        return []
    return solve_max_coverage(k, real_passwords, mutated_passwords)
