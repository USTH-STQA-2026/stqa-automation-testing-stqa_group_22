[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/ZpUiBug-)
# STQA Library Automation — Starter Template

Bài tập thực hành **Kiểm thử Web UI tự động** cho môn **Kiểm thử và Đảm bảo chất lượng phần mềm (STQA)**.
(*A hands-on **Automated Web UI Testing** assignment for the **Software Testing & Quality Assurance (STQA)** course.*)

Sử dụng **Playwright + Python** để kiểm thử hệ thống Mượn sách Thư viện ABC tại [https://stqa.rbc.vn](https://stqa.rbc.vn).
(*Uses **Playwright + Python** to test the Library Book Borrowing System.*)

> **📚 Hệ thống hư cấu / Fictional System**: Thư viện ABC là hệ thống **hư cấu** được thiết kế cho mục đích học tập. Tên nhân vật, tổ chức và dữ liệu đều là giả lập. / *ABC Library is a **fictional** system designed for educational purposes. All names, organizations, and data are simulated.*

---

## 👥 Thông tin nhóm / Team Information

> **⚠️ Sinh viên: Điền thông tin nhóm vào bảng dưới đây trước khi nộp bài.**

|              | Thông tin                    |
| ------------ | ---------------------------- |
| **Tên nhóm** | `<!-- VD: Nhóm 22 -->` |
| **Lớp** | `<!-- 252ICT2012.L1 -->` |
| **Học kỳ** | `<!-- VD: HK2 2025-2026 -->` |

| # | MSSV | Họ và tên | Vai trò |
|---|------|-----------|---------|
| 1 | 23BA14158| Nguyễn Chí Kiên | Nhóm trưởng |
| 2 | 23BA14148| Phạm Vũ Khánh | Thành viên |
| 3 | 23BA14059| Nguyễn Minh Đức | Thành viên |
| 4 | 2410761| Nguyễn Tú Oanh | Thành viên |
| 5 | 23BA14107| Đào Trung Hiếu | Thành viên |
---

## 📖 Trước khi bắt đầu — Bối cảnh / Before You Start — Context

### Bài tập này nằm ở đâu trong quy trình?

```
SRS (Yêu cầu phần mềm) → Dev xây hệ thống → A1: Kiểm thử thủ công → A2: Kiểm thử tự động (BẠN Ở ĐÂY)
```

Ở bài **A1** (nếu đã làm), bạn đã kiểm thử thủ công: mở trình duyệt, nhấn nút, ghi kết quả. Bây giờ ở **A2**, bạn sẽ **tự động hóa** các thao tác đó bằng code.

### Những ai liên quan? (*Stakeholders*)

| Vai trò         | Ai?            | Liên quan thế nào?                                                                                          |
| --------------- | -------------- | ----------------------------------------------------------------------------------------------------------- |
| **Khách hàng**  | Thư viện ABC   | Đưa ra yêu cầu nghiệp vụ ([BRD](docs/BRD-yeu-cau-nghiep-vu.md)) → BA viết [SRS](docs/SRS-library-system.md) |
| **Dev Team**    | Nhóm lập trình | Xây hệ thống                                                                                                |
| **Tester / QC** | **Bạn**        | Viết automated test, phát hiện lỗi                                                                          |
| **QA Lead**     | Giảng viên     | Review kết quả test                                                                                         |

### Tester dựa vào đâu để kiểm thử?

| Nguồn                      | Trong bài này                                                    |
| -------------------------- | ---------------------------------------------------------------- |
| **SRS** (đặc tả yêu cầu)   | [docs/SRS-library-system.md](docs/SRS-library-system.md) — 8 REQ |
| **Test accounts**          | [docs/test-accounts.md](docs/test-accounts.md) — 6 tài khoản     |
| **A1 test cases** (nếu có) | Tham khảo TC thủ công để viết code tự động                       |

### Software Testing vs Quality Assurance

|                  | **Testing** (Bài này)                             | **QA**                                       |
| ---------------- | ------------------------------------------------- | -------------------------------------------- |
| **Bạn đang làm** | ✅ Viết automated test, chạy test, chụp screenshot | Bonus B4: Viết REPORT.md đánh giá chất lượng |
| **Mục đích**     | Tìm lỗi tự động, nhanh, lặp lại được              | Đánh giá quy trình, đề xuất cải tiến         |

---

> ⚠️ Website sử dụng **Flutter Web (CanvasKit renderer)** — toàn bộ giao diện render trên `<canvas>`, không có HTML DOM thông thường. Dự án đã cung cấp sẵn các helper function để tương tác qua **Accessibility Semantics Tree**.
>
> (*The website uses **Flutter Web (CanvasKit renderer)** — the entire UI is rendered on `<canvas>`, with no standard HTML DOM. This project provides helper functions to interact via the Accessibility Semantics Tree.*)

---

## 📁 Cấu trúc dự án / Project Structure

```
stqa-automation-testing-stqa_group_22/
├── conftest.py                    # Fixtures & helper functions (ĐÃ HOÀN CHỈNH)
├── web_detector.py                # Web technology detector module (ĐÃ HOÀN CHỈNH)
├── pytest.ini                     # pytest configuration
├── requirements.txt               # Dependencies
├── .env.example                   # Environment variable template
├── .gitignore
├── LICENSE
├── README.md
├── screenshots/                   # Ảnh chụp màn hình tự động (38 TC)
└── tests/
    ├── test_login.py              # REQ-01: TC-01 → TC-07, TC-31 (8 TCs)
    ├── test_general.py            # REQ-02 + REQ-06: TC-08, TC-09, TC-23, TC-24, TC-35 (5 TCs)
    ├── test_search.py             # REQ-03: TC-10 → TC-14, TC-32, TC-37 (7 TCs)
    ├── test_borrow_return.py      # REQ-04 + REQ-05: TC-15, TC-16, TC-21, TC-22, TC-33, TC-38 (6 TCs)
    ├── test_borrow_access_control.py  # REQ-04: TC-17 → TC-20 (4 TCs)
    ├── test_member_management.py  # REQ-07: TC-25 → TC-28 (4 TCs)
    └── test_borrow_records.py     # REQ-08: TC-29, TC-30, TC-36, TC-39 (4 TCs)
```

---

## 🚀 Cài đặt / Installation

### 1. Clone repo & tạo môi trường ảo

```bash
git clone <repo-url>
cd stqa-library-automation-starter
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
# venv\Scripts\activate    # Windows
```

### 2. Cài đặt dependencies

```bash
pip install -r requirements.txt
playwright install chromium
```

### 3. Cấu hình biến môi trường

Tạo file `.env` từ template:

```bash
cp .env.example .env
```

Sửa `.env` với thông tin đăng nhập của bạn:

```
BASE_URL=https://stqa.rbc.vn
TEST_EMAIL=your_email@example.com
TEST_PASSWORD=your_password
TEST_DISPLAY_NAME=Your Display Name
```

> ⚠️ **KHÔNG commit file `.env`** — file này đã được thêm vào `.gitignore`.

---

## ▶️ Chạy test / Running Tests

```bash
# Run all tests (Chạy tất cả test)
pytest

# Run a specific file (Chạy 1 file cụ thể)
pytest tests/test_login.py

# Run a specific test case (Chạy 1 test case cụ thể)
pytest tests/test_login.py::test_login_success

# Verbose output (Hiện output chi tiết)
pytest -v -s
```

Screenshot được lưu tự động vào thư mục `screenshots/`.

---

## 🤖 CI với GitHub Actions (cho sinh viên)

Repo đã có workflow CI tại `.github/workflows/pytest-ci.yml` và sẽ tự chạy khi:

- Có `push` lên repo
- Có `pull_request`

CI sẽ thực hiện:

1. Cài Python + dependencies
2. Cài Playwright Chromium
3. Chạy `pytest --junitxml=report.xml`
4. Upload artifacts gồm:
  - `report.xml`
  - `screenshots/**`

### Cách xem kết quả CI

1. Vào tab **Actions** trên GitHub
2. Mở run mới nhất của workflow **Pytest CI**
3. Kéo xuống phần **Artifacts** để tải `pytest-artifacts`
4. Mở `report.xml` để xem kết quả theo chuẩn JUnit XML

### Chính sách public repo

- Workflow này chỉ chạy các test đang có trong thư mục `tests/` của repo public.
- Không thêm hidden tests vào repo public.

---

## 📋 Danh sách Test Case / Test Case List

> **Kết quả thực thi:** 38/38 TC hoàn thành — 29 Pass ✅, 9 Fail (xfail = bug đã ghi nhận) 🐛

### REQ-01 — Đăng nhập (`test_login.py`)

| TC    | Mô tả                                                         | Kết quả thủ công | Automation      | Screenshot |
| ----- | ------------------------------------------------------------- | ---------------- | --------------- | ---------- |
| TC-01 | Đăng nhập thành công — Librarian                              | ✅ Pass           | ✅ Pass          | `TC-01_librarian_login.png` |
| TC-02 | Đăng nhập thành công — Member                                 | ✅ Pass           | ✅ Pass          | `TC-02_member_login.png` |
| TC-03 | Email không tồn tại → bị từ chối                              | ✅ Pass           | ✅ Pass          | `TC-03_nonexistent_email.png` |
| TC-04 | Sai mật khẩu → thông báo "Incorrect password"                 | ✅ Pass           | ✅ Pass          | `TC-04_wrong_password.png` |
| TC-05 | Bỏ trống cả email và mật khẩu → thông báo lỗi                | ✅ Pass           | ✅ Pass          | `TC-05_empty_fields.png` |
| TC-06 | Thành viên Suspended (MEM004) vẫn đăng nhập được              | ✅ Pass           | ✅ Pass          | `TC-06_suspended_login.png` |
| TC-07 | Thành viên Expired (MEM005) vẫn đăng nhập được                | ✅ Pass           | ✅ Pass          | `TC-07_expired_login.png` |
| TC-31 | Chỉ bỏ trống email (có mật khẩu) → bị từ chối                | ✅ Pass           | ✅ Pass          | `TC-31_only_email_empty.png` |

### REQ-02 — Xem danh sách sách (`test_general.py`)

| TC    | Mô tả                                                         | Kết quả thủ công | Automation      | Screenshot |
| ----- | ------------------------------------------------------------- | ---------------- | --------------- | ---------- |
| TC-08 | Hiển thị đầy đủ 20 sách với tất cả trường thông tin          | ✅ Pass           | ✅ Pass          | `TC-08_book_list.png` |
| TC-09 | Trạng thái sách cập nhật ngay sau khi mượn                    | ✅ Pass           | ✅ Pass          | `TC-09_status_update.png` |

### REQ-03 — Tìm kiếm & Lọc sách (`test_search.py`)

| TC    | Mô tả                                                         | Kết quả thủ công | Automation      | Screenshot |
| ----- | ------------------------------------------------------------- | ---------------- | --------------- | ---------- |
| TC-10 | Tìm theo tên sách "Flutter" → trả đúng kết quả               | ✅ Pass           | ✅ Pass          | `TC-10_search_flutter.png` |
| TC-11 | Tìm theo tên tác giả "Nguyễn"                                 | ✅ Pass           | ✅ Pass          | `TC-11_search_nguyen.png` |
| TC-12 | Tìm kiếm không phân biệt hoa thường (flutter = FLUTTER)       | ✅ Pass           | ✅ Pass          | `TC-12_search_lowercase.png` |
| TC-13 | Tìm không có kết quả → thông báo "No books found"             | ✅ Pass           | ✅ Pass          | `TC-13_no_result.png` |
| TC-32 | Xóa từ khóa tìm kiếm → danh sách đầy đủ được khôi phục       | ✅ Pass           | ✅ Pass          | `TC-32_clear_search.png` |
| TC-14 | Lọc thể loại không phân biệt hoa thường                       | ❌ **Fail**       | 🐛 xfail BUG-02 | `TC-14_filter_correct_case.png`, `TC-14_filter_lowercase.png` |
| TC-37 | Kết hợp tìm kiếm + lọc thể loại → AND logic                  | ❌ **Fail**       | 🐛 xfail BUG-06 | `TC-37_search_filter_combo.png` |

### REQ-04 — Mượn sách (`test_borrow_return.py`, `test_borrow_access_control.py`)

| TC    | Mô tả                                                         | Kết quả thủ công | Automation      | Screenshot |
| ----- | ------------------------------------------------------------- | ---------------- | --------------- | ---------- |
| TC-15 | Mượn sách thành công (happy path) — MEM006                   | ✅ Pass           | ✅ Pass          | `TC-15_borrow_success.png` |
| TC-16 | Sách đã có người mượn → bị từ chối                            | ✅ Pass           | ✅ Pass          | `TC-16_reject_borrowed.png` |
| TC-33 | Mượn tại BVA boundary (lần mượn thứ 2) → thành công          | ✅ Pass           | ✅ Pass          | `TC-33_bva_boundary.png` |
| TC-17 | Thành viên Suspended → bị từ chối nhưng hiện thông báo "hết hạn" sai | ❌ **Fail** | 🐛 xfail BUG-03 | `TC-17_suspended_borrow.png` |
| TC-20 | Sách bị mất (Lost) → không thể mượn                           | ✅ Pass           | ✅ Pass          | `TC-20_lost_book.png` |
| TC-18 | Thành viên Expired → bị từ chối với thông báo "hết hạn" (đúng) | ✅ Pass         | ✅ Pass          | `TC-18_expired_borrow.png` |
| TC-19 | Vượt giới hạn 3 sách → vẫn cho mượn sách thứ 4               | ❌ **Fail**       | 🐛 xfail BUG-01 | `TC-19_borrow_limit.png` |

### REQ-05 — Trả sách (`test_borrow_return.py`)

| TC    | Mô tả                                                         | Kết quả thủ công | Automation      | Screenshot |
| ----- | ------------------------------------------------------------- | ---------------- | --------------- | ---------- |
| TC-21 | Trả sách thành công — Librarian trả BR003                     | ✅ Pass           | ✅ Pass          | `TC-21_return_success.png` |
| TC-22 | Trả sách chưa mượn → bị từ chối                               | ✅ Pass           | ✅ Pass          | `TC-22_no_return_btn.png` |
| TC-38 | Trả sách quá hạn → hiển thị cảnh báo overdue                 | ✅ Pass           | ✅ Pass          | `TC-38_return_overdue.png` |

### REQ-06 — Xử lý quá hạn (`test_general.py`)

| TC    | Mô tả                                                         | Kết quả thủ công | Automation      | Screenshot |
| ----- | ------------------------------------------------------------- | ---------------- | --------------- | ---------- |
| TC-24 | Thành viên xem phiếu mượn quá hạn của chính mình              | ✅ Pass           | ✅ Pass          | `TC-24_member_overdue.png` |
| TC-35 | Librarian xem tất cả phiếu quá hạn của mọi thành viên         | ✅ Pass           | ✅ Pass          | `TC-35_all_overdue.png` |
| TC-23 | Check Overdue lần 2 báo "0 phiếu" sai — bản ghi vẫn tồn tại  | ❌ **Fail**       | 🐛 xfail BUG-04 | `TC-23_check_overdue.png` |

### REQ-07 — Quản lý thành viên (`test_member_management.py`)

| TC    | Mô tả                                                         | Kết quả thủ công | Automation      | Screenshot |
| ----- | ------------------------------------------------------------- | ---------------- | --------------- | ---------- |
| TC-28 | Thành viên không có tab Members / nút Thêm thành viên         | ✅ Pass           | ✅ Pass          | `TC-28_member_no_tab.png` |
| TC-25 | Thêm thành viên với email hợp lệ → bị từ chối sai             | ❌ **Fail**       | 🐛 xfail BUG-05 | `TC-25_add_member_valid.png` |
| TC-26 | Email thiếu dấu chấm → được chấp nhận (sai)                   | ❌ **Fail**       | 🐛 xfail BUG-05 | `TC-26_invalid_email_no_dot.png` |
| TC-27 | Email trùng → thông báo "Invalid email" thay vì "duplicate"   | ❌ **Fail**       | 🐛 xfail BUG-05 | `TC-27_duplicate_email.png` |

### REQ-08 — Tra cứu phiếu mượn (`test_borrow_records.py`)

| TC    | Mô tả                                                         | Kết quả thủ công | Automation      | Screenshot |
| ----- | ------------------------------------------------------------- | ---------------- | --------------- | ---------- |
| TC-29 | Librarian xem phiếu mượn của bất kỳ thành viên nào            | ✅ Pass           | ✅ Pass          | `TC-29_librarian_records.png` |
| TC-30 | Thành viên chỉ xem được phiếu mượn của chính mình             | ✅ Pass           | ✅ Pass          | `TC-30_member_own_records.png` |
| TC-36 | Phiếu đã trả hiển thị đúng trạng thái và đầy đủ trường        | ✅ Pass           | ✅ Pass          | `TC-36_returned_record.png` |
| TC-39 | Thành viên có thể xem và trả sách thay thành viên khác (lỗi!) | ❌ **Fail**       | 🐛 xfail BUG-07 | `TC-39_cross_member_access.png` |

---

### 🐛 Tổng hợp Bug / Bug Summary

| Bug    | Severity    | TC liên quan      | Mô tả ngắn |
| ------ | ----------- | ----------------- | ---------- |
| BUG-01 | High        | TC-19             | Cho mượn sách thứ 4 — vi phạm giới hạn 3 sách |
| BUG-02 | Medium      | TC-14             | Bộ lọc thể loại phân biệt hoa thường |
| BUG-03 | Medium      | TC-17             | Thành viên Suspended nhận thông báo "hết hạn" sai thay vì thông báo đình chỉ |
| BUG-04 | High        | TC-23             | Check Overdue: lỗi boundary ngày hôm nay + lần 2 báo 0 |
| BUG-05 | High        | TC-25, TC-26, TC-27 | Validation email Add Member bị lỗi 3 chiều |
| BUG-06 | Medium      | TC-37             | Bộ lọc thể loại bị bỏ qua khi kết hợp với tìm kiếm |
| BUG-07 | **Critical** | TC-39            | Thành viên xem và trả sách của thành viên khác — vi phạm kiểm soát truy cập |

---

## 🔧 Các hàm hỗ trợ có sẵn / Available Helper Functions

Các hàm đã được cung cấp trong `conftest.py` — **KHÔNG cần tự viết lại**.
(*These functions are provided in `conftest.py` — you do NOT need to rewrite them.*)

### Flutter Web helpers

| Hàm                                 | Mô tả                                                                                     |
| ----------------------------------- | ----------------------------------------------------------------------------------------- |
| `enable_flutter_semantics(page)`    | Bật Semantics Tree — bắt buộc trước khi tương tác (*Enable Accessibility Semantics Tree*) |
| `flutter_fill(page, label, value)`  | Nhập text vào input field (*Fill text into an input field using `aria-label`*)            |
| `flutter_click_button(page, text)`  | Click button theo text hiển thị (*Click a button by its displayed text*)                  |
| `wait_for_flutter(page, text, ...)` | Smart Wait — chờ Semantics Tree cập nhật (*Wait for Flutter Semantics Tree update*)       |

### Universal helpers

| Hàm                                    | Mô tả                                                                       |
| -------------------------------------- | --------------------------------------------------------------------------- |
| `smart_fill(page, label, value, tech)` | Tự chọn cách nhập phù hợp (*Auto-select fill strategy*)                     |
| `smart_click(page, text, tech)`        | Tự chọn cách click phù hợp (*Auto-select click strategy*)                   |
| `login(page, test_config)`             | Đăng nhập với credentials từ `.env` (*Log in with credentials from `.env`*) |

### Fixtures

| Fixture       | Mô tả                                                                                |
| ------------- | ------------------------------------------------------------------------------------ |
| `page`        | Context mới cho mỗi test (*Playwright Page object — fresh browser context per test*) |
| `test_config` | Dict chứa `base_url`, `email`, `password`, `display_name`, `screenshot_dir`          |
| `web_tech`    | Thông tin công nghệ web (*WebTech object — detected web technology info*)            |

---

## 💡 Cách tương tác với Flutter Web / How to Interact with Flutter Web

Flutter Web (CanvasKit) render mọi thứ lên `<canvas>` — **không có HTML DOM thông thường**. Để test, ta cần:
(*Flutter Web (CanvasKit) renders everything onto `<canvas>` — there is no standard HTML DOM. To test, we need to:*)

1. **Bật Semantics Tree**: Gọi `enable_flutter_semantics(page)` → Flutter tạo các elements ẩn `<flt-semantics>` phủ lên canvas
2. **Tương tác qua ARIA attributes**:
   - Input fields: `input[aria-label="Email"]`
   - Buttons: `flt-semantics[role="button"]:has-text("Đăng nhập")`
   - Tabs: `flt-semantics[role="tab"][aria-label="Mượn / Trả"]`
   - Groups (book cards / card sách): `flt-semantics[role="group"][aria-label*="Mã: BOOK"]`

### Ví dụ pattern cơ bản / Basic Pattern Example

```python
from conftest import login, flutter_fill, wait_for_flutter

def test_example(page, test_config):
    # 1. Đăng nhập
    login(page, test_config)

    # 2. Tìm element và tương tác
    flutter_fill(page, "Tìm kiếm theo tên sách hoặc tác giả...", "Flutter")

    # 3. Smart Wait: chờ kết quả xuất hiện (thay vì time.sleep)
    wait_for_flutter(page, text="Flutter")

    # 4. Kiểm tra kết quả qua semantics
    result = page.locator('flt-semantics[aria-label*="Flutter"]')
    assert result.count() > 0, "Không tìm thấy kết quả"

    # 5. Hoặc lấy toàn bộ text từ semantics
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "Flutter" in sem_text
```

### Lưu ý quan trọng / Important Notes

- Luôn gọi `enable_flutter_semantics(page)` sau khi navigate hoặc sau thao tác thay đổi DOM
- Dùng **Smart Wait** thay vì `time.sleep()`:
  - `wait_for_flutter(page, text="...")` — chờ text xuất hiện trong Semantics Tree
  - `page.locator("...").wait_for()` — chờ element cụ thể
  - Xem comment trong `conftest.py` để biết chi tiết các cách chờ
- Sau khi fill input, Flutter có thể tạo input ẩn trong `<flt-text-editing-host>` — helper `flutter_fill()` đã xử lý điều này

---

## 📚 Tài liệu tham khảo / References

### Tài liệu dự án

| Bạn muốn...                  | Đi đến                                                         |
| ---------------------------- | -------------------------------------------------------------- |
| Xem đề bài + rubric          | [docs/ASSIGNMENT.md](docs/ASSIGNMENT.md)                       |
| Đọc yêu cầu hệ thống (SRS)   | [docs/SRS-library-system.md](docs/SRS-library-system.md)       |
| Xem yêu cầu nghiệp vụ (BRD)  | [docs/BRD-yeu-cau-nghiep-vu.md](docs/BRD-yeu-cau-nghiep-vu.md) |
| Xem tài khoản test           | [docs/test-accounts.md](docs/test-accounts.md)                 |
| **Liên kết textbook ↔ repo** | [docs/textbook-concepts.md](docs/textbook-concepts.md)         |
| **Bài tập nhóm thảo luận**   | [docs/group-exercises.md](docs/group-exercises.md)             |

### Liên kết bên ngoài

- [Playwright Python Docs](https://playwright.dev/python/)
- [Playwright Locators](https://playwright.dev/python/docs/locators)
- [Flutter Web Accessibility](https://docs.flutter.dev/ui/accessibility)
- [pytest Documentation](https://docs.pytest.org/)
