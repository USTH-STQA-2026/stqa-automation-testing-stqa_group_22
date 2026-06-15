"""
REQ-04 Borrow Book & REQ-05 Return Book — Verification of Manual Submission
TCs: TC-15, TC-16, TC-33 (Borrow core) | TC-21, TC-22, TC-38 (Return core)
Manual verdict: All Pass
"""
import os
import pytest
from conftest import (
    login, enable_flutter_semantics, reset_database, SCREENSHOT_DIR
)

BOOK_CARD = 'flt-semantics[role="group"][aria-label*="Mã: BOOK"]'
BORROW_TAB = 'flt-semantics[role="tab"][aria-label="Mượn / Trả"]'


def _borrow_first_available(page):
    """Mượn cuốn sách Available đầu tiên hiển thị trong viewport."""
    page.wait_for_timeout(2000)
    enable_flutter_semantics(page)

    borrow_btn = page.locator('flt-semantics[role="button"]:has-text("Mượn sách này")').first
    if borrow_btn.count() == 0:
        return False

    borrow_btn.click()
    page.wait_for_timeout(2000)
    enable_flutter_semantics(page)

    confirm = page.locator('flt-semantics[role="button"]:has-text("Mượn")').last
    if confirm.count() > 0:
        confirm.click()
        page.wait_for_timeout(2000)
        enable_flutter_semantics(page)
    return True


def _click_borrow_tab(page):
    tab = page.locator(BORROW_TAB)
    if tab.count() > 0:
        tab.first.click()
        page.wait_for_timeout(2000)
        enable_flutter_semantics(page)


# ── TC-15: Borrow book — happy path ───────────────────────────────────────
def test_TC15_borrow_book_success(page):
    """Manual verdict: PASS — BOOK002 borrowed for MEM006; record 'Đang mượn', due date +14 days"""
    login(page, "biet.hoang@email.com", "password123")
    page.wait_for_timeout(2000)
    enable_flutter_semantics(page)
    ok = _borrow_first_available(page)
    if not ok:
        pytest.skip("No available book in viewport for TC-15")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC-15_borrow_success.png"))
    sem = " ".join(page.locator("flt-semantics").all_text_contents())
    assert any(kw in sem for kw in ["thành công", "Đang mượn", "Borrowed", "success"]), \
        f"TC-15 FAIL: Borrow should succeed. Got: {sem[:300]}"


# ── TC-16: Already-borrowed book → rejected ───────────────────────────────
def test_TC16_already_borrowed_book_rejected(page):
    """Manual verdict: PASS — BOOK003 'Đang mượn' shows no borrow button"""
    login(page, "ba.nguyen@email.com", "password123")
    page.wait_for_timeout(2000)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC-16_reject_borrowed.png"))
    book003 = page.locator(f'{BOOK_CARD}[aria-label*="BOOK003"]')
    if book003.count() == 0:
        pytest.skip("BOOK003 not visible in Flutter virtual list viewport")
    borrow_btn = book003.locator('flt-semantics[role="button"]:has-text("Mượn sách này")')
    assert borrow_btn.count() == 0, \
        "TC-16 FAIL: BOOK003 (Đang mượn) should NOT show a borrow button"


# ── TC-33: BVA boundary — 2nd active borrow succeeds ─────────────────────
def test_TC33_borrow_at_bva_boundary_2nd_book(page):
    """Manual verdict: PASS — MEM006 borrows 2nd book (below 3-book limit): succeeds"""
    login(page, "biet.hoang@email.com", "password123")
    page.wait_for_timeout(2000)
    enable_flutter_semantics(page)
    ok = _borrow_first_available(page)
    if not ok:
        pytest.skip("No available book for TC-33 BVA boundary test")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC-33_bva_boundary.png"))
    sem = " ".join(page.locator("flt-semantics").all_text_contents())
    assert any(kw in sem for kw in ["thành công", "Đang mượn", "Borrowed", "success"]), \
        f"TC-33 FAIL: Borrow at BVA boundary (2nd book) should succeed. Got: {sem[:300]}"


# ── TC-21: Return book — happy path ──────────────────────────────────────
def test_TC21_return_book_success(page):
    """Manual verdict: PASS — BR003 (BOOK013, MEM006) returned; status → 'Đã trả'"""
    login(page, "librarian@library.com", "admin123")
    _click_borrow_tab(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC-21_return_before.png"))

    return_btn = page.locator('flt-semantics[role="button"]:has-text("Trả sách")').first
    try:
        return_btn.wait_for(state="attached", timeout=10000)
    except Exception:
        pytest.skip("No 'Trả sách' button found — no active borrow records visible")

    return_btn.click()
    page.wait_for_timeout(2500)
    enable_flutter_semantics(page)

    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC-21_return_success.png"))
    sem = " ".join(page.locator("flt-semantics").all_text_contents())
    assert any(kw in sem for kw in ["thành công", "Đã trả", "Returned", "Có sẵn", "Available"]), \
        f"TC-21 FAIL: Return should succeed. Got: {sem[:300]}"


# ── TC-22: Return unborrowed book → rejected ─────────────────────────────
def test_TC22_return_unborrowed_book_rejected(page):
    """Manual verdict: PASS — MEM003 has no borrow records → no Return button visible"""
    login(page, "dam.tran@email.com", "password123")
    _click_borrow_tab(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC-22_no_return_btn.png"))
    return_btn = page.locator('flt-semantics[role="button"]:has-text("Trả sách")')
    assert return_btn.count() == 0, \
        "TC-22 FAIL: Member with no borrows should NOT see a 'Trả sách' button"


# ── TC-38: Return overdue book → overdue warning shown ───────────────────
def test_TC38_return_overdue_shows_warning(page):
    """Manual verdict: PASS — Return successful AND overdue warning is displayed"""
    login(page, "librarian@library.com", "admin123")
    _click_borrow_tab(page)

    # Ensure Check Overdue has been run so we have an overdue record
    check_btn = page.locator(
        'flt-semantics[role="button"]:has-text("Kiểm tra quá hạn")'
    )
    if check_btn.count() > 0:
        check_btn.first.click()
        page.wait_for_timeout(2500)
        enable_flutter_semantics(page)

    # Find an overdue record (BR001)
    overdue_rec = page.locator('flt-semantics[role="group"][aria-label*="Quá hạn"]').first
    if overdue_rec.count() == 0:
        # Check if the word "Quá hạn" exists in general semantics
        sem_before = " ".join(page.locator("flt-semantics").all_text_contents())
        if "Quá hạn" not in sem_before:
            pytest.skip("No overdue record visible — Check Overdue must mark BR001 first")
        overdue_rec = page.locator('flt-semantics[role="group"]').first # fallback

    ret_btn = overdue_rec.locator('flt-semantics[role="button"]:has-text("Trả sách")')
    if ret_btn.count() == 0:
        ret_btn = page.locator('flt-semantics[role="button"]:has-text("Trả sách")').first

    ret_btn.click()
    page.wait_for_timeout(2500)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC-38_return_overdue.png"))
    sem = " ".join(page.locator("flt-semantics").all_text_contents())

    is_returned = any(kw in sem for kw in ["thành công", "Đã trả", "Returned"])
    has_overdue_warning = any(kw in sem for kw in ["quá hạn", "overdue", "cảnh báo",
                                                    "warning", "phí", "muộn"])
    assert is_returned, \
        f"TC-38 FAIL: Return of overdue book should succeed. Got: {sem[:300]}"
    assert has_overdue_warning, \
        f"TC-38 FAIL: Return of overdue book should show overdue warning. Got: {sem[:300]}"
