# REPORT — Kiểm thử tự động Web UI

**Môn học**: Kiểm thử và Đảm bảo chất lượng phần mềm (STQA)  
**Hệ thống kiểm thử**: Quản lý mượn sách Thư viện ABC — https://stqa.rbc.vn  
**Công cụ**: Python 3 + Playwright + pytest  
**Nhóm**: Nhóm 22 — Lớp 252ICT2012.L1 — HK2 2025-2026

| # | MSSV      | Họ và tên       | Vai trò     |
|---|-----------|-----------------|-------------|
| 1 | 23BA14158 | Nguyễn Chí Kiên | Nhóm trưởng |
| 2 | 23BA14148 | Phạm Vũ Khánh   | Thành viên  |
| 3 | 23BA14059 | Nguyễn Minh Đức | Thành viên  |
| 4 | 2410761   | Nguyễn Tú Oanh  | Thành viên  |
| 5 | 23BA14107 | Đào Trung Hiếu  | Thành viên  |

---

## 1. Tổng quan kết quả

| Hạng mục         | Số lượng |
|------------------|----------|
| Tổng test case   | 38       |
| Passed           | 29       |
| Failed (xfail)   | 9        |
| Bugs phát hiện   | 7        |

**Tỉ lệ pass:** 29/38 (76%) — 9 test FAIL đều là xfail do bug đã được ghi nhận có chủ đích.

---

## 2. Test case theo từng file

### 2.1 Đăng nhập — `test_login.py` (REQ-01)

| TC     | Hàm kiểm thử                                    | Mô tả kịch bản                                                                 | Kết quả |
|--------|-------------------------------------------------|--------------------------------------------------------------------------------|---------|
| TC-01  | `test_TC01_librarian_login_success`             | Đăng nhập tài khoản thủ thư hợp lệ. Kiểm tra hiển thị tên hoặc nút Đăng xuất. | PASSED  |
| TC-02  | `test_TC02_member_login_success`                | Đăng nhập tài khoản thành viên hợp lệ. Kiểm tra điều hướng thành công.         | PASSED  |
| TC-03  | `test_TC03_nonexistent_email_rejected`          | Đăng nhập email không tồn tại. Kiểm tra hệ thống từ chối và hiển thị lỗi.      | PASSED  |
| TC-04  | `test_TC04_wrong_password_rejected`             | Đăng nhập sai mật khẩu. Kiểm tra hệ thống hiển thị thông báo lỗi.              | PASSED  |
| TC-05  | `test_TC05_empty_email_and_password`            | Bỏ trống cả email và mật khẩu. Kiểm tra hệ thống không cho đăng nhập.          | PASSED  |
| TC-06  | `test_TC06_suspended_member_can_login`          | Tài khoản bị tạm ngưng vẫn đăng nhập được (chỉ bị chặn khi mượn sách).         | PASSED  |
| TC-07  | `test_TC07_expired_member_can_login`            | Tài khoản hết hạn vẫn đăng nhập được (chỉ bị chặn khi mượn sách).              | PASSED  |
| TC-31  | `test_TC31_only_email_empty_rejected`           | Nhập mật khẩu nhưng để trống email. Kiểm tra hệ thống từ chối.                 | PASSED  |

**Ghi chú kỹ thuật:** Tất cả 8 TC đều PASS. Sử dụng helper `login()` từ conftest và kiểm tra Semantics Tree qua `wait_for_flutter()`. Oracle kiểm tra tên hiển thị, chữ "Đăng xuất", hoặc vai trò người dùng.

---

### 2.2 Danh sách & Trạng thái sách — `test_general.py` (REQ-02, REQ-06)

| TC     | Hàm kiểm thử                                  | Mô tả kịch bản                                                                                         | Kết quả        |
|--------|-----------------------------------------------|--------------------------------------------------------------------------------------------------------|----------------|
| TC-08  | `test_TC08_full_book_list_with_all_fields`    | Kiểm tra danh sách hiển thị đủ 20 cuốn sách với tất cả các trường thông tin.                           | PASSED         |
| TC-09  | `test_TC09_book_status_updates_after_borrow`  | Mượn một cuốn sách và kiểm tra trạng thái cập nhật thành "Đang mượn".                                  | PASSED         |
| TC-23  | `test_TC23_check_overdue_boundary_and_idempotency` | Chạy kiểm tra quá hạn lần 2 liên tiếp. Kỳ vọng kết quả ổn định, không báo "0 phiếu" khi có dữ liệu. | **FAILED** (xfail — BUG-04) |
| TC-24  | `test_TC24_member_views_own_overdue_record`   | Thành viên MEM002 xem phiếu quá hạn và thấy đúng bản ghi BR001 của mình.                               | PASSED         |
| TC-35  | `test_TC35_librarian_sees_all_overdue_records`| Thủ thư chạy kiểm tra quá hạn và xem được tất cả phiếu quá hạn của mọi thành viên.                     | PASSED         |

**Ghi chú kỹ thuật:** TC-23 bị FAIL do BUG-04 — lần chạy thứ 2 của "Kiểm tra quá hạn" trả về "0 phiếu" dù dữ liệu vẫn tồn tại. Đây là lỗi idempotency trong logic backend. TC được đánh dấu `xfail` vì bug đã ghi nhận.

---

### 2.3 Tìm kiếm & Lọc sách — `test_search.py` (REQ-03)

| TC     | Hàm kiểm thử                            | Mô tả kịch bản                                                                                              | Kết quả        |
|--------|-----------------------------------------|-------------------------------------------------------------------------------------------------------------|----------------|
| TC-10  | `test_TC10_search_by_title_flutter`     | Tìm kiếm từ khóa "Flutter". Kiểm tra có ít nhất 1 card sách liên quan xuất hiện.                            | PASSED         |
| TC-11  | `test_TC11_search_by_author_nguyen`     | Tìm kiếm tác giả "Nguyễn Minh Đức". Kiểm tra kết quả chứa tên tác giả.                                     | PASSED         |
| TC-12  | `test_TC12_case_insensitive_search`     | Tìm "flutter" (chữ thường) phải trả về kết quả giống "Flutter". Kiểm tra hệ thống không phân biệt hoa/thường. | PASSED         |
| TC-13  | `test_TC13_search_no_match_shows_message` | Tìm chuỗi không tồn tại "xyz_khong_ton_tai_12345". Kiểm tra không có card sách nào hiển thị.              | PASSED         |
| TC-32  | `test_TC32_clear_search_restores_full_list` | Xóa từ khóa tìm kiếm. Kiểm tra danh sách khôi phục đủ 20 cuốn sách.                                    | PASSED         |
| TC-14  | `test_TC14_genre_filter_case_insensitive` | Lọc thể loại "công nghệ" (chữ thường). Kỳ vọng kết quả giống "Công nghệ".                               | **FAILED** (xfail — BUG-02) |
| TC-37  | `test_TC37_search_and_filter_combo`     | Kết hợp tìm kiếm từ khóa và lọc thể loại. Kiểm tra bộ lọc được áp dụng đồng thời.                         | **FAILED** (xfail — BUG-06) |

**Ghi chú kỹ thuật:** Helper `_search()`, `_clear_search()`, `_filter_genre()` được dùng xuyên suốt để tái sử dụng logic. BUG-02 là lỗi case-sensitivity trong bộ lọc thể loại. BUG-06 là lỗi bộ lọc thể loại bị bỏ qua khi kết hợp với tìm kiếm từ khóa.

---

### 2.4 Mượn & Trả sách — `test_borrow_return.py` (REQ-04, REQ-05)

| TC     | Hàm kiểm thử                                | Mô tả kịch bản                                                                                        | Kết quả |
|--------|---------------------------------------------|-------------------------------------------------------------------------------------------------------|---------|
| TC-15  | `test_TC15_borrow_book_success`             | Mượn một cuốn sách có sẵn và xác nhận qua dialog. Kiểm tra trạng thái chuyển sang "Đang mượn".        | PASSED  |
| TC-16  | `test_TC16_already_borrowed_book_rejected`  | Sách đang được mượn không hiển thị nút "Mượn sách này". Kiểm tra hệ thống ngăn mượn lại.              | PASSED  |
| TC-33  | `test_TC33_borrow_at_bva_boundary_2nd_book` | Mượn cuốn thứ 2 (biên dưới giới hạn). Kiểm tra lần mượn thứ 2 thành công bình thường.                 | PASSED  |
| TC-21  | `test_TC21_return_book_success`             | Trả sách đang mượn. Kiểm tra trạng thái chuyển sang "Đã trả" trong lịch sử.                           | PASSED  |
| TC-22  | `test_TC22_return_unborrowed_book_rejected` | Sách chưa được mượn không có nút "Trả sách". Kiểm tra hệ thống không cho trả.                         | PASSED  |
| TC-38  | `test_TC38_return_overdue_shows_warning`    | Trả sách quá hạn. Kiểm tra hệ thống hiển thị cảnh báo quá hạn trong quá trình trả.                    | PASSED  |

**Ghi chú kỹ thuật:** Tất cả 6 TC đều PASS. Helper `_borrow_first_available()` tự động tìm sách có trạng thái "Có sẵn" và thực hiện mượn qua dialog xác nhận. TC-33 kiểm tra BVA (Boundary Value Analysis) tại biên dưới của giới hạn 3 quyển.

---

### 2.5 Kiểm soát truy cập mượn sách — `test_borrow_access_control.py` (REQ-04)

| TC     | Hàm kiểm thử                                          | Mô tả kịch bản                                                                                                         | Kết quả        |
|--------|-------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------|----------------|
| TC-17  | `test_TC17_suspended_member_borrow_rejected_wrong_message` | Tài khoản bị tạm ngưng cố mượn sách. Kỳ vọng thông báo "Tài khoản đã bị tạm ngưng".                         | **FAILED** (xfail — BUG-03) |
| TC-18  | `test_TC18_expired_member_borrow_rejected`            | Tài khoản hết hạn cố mượn sách. Kiểm tra thông báo "Thành viên đã hết hạn" xuất hiện đúng.                            | PASSED         |
| TC-19  | `test_TC19_borrow_limit_3_books_not_enforced`         | Thực hiện mượn 4 lần liên tiếp. Kỳ vọng lần thứ 4 bị từ chối (giới hạn 3 quyển/thành viên).                          | **FAILED** (xfail — BUG-01) |
| TC-20  | `test_TC20_lost_book_cannot_be_borrowed`              | Sách có trạng thái "Thất lạc" không hiển thị nút mượn. Kiểm tra sách thất lạc không thể mượn.                         | PASSED         |

**Ghi chú kỹ thuật:** BUG-03 — hệ thống xử lý nhầm trạng thái `suspended` và `expired`, tài khoản bị tạm ngưng nhận thông báo của tài khoản hết hạn. BUG-01 — lỗi off-by-one: hệ thống dùng `> maxBooksPerMember` thay vì `>= maxBooksPerMember`, cho phép mượn 4 quyển thay vì tối đa 3.

---

### 2.6 Quản lý thành viên — `test_member_management.py` (REQ-07)

| TC     | Hàm kiểm thử                                  | Mô tả kịch bản                                                                                                       | Kết quả        |
|--------|-----------------------------------------------|----------------------------------------------------------------------------------------------------------------------|----------------|
| TC-28  | `test_TC28_member_has_no_members_tab`         | Tài khoản thành viên không thấy tab "Thành viên". Kiểm tra phân quyền giao diện đúng.                                | PASSED         |
| TC-25  | `test_TC25_add_valid_member_fails`            | Thêm thành viên với email hợp lệ "tay.tran@email.com". Kỳ vọng thêm thành công.                                     | **FAILED** (xfail — BUG-05) |
| TC-26  | `test_TC26_invalid_email_no_dot_accepted`     | Nhập email không hợp lệ "tay.tran@emailcom" (thiếu dấu chấm sau @). Kỳ vọng hệ thống từ chối.                      | **FAILED** (xfail — BUG-05) |
| TC-27  | `test_TC27_duplicate_email_wrong_message`     | Thêm email đã tồn tại. Kỳ vọng thông báo "email đã tồn tại", nhưng hệ thống hiển thị "Invalid".                     | **FAILED** (xfail — BUG-05) |

**Ghi chú kỹ thuật:** BUG-05 ảnh hưởng toàn bộ tính năng thêm thành viên — validation email bị lỗi 3 chiều: từ chối email hợp lệ, chấp nhận email không hợp lệ, và hiển thị thông báo lỗi sai khi trùng email. Helper `_fill_member_form()` hỗ trợ nhiều label field candidate để linh hoạt với thay đổi UI.

---

### 2.7 Tra cứu phiếu mượn — `test_borrow_records.py` (REQ-08)

| TC     | Hàm kiểm thử                                        | Mô tả kịch bản                                                                                                             | Kết quả        |
|--------|-----------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------|----------------|
| TC-29  | `test_TC29_librarian_views_any_member_records`      | Thủ thư tra cứu phiếu mượn theo mã thành viên bất kỳ. Kiểm tra xem được toàn bộ bản ghi.                                  | PASSED         |
| TC-30  | `test_TC30_member_views_only_own_records`           | Thành viên MEM002 tra cứu phiếu của mình. Kiểm tra chỉ thấy bản ghi BR001 thuộc về mình.                                  | PASSED         |
| TC-36  | `test_TC36_returned_record_shows_correct_fields`    | Phiếu có trạng thái "Đã trả" hiển thị đầy đủ các trường: mã phiếu, tên sách, ngày mượn, ngày trả.                        | PASSED         |
| TC-39  | `test_TC39_member_cannot_access_other_member_records` | Thành viên MEM002 cố tra cứu phiếu của MEM006. Kỳ vọng bị từ chối hoặc không thấy dữ liệu.                            | **FAILED** (xfail — BUG-07 CRITICAL) |

**Ghi chú kỹ thuật:** BUG-07 là lỗi nghiêm trọng nhất — thành viên có thể tra cứu và thao tác phiếu mượn của thành viên khác, vi phạm kiểm soát truy cập (access control breach). Tab "Tra cứu phiếu mượn" sử dụng selector `TRA_CUU_TAB` và input tìm kiếm theo mã thành viên.

---

## 3. Bugs phát hiện trong hệ thống

| Bug ID  | Mức độ      | TC phát hiện | Mô tả                                                                                                      |
|---------|------------|-------------|------------------------------------------------------------------------------------------------------------|
| BUG-01  | Cao        | TC-19        | Giới hạn mượn sách dùng `> 3` thay vì `>= 3` — thành viên mượn được 4 quyển thay vì tối đa 3 (off-by-one). |
| BUG-02  | Trung bình | TC-14        | Bộ lọc thể loại phân biệt chữ hoa/thường — "công nghệ" ≠ "Công nghệ".                                     |
| BUG-03  | Trung bình | TC-17        | Tài khoản bị tạm ngưng (`suspended`) nhận thông báo lỗi của tài khoản hết hạn (`expired`).                |
| BUG-04  | Cao        | TC-23        | Chạy "Kiểm tra quá hạn" lần 2 trả về "0 phiếu" dù dữ liệu quá hạn vẫn tồn tại (idempotency lỗi).        |
| BUG-05  | Cao        | TC-25,26,27  | Validation email thêm thành viên sai hoàn toàn: từ chối email hợp lệ, chấp nhận email sai định dạng.      |
| BUG-06  | Trung bình | TC-37        | Bộ lọc thể loại bị bỏ qua khi kết hợp với tìm kiếm từ khóa.                                              |
| BUG-07  | **Nghiêm trọng** | TC-39  | Thành viên tra cứu và thao tác được phiếu mượn của thành viên khác — vi phạm kiểm soát truy cập.          |

---

## 4. Nhận xét kỹ thuật

**Xử lý Flutter Web (CanvasKit):** Toàn bộ test dùng đúng cơ chế Semantics Tree (`flt-semantics`) và Smart Wait (`wait_for_flutter()`). Module `web_detector.py` tự động nhận diện stack công nghệ và chọn chiến lược tương tác phù hợp (Flutter vs HTML).

**Kiến trúc conftest:** Helper `smart_fill()` và `smart_click()` tự động chọn chiến lược Flutter hoặc HTML tùy theo kết quả phát hiện — giúp test không bị phụ thuộc cứng vào một renderer cụ thể.

**Chất lượng Oracle:** Các TC kiểm tra danh sách (TC-08, TC-09, TC-30) dùng Strong Oracle — kiểm tra từng phần tử trong danh sách. TC-39 dùng oracle kiểm tra access control thực tế thay vì chỉ kiểm tra UI ẩn nút.

**Cấu trúc RIPR:** Mỗi test case áp dụng mô hình RIPR (Reachability → Infection → Propagation → Revealability) và được đánh dấu `xfail` có chủ đích khi test phát hiện bug thực sự trong hệ thống.

**Reset trạng thái:** Helper `reset_database()` trong conftest cho phép khôi phục trạng thái hệ thống qua tài khoản thủ thư, đảm bảo các test độc lập với nhau.
