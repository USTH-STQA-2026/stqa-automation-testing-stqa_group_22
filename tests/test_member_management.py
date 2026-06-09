"""
REQ-07 Member Management — Verification of Manual Submission
TCs: TC-28 (PASS) | TC-25, TC-26, TC-27 (FAIL→BUG-05)
Manual verdict: 1 Pass, 3 Fail
BUG-05: Add Member email validation broken — rejects valid, accepts invalid, wrong dup msg
"""
import os
import pytest
from conftest import (
    login, enable_flutter_semantics, flutter_fill,
    flutter_click_button, SCREENSHOT_DIR
)

MEMBER_TAB = 'flt-semantics[role="tab"][aria-label="Thành viên"]'
ADD_MEMBER_BTN_TEXTS = ["Thêm thành viên", "Thêm", "Add Member", "Add"]
SAVE_BTN_TEXTS = ["Lưu", "Thêm", "Xác nhận", "Save", "Confirm", "OK"]

NAME_LABELS  = ["Họ tên", "Họ và tên", "Tên thành viên", "Full Name", "Name", "Tên"]
EMAIL_LABELS = ["Email", "Địa chỉ email", "Email address"]
PHONE_LABELS = ["Số điện thoại", "SĐT", "Điện thoại", "Phone", "Phone number"]


def _go_to_member_tab(page):
    page.locator(MEMBER_TAB).click()
    page.wait_for_timeout(1500)
    enable_flutter_semantics(page)


def _open_add_member_form(page):
    for btn_text in ADD_MEMBER_BTN_TEXTS:
        btn = page.locator(f'flt-semantics[role="button"]:has-text("{btn_text}")')
        if btn.count() > 0:
            btn.first.click()
            page.wait_for_timeout(1500)
            enable_flutter_semantics(page)
            return True
    return False


def _find_and_fill(page, candidate_labels, value):
    for label in candidate_labels:
        field = page.locator(f'input[aria-label="{label}"]')
        if field.count() > 0:
            flutter_fill(page, label, value)
            return label
    return None


def _fill_member_form(page, name="", email="", phone=""):
    _find_and_fill(page, NAME_LABELS, name)
    _find_and_fill(page, EMAIL_LABELS, email)
    _find_and_fill(page, PHONE_LABELS, phone)


def _submit_member_form(page):
    for btn_text in SAVE_BTN_TEXTS:
        btn = page.locator(f'flt-semantics[role="button"]:has-text("{btn_text}")').last
        if btn.count() > 0:
            btn.click()
            page.wait_for_timeout(2000)
            enable_flutter_semantics(page)
            return True
    return False


def _has_error(sem_text):
    return any(kw in sem_text for kw in [
        "không hợp lệ", "invalid", "lỗi", "error", "bắt buộc",
        "required", "không được để trống", "trống"
    ])


def _member_created(sem_text, email):
    return email and email in sem_text


# ── TC-28: Member has no Members tab ─────────────────────────────────────
def test_TC28_member_has_no_members_tab(page):
    """Manual verdict: PASS — Member role: no Members tab or Add Member button visible"""
    login(page, "ba.nguyen@email.com", "password123")
    page.wait_for_timeout(2000)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC-28_member_no_tab.png"))
    members_tab_visible = page.locator(MEMBER_TAB).count() > 0
    add_member_btn_visible = any(
        page.locator(f'flt-semantics[role="button"]:has-text("{btn}")').count() > 0
        for btn in ADD_MEMBER_BTN_TEXTS
    )
    assert not members_tab_visible, \
        "TC-28 FAIL: Member role should NOT see the Members tab"
    assert not add_member_btn_visible, \
        "TC-28 FAIL: Member role should NOT see the 'Add Member' button"


# ── TC-25: Add valid member → rejected as 'Invalid email' (BUG-05) ────────
@pytest.mark.xfail(
    strict=True,
    reason="BUG-05: Valid email 'tay.tran@email.com' is incorrectly rejected with "
           "'Invalid email' message. Member not created. Manual verdict: FAIL.",
)
def test_TC25_add_valid_member_fails(page):
    """Manual verdict: FAIL → BUG-05 — tay.tran@email.com rejected as 'Invalid email'"""
    login(page, "librarian@library.com", "admin123")
    _go_to_member_tab(page)

    if not _open_add_member_form(page):
        pytest.skip("Add member button not found")

    _fill_member_form(page, name="Trần Thị Tây", email="tay.tran@email.com", phone="0363636361")
    _submit_member_form(page)

    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC-25_add_member_valid.png"))
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())

    has_err = _has_error(sem_text)
    assert not has_err or "Thành viên" in sem_text, \
        f"TC-25 FAIL (BUG-05): Error shown for fully valid input. sem_text: {sem_text[:300]}"


# ── TC-26: Invalid email (no dot in domain) accepted (BUG-05) ─────────────
@pytest.mark.xfail(
    strict=True,
    reason="BUG-05: Invalid email 'tay.tran@emailcom' (no dot) is accepted and member is created successfully. Manual verdict: FAIL."
)
def test_TC26_invalid_email_no_dot_accepted(page):
    """Manual verdict: FAIL → BUG-05 — tay.tran@emailcom accepted (should be rejected)"""
    login(page, "librarian@library.com", "admin123")
    _go_to_member_tab(page)

    if not _open_add_member_form(page):
        pytest.skip("Add member button not found")

    _fill_member_form(page, name="Test No Dot", email="tay.tran@emailcom", phone="0901234567")
    _submit_member_form(page)

    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC-26_invalid_email_no_dot.png"))
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())

    has_err = _has_error(sem_text)
    created = _member_created(sem_text, "tay.tran@emailcom")
    assert has_err or not created, \
        "TC-26 FAIL (BUG-05): Email 'user@domain' (no dot) accepted — validation missing"


# ── TC-27: Duplicate email → generic 'Invalid email' message (BUG-05) ─────
@pytest.mark.xfail(
    strict=True,
    reason="BUG-05: Duplicate email shows 'Invalid email' instead of duplicate error message. Manual verdict: FAIL."
)
def test_TC27_duplicate_email_wrong_message(page):
    """Manual verdict: FAIL → BUG-05 — Duplicate email shows 'Invalid email' not 'duplicate'"""
    login(page, "librarian@library.com", "admin123")
    _go_to_member_tab(page)

    if not _open_add_member_form(page):
        pytest.skip("Add member button not found")

    _fill_member_form(page, name="Nguyen Duplicate", email="ba.nguyen@email.com", phone="0901234567")
    _submit_member_form(page)

    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC-27_duplicate_email.png"))
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())

    has_dup_msg = any(kw in sem_text.lower() for kw in ["đã tồn tại", "tồn tại", "duplicate", "exists", "trùng"])
    assert has_dup_msg, \
        "TC-27 FAIL (BUG-05): Duplicate email should show a duplicate error message, not generic format error"
