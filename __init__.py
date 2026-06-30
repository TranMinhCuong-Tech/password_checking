REAL_PASSWORD_FILE = "real_passwords.txt"
MUTATED_PASSWORD_FILE = "mutated_passwords.txt"
PASSWORD_FILES = (REAL_PASSWORD_FILE, MUTATED_PASSWORD_FILE)

try:
    from . import pwd_checking
    from . import rules
except ImportError:
    import pwd_checking
    import rules


# File nay la diem vao cua du an.
# No hien thi banner, hoi k, roi chuyen quyen dieu khien sang pwd_checking.py.
# Ham ben duoi deu co comment mo ta chuc nang cua tung ham.

# Ham showBanner: in banner va thong tin dau vao cua chuong trinh.
def showBanner():
    banner = """
                ██████╗  █████╗ ███████╗███████╗██╗    ██╗ ██████╗ ██████╗ ██████╗ 
                ██╔══██╗██╔══██╗██╔════╝██╔════╝██║    ██║██╔═══██╗██╔══██╗██╔══██╗
                ██████╔╝███████║███████╗███████╗██║ █╗ ██║██║   ██║██████╔╝██║  ██║
                ██╔═══╝ ██╔══██║╚════██║╚════██║██║███╗██║██║   ██║██╔══██╗██║  ██║
                ██║     ██║  ██║███████║███████║╚███╔███╔╝╚██████╔╝██║  ██║██████╔╝
                ╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝ ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═════╝ 
                                                                                
                 ██████╗██╗  ██╗███████╗ ██████╗██╗  ██╗██╗███╗   ██╗ ██████╗      
                ██╔════╝██║  ██║██╔════╝██╔════╝██║ ██╔╝██║████╗  ██║██╔════╝      
                ██║     ███████║█████╗  ██║     █████╔╝ ██║██╔██╗ ██║██║  ███╗     
                ██║     ██╔══██║██╔══╝  ██║     ██╔═██╗ ██║██║╚██╗██║██║   ██║     
                ╚██████╗██║  ██║███████╗╚██████╗██║  ██╗██║██║ ╚████║╚██████╔╝     
                 ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝                             
    """
    print(banner)

    print("    File dau vao:")
    print(f"        - Mat khau that    : {REAL_PASSWORD_FILE}")
    print(f"        - Mat khau bien doi: {MUTATED_PASSWORD_FILE}")
    print("\n    Muc tieu:")
    print("        Chon dung k luat bien doi de phu duoc nhieu mat khau that nhat.")

# Ham prompt_k: hoi nguoi dung nhap so luat can chon.
def prompt_k():
    # Hoi nguoi dung can chon bao nhieu luat.
    max_rules = len(rules.RULES)
    print("\n[+] Hay chon so luat co dinh truoc khi chon thuat toan.")

    while True:
        try:
            k_raw = input(f"[+] Nhap so luat k (1-{max_rules}, 0 de thoat): ").strip().lower()
            k = int(k_raw)
            if k == 0:
                return "exit"

            if 1 <= k <= max_rules:
                return k
            print(f"[!] Vui long nhap so trong khoang 1 den {max_rules}.")
        except ValueError:
            print("[!] Vui long nhap mot so hop le.")

# Ham main: dieu khien luong chay chinh cua chuong trinh.
def main():
    # Vong lap chinh:
    # 1) hien thi danh muc luat
    # 2) hoi gia tri k
    # 3) cho nguoi dung chon mot thuat toan
    showBanner()
    while True:
        rules.printRuleCatalog()
        selected_k = prompt_k()
        if selected_k == "exit":
            print("[*] Dang thoat...\n")
            break
        print(f"\n[+] So luat da chon co dinh: {selected_k}")
        print("[+] Bay gio hay chon mot thuat toan de tim do phu tot nhat.")
        result = pwd_checking.runAlgorithms(selected_k, PASSWORD_FILES)
        if result == "exit":
            break


if __name__ == "__main__":
    main()