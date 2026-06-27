try:
    from ..coverage_problem import run_solver, load_passwords, solve_ilp_pulp_cbc
except ImportError:
    from coverage_problem import run_solver, load_passwords, solve_ilp_pulp_cbc


# Ham solve_max_coverage: chay ILP voi PuLP va CBC de tim loi giai chinh xac.
def solve_max_coverage(k, passwords):
    # Giai bai Maximum Coverage bang ILP voi PuLP va CBC.
    return run_solver("ILP + PuLP + CBC", solve_ilp_pulp_cbc, k, passwords, "output_ILP_PuLP_CBC")


# Ham check_password: ham goi chung de kiem tra mat khau.
def check_password(k, passwords=None):
    # Ham goi chung de giu cau truc dong nhat voi module khac
    if passwords is None:
        passwords = load_passwords()
    if not passwords:
        return []
    return solve_max_coverage(k, passwords)
