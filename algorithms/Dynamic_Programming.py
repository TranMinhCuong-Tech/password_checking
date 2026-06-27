try:
    from ..coverage_problem import run_solver, load_passwords, solve_dp
except ImportError:
    from coverage_problem import run_solver, load_passwords, solve_dp


# Ham solve_max_coverage: chay dynamic programming de tim loi giai chinh xac.
def solve_max_coverage(k, passwords):
    # Goi giai phap chinh xac co memoization
    return run_solver("Dynamic Programming", solve_dp, k, passwords, "output_dp")


# Ham check_password: ham goi chung de kiem tra mat khau.
def check_password(k, passwords=None):
    # Ham goi chung de giu cau truc dong nhat voi module khac
    if passwords is None:
        passwords = load_passwords()
    if not passwords:
        return []
    return solve_max_coverage(k, passwords)
