"""
REQ-08 Borrow Record Lookup — Verification of Manual Submission
TCs: TC-29, TC-30, TC-36 (PASS) | TC-39 (FAIL→BUG-07)
Manual verdict: 3 Pass, 1 Fail
BUG-07: CRITICAL — Member can view and return another member's records (access control breach)
"""
import os
import pytest
from conftest import (
    login, enable_flutter_semantics, flutter_fill,
    flutter_click_button, wait_for_flutter, reset_database, SCREENSHOT_DIR
)

BORROW_TAB = 'flt-semantics[role="tab"][aria-label="Mượn / Trả"]'
TRA_CUU_TAB = 'flt-semantics[role="tab"][aria-label="Tra cứu phiếu mượn"]'
SEARCH_INPUT_LABEL = "Nhập mã thành viên (VD: MEM001)"
BR_RECORD  = 'flt-semantics[role="group"][aria-label*="Mã: BR"]'


def _click_borrow_tab(page):
    tab = page.locator(BORROW_TAB)
    if tab.count() > 0:
        tab.first.click()
        page.wait_for_timeout(2000)
        enable_flutter_semantics(page)


# ── TC-29: Librarian views any member's records ───────────────────────────
def test_TC29_librarian_views_any_member_records(page):
    """Manual verdict: PASS — Librarian sees all records with all required fields"""
    login(page, "librarian@library.com", "admin123")
    _click_borrow_tab(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC-29_librarian_records.png"))
    sem = " ".join(page.locator("flt-semantics").all_text_contents())
    has_records = page.locator(BR_RECORD).count() > 0 or any(
        kw in sem for kw in ["BR001", "BR002", "BR003", "Đang mượn", "Quá hạn", "Đã trả"]
    )
    assert has_records, \
        f"TC-29 FAIL: Librarian should see borrow records from all members. Got: {sem[:300]}"


# ── TC-30: Member views only own records ──────────────────────────────────
def test_TC30_member_views_only_own_records(page):
    """Manual verdict: PASS — MEM002 sees BR001, NOT other members' records"""
    login(page, "ba.nguyen@email.com", "password123")
    _click_borrow_tab(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC-30_member_own_records.png"))
    sem = " ".join(page.locator("flt-semantics").all_text_contents())
    has_own = any(kw in sem for kw in ["BR001", "Đang mượn", "Quá hạn", "Trả sách"])
    has_others = any(kw in sem for kw in ["MEM003", "MEM006", "biet.hoang", "dam.tran"])
    assert has_own, \
        f"TC-30 FAIL: MEM002 should see their own borrow records. Got: {sem[:300]}"
    assert not has_others, \
        f"TC-30 FAIL: MEM002 should NOT see other members' records. Got: {sem[:300]}"


# ── TC-36: Returned record shows correct status + all fields ──────────────
def test_TC36_returned_record_shows_correct_fields(page):
    """Manual verdict: PASS — Returned record shows 'Đã trả' + Record ID/Book/Dates"""
    # Librarian returns a book to ensure a 'Đã trả' record exists
    login(page, "librarian@library.com", "admin123")
    _click_borrow_tab(page)
    ret_btn = page.locator('flt-semantics[role="button"]:has-text("Trả sách")').first
    if ret_btn.count() > 0:
        ret_btn.click()
        page.wait_for_timeout(2500)
        enable_flutter_semantics(page)

    # Switch to MEM002
    flutter_click_button(page, "Đăng xuất")
    page.wait_for_timeout(2000)
    enable_flutter_semantics(page)
    flutter_fill(page, "Email", "ba.nguyen@email.com")
    flutter_fill(page, "Mật khẩu", "password123")
    flutter_click_button(page, "Đăng nhập")
    wait_for_flutter(page, text="Đăng xuất")
    enable_flutter_semantics(page)

    _click_borrow_tab(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC-36_returned_record.png"))
    sem = " ".join(page.locator("flt-semantics").all_text_contents())
    has_returned = ("Đã trả" in sem or
                    page.locator('flt-semantics[role="group"][aria-label*="Đã trả"]').count() > 0)
    assert has_returned, \
        f"TC-36 FAIL: MEM002's returned record should show 'Đã trả' status. Got: {sem[:300]}"


# ── TC-39: Cross-member access control breach (BUG-07) ────────────────────
@pytest.mark.xfail(
    strict=False,
    reason="BUG-07 (CRITICAL): MEM002 can search for MEM006's ID and view MEM006's borrow "
           "records; Return button is accessible for other member's records. "
           "Full access control breach. Manual verdict: FAIL.",
)
def test_TC39_member_cannot_access_other_member_records(page):
    """Manual verdict: FAIL → BUG-07 CRITICAL — MEM002 can view/return MEM006's records"""
    login(page, "ba.nguyen@email.com", "password123")
    _click_borrow_tab(page)

    # Click the Tra cứu phiếu mượn tab
    tab = page.locator(TRA_CUU_TAB)
    if tab.count() > 0:
        tab.first.click()
        page.wait_for_timeout(2000)
        enable_flutter_semantics(page)

    # Fill target member ID
    flutter_fill(page, SEARCH_INPUT_LABEL, "MEM006")
    page.wait_for_timeout(1000)
    enable_flutter_semantics(page)

    # Click Tra cứu
    flutter_click_button(page, "Tra cứu")
    page.wait_for_timeout(2500)
    enable_flutter_semantics(page)

    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC-39_cross_member_access.png"))
    sem = " ".join(page.locator("flt-semantics").all_text_contents())

    has_other_records = any(kw in sem for kw in ["MEM006", "Hoàng Cá Biệt", "biet.hoang"])
    
    assert not has_other_records, \
        f"TC-39 FAIL (BUG-07 CRITICAL): MEM002 can see MEM006's borrow records — " \
        f"access control breach: member data exposed to other members. Got: {sem[:200]}"
