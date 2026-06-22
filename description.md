# Mô tả dự án: Password Checking theo bài toán Maximum Coverage

## 1. Tổng quan

Dự án này mô hình hóa việc lựa chọn các quy tắc kiểm tra mật khẩu dưới dạng bài toán **Maximum Coverage**. Thay vì kiểm tra một mật khẩu đơn lẻ theo từng điều kiện, project xem toàn bộ danh sách mật khẩu trong `passwords.txt` như một **tập vũ trụ** và mỗi quy tắc như một **tập con** chứa những mật khẩu thỏa quy tắc đó.

Mục tiêu của bài toán là chọn tối đa `k` quy tắc sao cho hợp của các tập con tương ứng bao phủ được nhiều mật khẩu nhất có thể.

Nói cách khác:

- `passwords.txt` là tập cha chứa toàn bộ phần tử đầu vào.
- Mỗi quy tắc là một cách tạo ra một tập con từ tập cha theo một điều kiện nhất định.
- Người dùng chọn số lượng quy tắc `k`.
- Chương trình tìm tổ hợp quy tắc tốt nhất để bao phủ được nhiều mật khẩu nhất.

Đây chính là một cách biểu diễn rất điển hình của bài toán tối ưu tổ hợp, nơi ta không chỉ cần “có thỏa điều kiện hay không”, mà còn phải “thỏa điều kiện tốt đến mức nào”.

---

## 2. Lý thuyết nền tảng

### 2.1. Bài toán quyết định, NP và NP-hard

Trong lý thuyết độ phức tạp tính toán, nhiều bài toán được chia thành các lớp:

- **P**: các bài toán có thể giải trong thời gian đa thức.
- **NP**: các bài toán mà nếu cho trước một lời giải ứng viên, ta có thể kiểm tra lời giải đó trong thời gian đa thức.
- **NP-complete**: các bài toán vừa thuộc NP, vừa là khó nhất trong NP.
- **NP-hard**: các bài toán ít nhất cũng khó như mọi bài toán trong NP, nhưng bản thân chúng không nhất thiết phải thuộc NP.

Ý nghĩa trực quan:

- Nếu một bài toán thuộc **P**, ta thường kỳ vọng có thuật toán nhanh khi dữ liệu lớn.
- Nếu một bài toán là **NP-hard**, thì rất khó tìm thuật toán tối ưu chạy nhanh cho mọi trường hợp.

Trong bối cảnh của dự án này, việc chọn đúng `k` quy tắc để tối đa hóa số mật khẩu được phủ là một bài toán tổ hợp có không gian tìm kiếm tăng rất nhanh theo số quy tắc. Khi số quy tắc lớn hơn, số cách chọn tổ hợp tăng theo cấp số tổ hợp, khiến bài toán trở nên rất khó giải tối ưu trong thời gian ngắn.

### 2.2. Maximum Coverage là gì?

Bài toán **Maximum Coverage** có dạng:

- Cho một tập vũ trụ `U`.
- Cho một họ các tập con `S_1, S_2, ..., S_m`.
- Chọn nhiều nhất `k` tập con sao cho số phần tử trong hợp của chúng là lớn nhất.

Mục tiêu:

```text
maximize |S_1 ∪ S_2 ∪ ... ∪ S_k|
```

Ràng buộc:

```text
chọn không quá k tập con
```

Đây là một bài toán tối ưu chuẩn trong nghiên cứu thuật toán, có liên hệ gần với **Set Cover**:

- **Set Cover**: phủ toàn bộ tập vũ trụ bằng ít tập nhất.
- **Maximum Coverage**: với số tập bị giới hạn, phủ được nhiều phần tử nhất.

Hai bài toán này đều thuộc nhóm bài toán tổ hợp khó, và thường được dùng để minh họa cho tư duy thiết kế thuật toán exact, greedy, dynamic programming và các mô hình ràng buộc.

### 2.3. Vì sao bài toán này là NP-hard?

Maximum Coverage là một bài toán **NP-hard** vì:

- Không gian lựa chọn các tập con tăng rất nhanh theo số tập ứng viên.
- Muốn tìm lời giải tối ưu, ta thường phải xét nhiều tổ hợp khả dĩ.
- Khi số lượng tập ứng viên đủ lớn, việc duyệt hết mọi khả năng trở nên không khả thi.

Điều quan trọng là:

- Nếu ai đó đưa cho ta một tập `k` quy tắc cụ thể, ta có thể kiểm tra nhanh số mật khẩu được phủ.
- Nhưng để tìm ra tập `k` quy tắc tốt nhất thì lại rất khó.

Đó là dấu hiệu điển hình của một bài toán tối ưu thuộc nhóm khó.

---

## 3. Ánh xạ bài toán vào project

### 3.1. Tập vũ trụ

Trong project, tập cha `U` chính là toàn bộ mật khẩu đọc từ file `passwords.txt`.

Mỗi dòng không rỗng trong file là một phần tử của `U`.

Ví dụ:

```text
U = {password_1, password_2, password_3, ..., password_n}
```

### 3.2. Tập con ứng với từng quy tắc

Mỗi quy tắc trong project xác định một tập con:

```text
S_i = { password ∈ U | password thỏa quy tắc i }
```

Trong code, các quy tắc này được định nghĩa trong `coverage_problem.py` và được lưu trong biến `RULES`.

Các quy tắc ứng viên hiện có:

1. Ký tự đầu tiên là chữ hoa
2. Toàn bộ ký tự là chữ hoa
3. Toàn bộ ký tự là chữ thường
4. Ký tự cuối cùng là chữ số
5. Ký tự cuối cùng là ký tự đặc biệt
6. Ký tự đầu tiên là ký tự đặc biệt
7. Mật khẩu chuẩn

### 3.3. Ý nghĩa của việc chọn `k` quy tắc

Người dùng chọn một số `k`.

Chương trình sẽ tìm ra một tập các quy tắc có kích thước `k` sao cho:

```text
|S_a ∪ S_b ∪ ... ∪ S_k|
```

là lớn nhất.

Nói đơn giản:

- mỗi quy tắc bao phủ một nhóm mật khẩu;
- nhiều quy tắc có thể chồng lấn lên nhau;
- mục tiêu là chọn `k` quy tắc có tổng vùng phủ lớn nhất, tránh lãng phí vào các phần tử bị đếm lặp.

### 3.4. Vì sao dùng bitmask?

Trong `coverage_problem.py`, mỗi quy tắc được chuyển thành một **bitmask**:

- bit thứ `i` = `1` nếu mật khẩu thứ `i` thuộc tập con của quy tắc;
- bit thứ `i` = `0` nếu không thuộc.

Nhờ đó:

- hợp của hai tập con trở thành phép `OR` bit;
- số phần tử được phủ được tính nhanh bằng `bit_count()`;
- việc đánh giá các tổ hợp quy tắc nhanh hơn nhiều so với thao tác trên danh sách thường.

Đây là một tối ưu quan trọng của project.

---

## 4. Luồng hoạt động của project

### 4.1. File `passwords.txt`

Đây là nguồn dữ liệu đầu vào.

Hàm `load_passwords()` sẽ:

- mở file;
- đọc từng dòng;
- loại bỏ dòng rỗng;
- trả về danh sách mật khẩu.

Nếu file không tồn tại, chương trình báo lỗi và trả về danh sách rỗng.

### 4.2. Khởi tạo các quy tắc

Trong `coverage_problem.py`, mỗi quy tắc được cài đặt bằng một hàm kiểm tra:

- `first_char_upper`
- `all_upper`
- `all_lower`
- `ends_with_digit`
- `ends_with_special`
- `starts_with_special`
- `standard_password`

Mỗi hàm nhận một chuỗi password và trả về `True` hoặc `False`.

Sau đó chúng được đóng gói trong `RULES` gồm:

- `label`: tên hiển thị;
- `predicate`: hàm kiểm tra điều kiện.

### 4.3. Biến đổi thành bài toán tối ưu

Quá trình giải bài toán gồm các bước:

1. Đọc toàn bộ mật khẩu trong `passwords.txt`.
2. Tạo bitmask cho từng quy tắc.
3. Chọn thuật toán giải.
4. Tính tổ hợp quy tắc tốt nhất theo tiêu chí tối đa hóa số password được phủ.
5. In kết quả ra màn hình.
6. Ghi kết quả cuối cùng vào file output tương ứng.

### 4.4. Kết quả đầu ra

Hàm `save_answer()` chỉ ghi:

- danh sách quy tắc đã chọn;
- danh sách password được phủ.

Không ghi:

- thông số benchmark;
- toàn bộ `passwords.txt`;
- các password không thuộc vùng phủ của tập quy tắc đã chọn.

Nếu không có kết quả, chương trình ghi `null`.

---

## 5. Giải thích chi tiết từng thuật toán trong `algorithms/`

Project có 4 cách giải:

1. Brute Force
2. Greedy
3. Math Model
4. Dynamic Programming

Tất cả đều dùng chung tầng xử lý trong `coverage_problem.py`, nhưng khác nhau ở chiến lược tìm nghiệm.

---

## 5.1. Brute Force

### Ý tưởng

Brute Force là cách trực tiếp và “thẳng tay” nhất:

- liệt kê tất cả các tổ hợp gồm đúng `k` quy tắc;
- với mỗi tổ hợp, tính hợp của các tập con;
- chọn tổ hợp có số mật khẩu được phủ lớn nhất.

### Cách hoạt động trong project

Trong `solve_bruteforce()`:

1. `build_rule_masks(passwords)` tạo bitmask cho từng quy tắc.
2. Duyệt tất cả các tổ hợp `k` quy tắc bằng `itertools.combinations`.
3. Với mỗi tổ hợp:
   - khởi tạo `mask = 0`;
   - dùng phép `OR` để gộp các bitmask của từng quy tắc;
   - tính số bit bằng `mask.bit_count()`.
4. Ghi nhận tổ hợp nào có số bit lớn nhất.

### Vì sao đúng?

Vì thuật toán xét toàn bộ không gian nghiệm khả dĩ, nên nó không bỏ sót lời giải tối ưu nào.

### Độ phức tạp

Nếu có `m` quy tắc ứng viên và chọn `k` quy tắc, số tổ hợp cần duyệt là:

```text
C(m, k)
```

Đây là tốc độ tăng rất nhanh khi `m` lớn.

### Đánh giá

- Ưu điểm: cho nghiệm tối ưu tuyệt đối.
- Nhược điểm: chậm khi số quy tắc tăng.

Brute Force là lời giải chuẩn để làm mốc so sánh cho các thuật toán khác.

---

## 5.2. Greedy

### Ý tưởng

Greedy không cố gắng duyệt hết mọi khả năng. Thay vào đó, nó chọn từng quy tắc theo tiêu chí:

- ở bước hiện tại, chọn quy tắc làm tăng số mật khẩu được phủ thêm nhiều nhất.

Đây là chiến lược “tham lam”:

- chọn cái tốt nhất ngay trước mắt;
- không nhìn sâu toàn bộ tương lai.

### Cách hoạt động trong project

Trong `solve_greedy()`:

1. Tạo bitmask cho tất cả quy tắc.
2. Khởi tạo:
   - `selected_rule_ids = []`
   - `covered_mask = 0`
   - `remaining_rule_ids` là các quy tắc chưa chọn.
3. Lặp cho đến khi chọn đủ `k` quy tắc:
   - thử từng quy tắc còn lại;
   - tính `candidate_mask = covered_mask | rule_masks[rule_id]`;
   - đo “lợi ích tăng thêm” bằng số bit mới được thêm vào;
   - chọn quy tắc có gain lớn nhất.
4. Cập nhật vùng phủ hiện tại và tiếp tục vòng lặp.

### Tính chất

Greedy có thể rất nhanh và thường cho kết quả khá tốt, nhưng:

- không đảm bảo tối ưu toàn cục;
- có thể bị “mắc bẫy” bởi lựa chọn tốt cục bộ nhưng không tốt về tổng thể.

### Độ phức tạp

Thông thường là thấp hơn nhiều so với brute force, vì không cần duyệt toàn bộ tổ hợp.

### Đánh giá

- Ưu điểm: nhanh, dễ hiểu, dễ mở rộng.
- Nhược điểm: chỉ là xấp xỉ, không bảo đảm lời giải tối ưu.

Greedy rất phù hợp khi cần chạy nhanh và chấp nhận đánh đổi một phần độ chính xác.

---

## 5.3. Math Model

### Ý tưởng

Thuật toán này bám sát mô hình toán học của Maximum Coverage:

- biểu diễn mỗi tập bằng bitmask;
- duyệt toàn bộ tập con có đúng `k` quy tắc;
- tính vùng phủ của từng tập con;
- chọn tập con cho kết quả lớn nhất.

Về mặt bản chất, đây vẫn là một cách giải exact, nhưng cách trình bày gần với mô hình toán học hơn:

```text
maximize |union of selected sets|
subject to selecting exactly k sets
```

### Cách hoạt động trong project

Trong `solve_math_model()`:

1. Tính bitmask cho mọi quy tắc.
2. Duyệt từ `0` đến `2^m - 1`, với `m` là số quy tắc ứng viên.
3. Chỉ giữ những `subset_mask` có đúng `k` bit được bật.
4. Với mỗi `subset_mask`:
   - duyệt từng bit;
   - nếu bit nào bật thì OR bitmask của quy tắc tương ứng vào `coverage_mask`.
5. Đếm số bit của `coverage_mask`.
6. Cập nhật nghiệm tốt nhất.

### Tại sao gọi là “Math Model”?

Vì cách này thể hiện rõ ý tưởng mô hình hóa:

- biến quyết định: chọn hay không chọn một quy tắc;
- hàm mục tiêu: tối đa hóa số password được phủ;
- ràng buộc: chỉ chọn đúng `k` quy tắc.

Nó rất phù hợp khi viết báo cáo lý thuyết hoặc minh họa bài toán tối ưu tổ hợp.

### Đánh giá

- Ưu điểm: lời giải chính xác, mô hình hóa rõ ràng.
- Nhược điểm: vẫn có độ phức tạp mũ theo số quy tắc.

---

## 5.4. Dynamic Programming

### Ý tưởng

Dynamic Programming trong project thực chất là **tìm kiếm đệ quy có ghi nhớ**:

- lưu lại kết quả của các trạng thái đã tính;
- tránh tính lặp lại cùng một trạng thái nhiều lần.

Đây là một cách tối ưu hơn brute force trong những trường hợp có nhiều nhánh trùng nhau.

### Cách hoạt động trong project

Trong `solve_dp()`:

1. Tạo bitmask cho các quy tắc.
2. Định nghĩa hàm `best_solution(selected_mask, remaining)` với `lru_cache`.
3. Ý nghĩa trạng thái:
   - `selected_mask`: các quy tắc đã chọn;
   - `remaining`: số quy tắc còn phải chọn.
4. Nếu `remaining == 0`, trả về vùng phủ rỗng.
5. Nếu chưa kết thúc:
   - thử thêm từng quy tắc chưa được chọn;
   - gọi đệ quy cho trạng thái mới;
   - kết hợp kết quả hiện tại với kết quả con.
6. Nhờ `lru_cache`, nếu cùng một trạng thái xuất hiện lại, kết quả được lấy từ cache thay vì tính lại.

### Ý nghĩa của memoization

Memoization làm giảm số lần tính trùng:

- nếu một trạng thái đã xuất hiện trước đó;
- kết quả của nó được lưu;
- lần sau chỉ cần đọc lại.

### Điểm cần hiểu đúng

Thuật toán này vẫn là exact search, không phải DP theo nghĩa cổ điển của các bài toán như dãy con, ba lô, hay quy hoạch động trên trục số.

Nó là:

- duyệt trạng thái tổ hợp;
- kết hợp với cache để tránh lặp.

### Đánh giá

- Ưu điểm: chính xác, có thể tiết kiệm đáng kể so với duyệt thô trong một số trường hợp.
- Nhược điểm: vẫn tăng nhanh theo số quy tắc, vì không gian trạng thái tổ hợp vẫn lớn.

---

## 6. Giải thích các hàm quan trọng trong `coverage_problem.py`

### 6.1. Các hàm kiểm tra quy tắc

Mỗi hàm như `first_char_upper()` hay `ends_with_digit()` là một **predicate**.

Chức năng của chúng là:

- nhận một password;
- trả về `True/False`;
- từ đó xác định password đó có thuộc tập con của quy tắc hay không.

### 6.2. `build_rule_masks(passwords)`

Hàm này chuyển mỗi quy tắc thành một bitmask tương ứng.

Đây là bước then chốt vì:

- thay vì giữ tập con dưới dạng list phức tạp;
- ta chuyển sang dạng bit;
- từ đó thao tác hợp, so sánh, đếm trở nên rất nhanh.

### 6.3. `mask_to_passwords(passwords, mask)`

Hàm này chuyển ngược bitmask về danh sách password thực tế.

Điều này cần thiết để:

- in ra kết quả cho người dùng;
- ghi file output ở dạng dễ đọc.

### 6.4. `result_payload(...)`

Hàm này chuẩn hóa đầu ra giữa các solver.

Nhờ vậy:

- giao diện in kết quả thống nhất;
- việc lưu file cũng đồng nhất;
- các thuật toán khác nhau vẫn trả về cùng một cấu trúc dữ liệu.

### 6.5. `run_solver(...)`

Đây là lớp bao chung cho cả 4 thuật toán.

Nó có nhiệm vụ:

- đo thời gian chạy;
- đo bộ nhớ;
- gọi solver;
- lưu kết quả;
- in thống kê ra màn hình.

Tức là phần “giao diện benchmark” được tách riêng khỏi logic tối ưu.

---

## 7. Vai trò của từng file trong project

### `coverage_problem.py`

Chứa:

- định nghĩa quy tắc;
- tải dữ liệu;
- chuyển đổi bitmask;
- các solver cốt lõi;
- hàm chạy và ghi kết quả.

Đây là trung tâm của toàn bộ project.

### `rules.py`

Chứa lớp giao diện dòng lệnh để:

- hiển thị danh sách rule;
- nhận lựa chọn `k` từ người dùng;
- gọi solver tương ứng.

### `pwd_checking.py`

Là điểm vào chính của chương trình:

- hiển thị menu chọn thuật toán;
- gọi đúng module tương ứng;
- điều phối luồng xử lý chính.

### `algorithms/Brute_Force.py`

Gọi solver brute force và ghi file:

```text
output_brute_max_coverage.txt
```

### `algorithms/Greedy.py`

Gọi solver greedy và ghi file:

```text
output_greedy_max_coverage.txt
```

### `algorithms/Math_Model.py`

Gọi solver math model và ghi file:

```text
output_math_model_max_coverage.txt
```

### `algorithms/Dynamic_Programming.py`

Gọi solver dynamic programming và ghi file:

```text
output_dp_max_coverage.txt
```

---

## 8. Ý nghĩa học thuật của dự án

Dự án này không chỉ là một chương trình lọc password. Về mặt học thuật, nó minh họa rất rõ các khái niệm sau:

- cách mô hình hóa một bài toán thực tế thành bài toán tổ hợp;
- cách biểu diễn tập hợp bằng bitmask;
- sự khác nhau giữa giải chính xác và giải xấp xỉ;
- vai trò của NP-hard trong thiết kế thuật toán;
- cách tối ưu hiệu năng bằng memoization và thao tác bit.

Đây là một ví dụ tốt để thấy rằng:

- cùng một bài toán có thể giải bằng nhiều chiến lược khác nhau;
- mỗi chiến lược có ưu, nhược riêng;
- lựa chọn thuật toán phụ thuộc vào mục tiêu: nhanh hay chính xác, dễ hiểu hay tối ưu, mô hình toán hay thực thi thực tế.

---

## 9. Kết luận

Project `password_checking_maximum_coverage` đã chuyển bài toán kiểm tra mật khẩu thành một bài toán **Maximum Coverage** điển hình:

- tập cha là toàn bộ mật khẩu trong `passwords.txt`;
- mỗi quy tắc tạo ra một tập con;
- người dùng chọn `k` quy tắc;
- chương trình tìm cách phủ được nhiều mật khẩu nhất.

Bốn thuật toán trong project thể hiện bốn góc nhìn khác nhau:

- **Brute Force**: đúng tuyệt đối nhưng chậm;
- **Greedy**: nhanh, xấp xỉ;
- **Math Model**: bám sát mô hình toán học, exact;
- **Dynamic Programming**: exact với ghi nhớ trạng thái.

Nhờ đó, project không chỉ giải một bài toán cụ thể mà còn là một ví dụ trực quan về cách lý thuyết độ phức tạp, tối ưu tổ hợp và biểu diễn tập hợp được áp dụng trong thực tế.
