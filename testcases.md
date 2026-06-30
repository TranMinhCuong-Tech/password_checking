# Test Cases for Password Checking Maximum Coverage

Tài liệu này tổng hợp một bộ test tổng quát cho project `password_checking_maximum_coverage`.

Mục tiêu:

- tránh phải liệt kê toàn bộ ma trận `Rules x Algorithms x k` bằng brute force
- vẫn bao phủ được các hành vi quan trọng của project
- dùng `Brute Force` làm chuẩn tham chiếu cho các bộ test nhỏ
- kiểm tra cả tính đúng, tính ổn định, và tính hợp lệ của kết quả

---

## 1. Nguyên tắc thiết kế test

### 1.1. Không test exhaustive trên toàn bộ dữ liệu lớn

Không nên chạy brute force cho mọi tổ hợp `k = 1..20` trên toàn bộ dataset thật, vì:

- số tổ hợp tăng rất nhanh theo `C(n, k)`
- thời gian chạy sẽ tăng mạnh khi `k` lớn
- mục tiêu test là bao phủ hành vi, không phải duyệt hết mọi khả năng

### 1.2. Dùng brute force làm oracle cho bài nhỏ

Với các bộ dữ liệu nhỏ, `Brute Force` là kết quả chuẩn để đối chiếu:

- `Brute Force` là exact solver
- các solver khác không được vượt quá kết quả brute force trên cùng input
- `ILP + PuLP + CBC` cũng nên khớp brute force nếu solver chạy đúng

### 1.3. Chia test theo lớp phủ

Tập test được chia thành:

- boundary test
- coverage test
- algorithm consistency test
- property-based test
- metamorphic test

---

## 2. Bộ test theo mục tiêu

### 2.1. Boundary tests

| Test ID | Mục tiêu | Input chính | Kết quả mong đợi |
|---|---|---|---|
| B1 | `k = 1` | dataset chuẩn, chọn 1 rule | chương trình chạy bình thường, trả về đúng 1 rule nếu có đủ dữ liệu |
| B2 | `k = 2` | dataset chuẩn, chọn 2 rule | kết quả hợp lệ, coverage không giảm so với `k = 1` |
| B3 | `k = 3` | dataset chuẩn, chọn 3 rule | solver exact cho ra nghiệm tối ưu trên dataset nhỏ |
| B4 | `k = 5` | dataset chuẩn | kiểm tra độ ổn định khi số rule tăng |
| B5 | `k = 20` | dataset chuẩn | kiểm tra giới hạn lớn nhất của menu rules |
| B6 | `k > 20` | nhập giá trị vượt giới hạn | chương trình phải chặn input hoặc báo lỗi hợp lệ |
| B7 | `k = 0` | nhập 0 | chương trình thoát hoặc quay về menu theo thiết kế |
| B8 | dữ liệu rỗng | file real hoặc mutated rỗng | chương trình báo lỗi dữ liệu thiếu |

### 2.2. Coverage tests

| Test ID | Mục tiêu | Dataset gợi ý | Kết quả mong đợi |
|---|---|---|---|
| C1 | kích hoạt `identity_short` | password độ dài `<= 6` | rule này có thể phủ một phần universe |
| C2 | kích hoạt `identity_medium` | password độ dài `7..10` | rule này có coverage rõ ràng |
| C3 | kích hoạt `identity_long` | password độ dài `>= 11` | rule này phủ được các password dài |
| C4 | kích hoạt `append_single_digit` | password có thể sinh ra biến thể số cuối | coverage lớn hơn hoặc bằng các rule identity trong dữ liệu phù hợp |
| C5 | kích hoạt `append_double_digit` | password có thể sinh ra 00, 11, 22... | candidate phải được nhận đúng |
| C6 | kích hoạt `append_123` | password có thể ghép `123` | coverage phản ánh đúng rule append |
| C7 | kích hoạt `append_year` | password có thể ghép năm | kết quả phải đúng với khoảng năm đã định nghĩa |
| C8 | kích hoạt `append_special` | password có thể ghép ký tự đặc biệt | phát hiện đúng biến thể `! @ # $ %` |
| C9 | kích hoạt `prepend_single_digit` | password có thể thêm số ở đầu | candidate đúng vị trí tiền tố |
| C10 | kích hoạt `prepend_123` | password có thể thêm `123` ở đầu | candidate đúng vị trí tiền tố |
| C11 | kích hoạt `reverse` | password không đối xứng | đảo chuỗi phải chính xác |
| C12 | kích hoạt leet rules | password chứa `a/o/e/s` | thay thế leet phải đúng mapping |
| C13 | kích hoạt `mixed_leet` | password chứa nhiều ký tự leet | kết quả phải kết hợp nhiều thay thế |
| C14 | kích hoạt `keyboard_walk` | password ghép được chuỗi bàn phím | candidate sinh ra đúng danh sách walk |
| C15 | kích hoạt `duplicate_last_char` | password không rỗng | ký tự cuối được lặp lại đúng |
| C16 | overlap mạnh | một password phủ bởi nhiều rules | solver phải xử lý union đúng, không đếm trùng |
| C17 | không rule nào khớp | password bất thường | coverage của password đó phải bằng 0 |

### 2.3. Algorithm consistency tests

Các test này dùng dataset nhỏ để so sánh giữa các solver.

| Test ID | Mục tiêu | Solver so sánh | Kết quả mong đợi |
|---|---|---|---|
| A1 | brute force làm chuẩn | Brute Force vs Greedy | Greedy không được vượt brute force |
| A2 | brute force làm chuẩn | Brute Force vs Randomized Search | Randomized Search không được vượt brute force |
| A3 | brute force làm chuẩn | Brute Force vs Hill Climbing | Hill Climbing không được vượt brute force |
| A4 | exact solver khớp nhau | Brute Force vs Dynamic Programming | kết quả coverage phải bằng nhau trên bài nhỏ |
| A5 | exact solver khớp nhau | Brute Force vs ILP + PuLP + CBC | kết quả coverage phải bằng nhau trên bài nhỏ nếu CBC chạy đúng |
| A6 | heuristic stability | nhiều lần chạy Randomized Search | coverage dao động trong phạm vi hợp lệ |
| A7 | output format | mọi solver | file output được tạo đúng tên và đúng định dạng |

### 2.4. Property-based tests

| Test ID | Property | Cách kiểm tra | Kết quả mong đợi |
|---|---|---|---|
| P1 | số rule chọn ra không vượt `k` | kiểm tra độ dài `selected_rule_ids` | đúng bằng `k` hoặc nhỏ hơn nếu dữ liệu không đủ |
| P2 | coverage không âm | kiểm tra `coverage_count` | luôn `>= 0` |
| P3 | coverage không vượt tổng số password thật | kiểm tra `coverage_count <= total_passwords` | luôn đúng |
| P4 | brute force là tối ưu trên bài nhỏ | so với các solver khác | không solver nào vượt brute force |
| P5 | tăng `k` thì coverage tối đa không giảm | so sánh `k = 1, 2, 3...` | coverage tốt nhất không giảm theo `k` |
| P6 | output phải nhất quán | đọc file output và so với result in console | nội dung khớp nhau |

### 2.5. Metamorphic tests

| Test ID | Biến đổi input | Quan hệ kỳ vọng |
|---|---|---|
| M1 | thêm password không liên quan vào `real_passwords.txt` | coverage của các rule không đổi ở phần cốt lõi |
| M2 | đổi thứ tự password trong file | kết quả coverage không đổi, chỉ có thể khác thứ tự hiển thị |
| M3 | nhân đôi dữ liệu đầu vào | logic chọn rule không sai, chỉ thay đổi số lượng thống kê |
| M4 | thêm candidate không khớp vào `mutated_passwords.txt` | các rule cũ không bị ảnh hưởng |
| M5 | chạy lại cùng input nhiều lần với solver deterministic | kết quả không đổi |

---

## 3. Bộ dataset đại diện

Để test tổng quát mà không tốn quá nhiều thời gian, nên chuẩn bị các dataset nhỏ sau:

| Dataset | Mục tiêu | Nội dung gợi ý |
|---|---|---|
| T1 | kiểm tra rule đơn lẻ | chỉ chứa password phù hợp với `identity_short` hoặc `capitalize` |
| T2 | kiểm tra overlap | nhiều password có thể bị phủ bởi nhiều rule cùng lúc |
| T3 | kiểm tra leet/reverse | password chứa `a/o/e/s`, chuỗi đối xứng và không đối xứng |
| T4 | kiểm tra dữ liệu biên | password rỗng, 1 ký tự, rất ngắn, rất dài |
| T5 | kiểm tra bài thực tế nhỏ | lấy một phần nhỏ từ dataset thật để brute force được |
| T6 | kiểm tra dữ liệu xấu | không có password nào match mutated |

---

## 4. Ma trận chạy khuyến nghị

Không cần chạy mọi algorithm với mọi `k` trên mọi dataset lớn.

### 4.1. Bộ test tối thiểu nhưng đủ mạnh

| Dataset | k | Algorithms cần chạy |
|---|---:|---|
| T1 | 1 | Brute Force, Greedy, ILP + PuLP + CBC |
| T1 | 2 | Brute Force, Greedy, ILP + PuLP + CBC |
| T2 | 3 | Brute Force, Greedy, Randomized Search, ILP + PuLP + CBC |
| T3 | 3 | Brute Force, Greedy, Hill Climbing, Dynamic Programming |
| T4 | 1 | tất cả solver để kiểm tra xử lý biên |
| T5 | 3 | tất cả solver exact + heuristic |
| T6 | 1 | tất cả solver để kiểm tra coverage bằng 0 |

### 4.2. Bộ test thực tế khi chấm bài

Nếu muốn giảm thời gian:

- dùng `Brute Force` chỉ cho `k = 1..3`
- dùng `Dynamic Programming` và `ILP` cho bài nhỏ
- dùng heuristic cho bài lớn

---

## 5. Ví dụ tiêu chí pass/fail

### Pass

- chương trình không crash
- menu hiển thị đúng thứ tự thuật toán
- `Brute Force` trả về kết quả tối ưu cho dataset nhỏ
- `Greedy` và các heuristic trả về kết quả hợp lệ
- file output được tạo đúng tên
- `coverage_count` hợp lệ và không vượt số password thật

### Fail

- solver trả về số rule sai
- coverage âm hoặc vượt tổng số password
- output file sai format
- exact solver không khớp brute force trên dataset nhỏ
- menu thuật toán không đúng thứ tự mới

---

## 6. Kết luận

Bộ test này cho phép kiểm tra project theo cách:

- đủ tổng quát
- không tốn quá nhiều thời gian
- vẫn dùng brute force làm chuẩn khi cần

Nếu cần mở rộng hơn, có thể thêm:

- testcase riêng cho từng rule
- testcase riêng cho từng solver
- testcase benchmark thời gian chạy

