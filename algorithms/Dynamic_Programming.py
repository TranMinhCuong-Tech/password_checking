"""
Dynamic Programming (Memoization / Caching)
--------------------------------------------
Ý tưởng DP áp dụng vào bài toán password checking:

1. **Memoize kết quả sub-problems** – Nhiều password trong thực tế chia sẻ
   prefix chung (vd: "Password1!", "Password1@").  DP lưu kết quả kiểm tra
   từng prefix vào cache; lần sau gặp lại prefix đó → tra bảng O(1).

2. **Precompute character-class table** – Xây dựng một lần bảng
   `char_class[ord(ch)]` cho toàn bộ ASCII printable, tránh gọi lại
   `isupper()`, `isdigit()`, `in punctuation` trong vòng lặp nóng.

3. **Incremental state accumulation** – Với rule "standard password",
   dùng tuple (has_digit, has_special) như "state" DP, cập nhật dần
   theo từng ký tự thay vì rescan.

Trade-off:
- Cache tốt khi dataset có nhiều prefix trùng nhau.
- Overhead dict lookup nếu dataset toàn password unique → không bằng Greedy.

Time  : O(n * m) worst, gần O(n) best (cache hit rate cao)
Space : O(u * m) — u: số prefix unique trong dataset
"""

import string
import time
import tracemalloc
from functools import lru_cache

_CC_UPPER   = 1
_CC_LOWER   = 2
_CC_DIGIT   = 3
_CC_SPECIAL = 4
_CC_OTHER   = 0

_SPECIAL_SET = frozenset(string.punctuation)

# Build lookup table for all 128 ASCII chars (index = ord value)
_CHAR_CLASS = [_CC_OTHER] * 128
for _i in range(128):
    _ch = chr(_i)
    if _ch.isupper():
        _CHAR_CLASS[_i] = _CC_UPPER
    elif _ch.islower():
        _CHAR_CLASS[_i] = _CC_LOWER
    elif _ch.isdigit():
        _CHAR_CLASS[_i] = _CC_DIGIT
    elif _ch in _SPECIAL_SET:
        _CHAR_CLASS[_i] = _CC_SPECIAL


def _char_class(ch):
    o = ord(ch)
    return _CHAR_CLASS[o] if o < 128 else (_CC_SPECIAL if ch in _SPECIAL_SET else _CC_OTHER)


@lru_cache(maxsize=None)
def _dp_all_same_class(password, target_class):
    """DP: kiểm tra mọi ký tự trong password thuộc target_class."""
    if not password:
        return False
    if _char_class(password[-1]) != target_class:
        return False
    if len(password) == 1:
        return True
    return _dp_all_same_class(password[:-1], target_class)


@lru_cache(maxsize=None)
def _dp_has_class(password, target_class):
    """DP: kiểm tra tồn tại ít nhất 1 ký tự thuộc target_class."""
    if not password:
        return False
    if _char_class(password[-1]) == target_class:
        return True
    return _dp_has_class(password[:-1], target_class)


def first_char_upper(password):
    return len(password) > 0 and _char_class(password[0]) == _CC_UPPER


def all_upper(password):
    return _dp_all_same_class(password, _CC_UPPER)


def all_lower(password):
    return _dp_all_same_class(password, _CC_LOWER)


def ends_with_digit(password):
    return len(password) > 0 and _char_class(password[-1]) == _CC_DIGIT


def ends_with_special(password):
    return len(password) > 0 and _char_class(password[-1]) == _CC_SPECIAL


def starts_with_special(password):
    return len(password) > 0 and _char_class(password[0]) == _CC_SPECIAL


def standard_password(password):
    """
    DP Standard Password:
    - Dùng _dp_has_class (memoized) để kiểm tra digit + special.
    - Điều kiện rẻ (len, first char) kiểm tra trước để short-circuit.
    """
    if len(password) <= 15:
        return False
    if _char_class(password[0]) != _CC_UPPER:
        return False
    return _dp_has_class(password, _CC_DIGIT) and _dp_has_class(password, _CC_SPECIAL)


RULES = {
    1: (first_char_upper,    "output_dp_first_char_upper.txt"),
    2: (all_upper,           "output_dp_all_upper.txt"),
    3: (all_lower,           "output_dp_all_lower.txt"),
    4: (ends_with_digit,     "output_dp_ends_with_digit.txt"),
    5: (ends_with_special,   "output_dp_ends_with_special.txt"),
    6: (starts_with_special, "output_dp_starts_with_special.txt"),
    7: (standard_password,   "output_dp_standard_password.txt"),
}

def load_passwords(filename="passwords.txt"):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[!] File '{filename}' not found.")
        return []


def save_results(passwords, filename):
    with open(filename, "w", encoding="utf-8") as f:
        for password in passwords:
            f.write(password + "\n")
    print(f"[+] Results saved to: {filename}")

def benchmark(rule_function, passwords, output_file):
    # Clear cache giữa các lần benchmark để đo fair
    _dp_all_same_class.cache_clear()
    _dp_has_class.cache_clear()

    tracemalloc.start()
    start_time = time.perf_counter()

    matched = []
    for password in passwords:
        if rule_function(password):
            matched.append(password)

    end_time = time.perf_counter()
    current_memory, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    save_results(matched, output_file)

    # Cache stats
    hits_all  = _dp_all_same_class.cache_info()
    hits_has  = _dp_has_class.cache_info()
    total_hits = hits_all.hits + hits_has.hits

    print("\n============= DYNAMIC PROGRAMMING RESULT =============")
    print(f"[+] Rule            : {rule_function.__name__}")
    print(f"[+] Solutions Found : {len(matched)}")
    print(f"[+] Execution Time  : {end_time - start_time:.6f} s")
    print(f"[+] Current Memory  : {current_memory / 1024:.2f} KB")
    print(f"[+] Peak Memory     : {peak_memory / 1024:.2f} KB")
    print(f"[+] Cache Hits      : {total_hits}")
    print("=======================================================")

    return matched

def check_password(choice, passwords=None):
    if passwords is None:
        passwords = load_passwords()
    if not passwords:
        return []

    if choice == 0:
        print("[*] Exiting...")
        return []

    if choice not in RULES:
        print("[!] Invalid choice!")
        return []

    rule_function, output_file = RULES[choice]
    return benchmark(rule_function, passwords, output_file)