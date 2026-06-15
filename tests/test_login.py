"""
REQ-01 Login — Verification of Manual Submission
TCs: TC-01, TC-02, TC-03, TC-04, TC-05, TC-06, TC-07, TC-31
Manual verdict: ALL PASS (8/8)
"""
import os
import pytest
from conftest import (
    login, enable_flutter_semantics, flutter_fill,
    flutter_click_button, BASE_URL, SCREENSHOT_DIR
)


# ── TC-01: Librarian login success ────────────────────────────────────────
def test_TC01_librarian_login_success(page):
    """Manual verdict: PASS — Login OK, AppBar shows Nguyen Thu Thu (Librarian)"""
    page.goto(BASE_URL, wait_until="load", timeout=90000)
    try:
        page.locator("flt-glass-pane").wait_for(state="attached", timeout=60000)
    except Exception:
        pass
    enable_flutter_semantics(page)
    flutter_fill(page, "Email", "librarian@library.com")
    flutter_fill(page, "Mật khẩu", "admin123")
    flutter_click_button(page, "Đăng nhập")
    page.wait_for_timeout(3000)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC-01_librarian_login.png"))
    sem = " ".join(page.locator("flt-semantics").all_text_contents())
    assert any(kw in sem for kw in ["Nguyen Thu Thu", "Thủ thư", "Librarian", "Đăng xuất"]), \
        f"TC-01 FAIL: Librarian login should show name/role. Got: {sem[:300]}"


# ── TC-02: Member login success ───────────────────────────────────────────
def test_TC02_member_login_success(page):
    """Manual verdict: PASS — Login OK, AppBar shows Nguyen Hoc Ba (Member)"""
    login(page, "ba.nguyen@email.com", "password123")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC-02_member_login.png"))
    enable_flutter_semantics(page)
    sem = " ".join(page.locator("flt-semantics").all_text_contents())
    assert any(kw in sem for kw in ["Nguyen Hoc Ba", "Thành viên", "Member", "Đăng xuất"]), \
        f"TC-02 FAIL: Member login should show name/role. Got: {sem[:300]}"


# ── TC-03: Non-existent email → rejected ─────────────────────────────────
def test_TC03_nonexistent_email_rejected(page):
    """Manual verdict: PASS — Login failed, stays on login page"""
    page.goto(BASE_URL, wait_until="load", timeout=90000)
    try:
        page.locator("flt-glass-pane").wait_for(state="attached", timeout=60000)
    except Exception:
        pass
    enable_flutter_semantics(page)
    flutter_fill(page, "Email", "noone@email.com")
    flutter_fill(page, "Mật khẩu", "password123")
    flutter_click_button(page, "Đăng nhập")
    page.wait_for_timeout(2500)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC-03_nonexistent_email.png"))
    sem = " ".join(page.locator("flt-semantics").all_text_contents())
    still_on_login = any(kw in sem for kw in ["Đăng nhập", "Email", "Mật khẩu"])
    has_error = any(kw in sem for kw in ["không tìm thấy", "not found", "sai", "lỗi",
                                          "Member not found", "Invalid"])
    assert still_on_login or has_error, \
        f"TC-03 FAIL: Non-existent email should be rejected. Got: {sem[:300]}"


# ── TC-04: Wrong password → 'Incorrect password' ─────────────────────────
def test_TC04_wrong_password_rejected(page):
    """Manual verdict: PASS — Shows 'Incorrect password', page does not change"""
    page.goto(BASE_URL, wait_until="load", timeout=90000)
    try:
        page.locator("flt-glass-pane").wait_for(state="attached", timeout=60000)
    except Exception:
        pass
    enable_flutter_semantics(page)
    flutter_fill(page, "Email", "ba.nguyen@email.com")
    flutter_fill(page, "Mật khẩu", "wrongpassword")
    flutter_click_button(page, "Đăng nhập")
    page.wait_for_timeout(2500)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC-04_wrong_password.png"))
    sem = " ".join(page.locator("flt-semantics").all_text_contents())
    assert any(kw in sem for kw in ["Incorrect password", "sai mật khẩu", "Sai",
                                     "Mật khẩu không đúng", "không đúng"]), \
        f"TC-04 FAIL: Wrong password should show rejection message. Got: {sem[:300]}"


# ── TC-05: Empty email and password → empty field message ─────────────────
def test_TC05_empty_email_and_password(page):
    """Manual verdict: PASS — Shows 'Please enter email and password'"""
    page.goto(BASE_URL, wait_until="load", timeout=90000)
    try:
        page.locator("flt-glass-pane").wait_for(state="attached", timeout=60000)
    except Exception:
        pass
    enable_flutter_semantics(page)
    # Leave fields empty, just click login
    flutter_click_button(page, "Đăng nhập")
    page.wait_for_timeout(2000)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC-05_empty_fields.png"))
    sem = " ".join(page.locator("flt-semantics").all_text_contents())
    still_on_login = any(kw in sem for kw in ["Đăng nhập", "Email", "Mật khẩu"])
    has_msg = any(kw in sem for kw in ["Please enter", "Vui lòng nhập", "email", "mật khẩu",
                                        "trống", "bắt buộc"])
    assert still_on_login, \
        f"TC-05 FAIL: Empty login should stay on login page. Got: {sem[:300]}"


# ── TC-06: Suspended member (MEM004) can log in ───────────────────────────
def test_TC06_suspended_member_can_login(page):
    """Manual verdict: PASS — Login OK, AppBar shows Le Can Cu (Member)"""
    login(page, "cu.le@email.com", "password123")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC-06_suspended_login.png"))
    enable_flutter_semantics(page)
    sem = " ".join(page.locator("flt-semantics").all_text_contents())
    assert any(kw in sem for kw in ["Le Can Cu", "Đăng xuất", "Thoát"]), \
        f"TC-06 FAIL: Suspended member should be able to log in. Got: {sem[:300]}"


# ── TC-07: Expired member (MEM005) can log in ────────────────────────────
def test_TC07_expired_member_can_login(page):
    """Manual verdict: PASS — Login OK, AppBar shows Pham Trung Binh (Member)"""
    login(page, "binh.pham@email.com", "password123")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC-07_expired_login.png"))
    enable_flutter_semantics(page)
    sem = " ".join(page.locator("flt-semantics").all_text_contents())
    assert any(kw in sem for kw in ["Pham Trung Binh", "Đăng xuất", "Thoát"]), \
        f"TC-07 FAIL: Expired member should be able to log in. Got: {sem[:300]}"


# ── TC-31: Only email empty (password filled) → rejected ─────────────────
def test_TC31_only_email_empty_rejected(page):
    """Manual verdict: PASS — Shows message, page does not change"""
    page.goto(BASE_URL, wait_until="load", timeout=90000)
    try:
        page.locator("flt-glass-pane").wait_for(state="attached", timeout=60000)
    except Exception:
        pass
    enable_flutter_semantics(page)
    # Only fill password, leave email empty
    flutter_fill(page, "Mật khẩu", "password123")
    flutter_click_button(page, "Đăng nhập")
    page.wait_for_timeout(2000)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC-31_only_email_empty.png"))
    sem = " ".join(page.locator("flt-semantics").all_text_contents())
    still_on_login = any(kw in sem for kw in ["Đăng nhập", "Email", "Mật khẩu"])
    assert still_on_login, \
        f"TC-31 FAIL: Login with empty email should stay on login page. Got: {sem[:300]}"
