try:
    from ..coverage_problem import load_passwords, run_solver, solve_beam_search
except ImportError:
    from coverage_problem import load_passwords, run_solver, solve_beam_search


# Ham solve_max_coverage: chay beam search de tim tap luat tot nhat.
def solve_max_coverage(k, passwords):
    return run_solver("Beam Search", solve_beam_search, k, passwords, "output_beam")


# Ham check_password: ham goi chung de kiem tra mat khau.
def check_password(k, passwords=None):
    if passwords is None:
        passwords = load_passwords()
    if not passwords:
        return []
    return solve_max_coverage(k, passwords)

