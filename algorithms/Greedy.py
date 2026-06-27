try:
    from ..coverage_problem import run_solver, load_passwords, solve_greedy
except ImportError:
    from coverage_problem import run_solver, load_passwords, solve_greedy


# Ham solve_max_coverage: chay giai phap tham lam de lay phu lon.
def solve_max_coverage(k, passwords):
    # Goi giai phap tham lam xap xi
    return run_solver("Greedy", solve_greedy, k, passwords, "output_greedy")


# Ham check_password: ham goi chung de kiem tra mat khau.
def check_password(k, passwords=None):
    # Ham goi chung de giu cau truc dong nhat voi module khac
    if passwords is None:
        passwords = load_passwords()
    if not passwords:
        return []
    return solve_max_coverage(k, passwords)
