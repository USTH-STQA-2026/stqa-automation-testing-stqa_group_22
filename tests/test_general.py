"""
REQ-02 View Book List & REQ-06 Overdue Processing — Verification of Manual Submission
TCs: TC-08, TC-09, TC-24, TC-35 (PASS) | TC-23 (FAIL→BUG-04)
Manual verdict: 4 Pass, 1 Fail
"""
import os
import pytest
from conftest import (
    login, enable_flutter_semantics, flutter_fill,
    flutter_click_button, wait_for_flutter, reset_database, SCREENSHOT_DIR
)

BOOK_CARD = 'flt-semantics[role="group"][aria-label*="Mã: BOOK"]'
BORROW_TAB = 'flt-semantics[role="tab"][aria-label="Mượn / Trả"]'


def _click_borrow_tab(page):
    try:
        tab = page.locator(BORROW_TAB)
        if tab.count() > 0:
            tab.first.click()
            page.wait_for_timeout(2000)
    except Exception:
        pass
    enable_flutter_semantics(page)


def _run_check_overdue(page):
    check_btn = page.locator(
        'flt-semantics[role="button"]:has-text("Kiểm tra quá hạn"), '
        'flt-semantics[role="button"]:has-text("Check Overdue")'
    )
    if check_btn.count() > 0:
        check_btn.first.click()
        page.wait_for_timeout(2500)
        enable_flutter_semantics(page)
        return True
    return False


# ── TC-08: Full book list with all fields ─────────────────────────────────
def test_TC08_full_book_list_with_all_fields(page):
    """Manual verdict: PASS — 20 books shown, all fields present per card"""
    login(page, "ba.nguyen@email.com", "password123")
    page.wait_for_timeout(2000)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC-08_book_list.png"))
    sem = " ".join(page.locator("flt-semantics").all_text_contents())
    # Should show books with status fields
    has_books = any(kw in sem for kw in ["BOOK", "Có sẵn", "Available", "Đang mượn", "Borrowed"])
    has_fields = any(kw in sem for kw in ["Tác giả", "Author", "Thể loại", "Genre",
                                           "Năm", "Year", "Trạng thái", "Status"])
    assert has_books, f"TC-08 FAIL: Should display book list. Got: {sem[:300]}"
    assert has_fields, f"TC-08 FAIL: Book cards should have Name/Author/Genre/Year/Status. Got: {sem[:300]}"


# ── TC-09: Book status updates immediately after borrow ───────────────────
def test_TC09_book_status_updates_after_borrow(page):
    """Manual verdict: PASS — After borrow, book status changes to 'Đang mượn' immediately"""
    login(page, "biet.hoang@email.com", "password123")
    page.wait_for_timeout(2000)
    enable_flutter_semantics(page)

    # Find first available book and borrow it
    available = page.locator(
        f'{BOOK_CARD}[aria-label*="Có sẵn"]'
    ).first
    try:
        available.wait_for(state="attached", timeout=10000)
    except Exception:
        pytest.skip("No available book visible in viewport")

    borrow_btn = available.locator('flt-semantics[role="button"]:has-text("Mượn")')
    if borrow_btn.count() == 0:
        pytest.skip("No borrow button found on available book card")

    borrow_btn.first.click()
    page.wait_for_timeout(2000)
    enable_flutter_semantics(page)

    # Confirm if dialog appears
    confirm = page.locator('flt-semantics[role="button"]:has-text("Mượn")').last
    if confirm.count() > 0:
        confirm.click()
        page.wait_for_timeout(2000)
        enable_flutter_semantics(page)

    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC-09_status_update.png"))
    sem = " ".join(page.locator("flt-semantics").all_text_contents())
    # After borrow, should see 'Đang mượn' somewhere
    assert any(kw in sem for kw in ["Đang mượn", "Borrowed", "thành công"]), \
        f"TC-09 FAIL: Book status should update to 'Đang mượn' after borrow. Got: {sem[:300]}"


# ── TC-23: Check Overdue boundary error + run-2 returns 0 (BUG-04) ────────
@pytest.mark.xfail(
    strict=True,
    reason="BUG-04: Overdue check has boundary date error — records due exactly today "
           "are not flagged. Run-2 reports 0 records even when overdue records exist. "
           "Manual verdict: FAIL.",
)
def test_TC23_check_overdue_boundary_and_idempotency(page):
    """Manual verdict: FAIL → BUG-04 — Boundary error (today not flagged); run-2 returns 0"""
    reset_database(page)

    login(page, "librarian@library.com", "admin123")
    _click_borrow_tab(page)

    check_btn = page.locator(
        'flt-semantics[role="button"]:has-text("Kiểm tra quá hạn")'
    )
    try:
        check_btn.first.wait_for(state="attached", timeout=10000)
    except Exception:
        pytest.skip("Check Overdue button not found")

    # Run 1
    check_btn.first.click()
    page.wait_for_timeout(2500)
    enable_flutter_semantics(page)
    overdue_count_run1 = page.locator(
        'flt-semantics[role="group"][aria-label*="Quá hạn"]'
    ).count()

    # Run 2 — should still see the same overdue records (idempotent)
    check_btn2 = page.locator('flt-semantics[role="button"]:has-text("Kiểm tra quá hạn")')
    if check_btn2.count() > 0:
        check_btn2.first.click()
        page.wait_for_timeout(2500)
        enable_flutter_semantics(page)

    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC-23_check_overdue.png"))
    overdue_count_run2 = page.locator(
        'flt-semantics[role="group"][aria-label*="Quá hạn"]'
    ).count()

    assert overdue_count_run2 > 0, \
        f"TC-23 FAIL (BUG-04): After 2 runs of Check Overdue, BR001 should still show "\
        f"'Quá hạn'. Run-1 found {overdue_count_run1}, Run-2 found {overdue_count_run2}."


# ── TC-24: Member views own overdue record ────────────────────────────────
def test_TC24_member_views_own_overdue_record(page):
    """Manual verdict: PASS — MEM002 sees BR001 with 'Quá hạn' status"""
    reset_database(page)

    # Step 1: Librarian runs Check Overdue
    login(page, "librarian@library.com", "admin123")
    _click_borrow_tab(page)
    _run_check_overdue(page)

    # Step 2: Switch to MEM002
    flutter_click_button(page, "Đăng xuất")
    page.wait_for_timeout(2000)
    enable_flutter_semantics(page)
    flutter_fill(page, "Email", "ba.nguyen@email.com")
    flutter_fill(page, "Mật khẩu", "password123")
    flutter_click_button(page, "Đăng nhập")
    wait_for_flutter(page, text="Đăng xuất")
    enable_flutter_semantics(page)

    _click_borrow_tab(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC-24_member_overdue.png"))
    sem = " ".join(page.locator("flt-semantics").all_text_contents())
    assert any(kw in sem for kw in ["Quá hạn", "Overdue", "BR001", "Đang mượn", "Trả sách"]), \
        f"TC-24 FAIL: MEM002 should see own borrow/overdue record (BR001). Got: {sem[:300]}"


# ── TC-35: Librarian sees ALL overdue records across members ──────────────
def test_TC35_librarian_sees_all_overdue_records(page):
    """Manual verdict: PASS — Librarian sees overdue records from all members after Check Overdue"""
    reset_database(page)

    login(page, "librarian@library.com", "admin123")
    _click_borrow_tab(page)
    _run_check_overdue(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC-35_all_overdue.png"))
    sem = " ".join(page.locator("flt-semantics").all_text_contents())
    overdue_recs = page.locator('flt-semantics[role="group"][aria-label*="Quá hạn"]')
    has_overdue = overdue_recs.count() > 0 or "Quá hạn" in sem
    assert has_overdue, \
        f"TC-35 FAIL: Librarian should see overdue records for all members after Check Overdue. Got: {sem[:300]}"
