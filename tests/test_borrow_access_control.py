"""
REQ-04 Borrow Book Access Control — Verification of Manual Submission
TCs: TC-17, TC-20 (PASS) | TC-18 (FAIL→BUG-03), TC-19 (FAIL→BUG-01)
Manual verdict: 2 Pass, 2 Fail
"""
import os
import pytest
from conftest import (
    login, enable_flutter_semantics, flutter_fill,
    flutter_click_button, reset_database, SCREENSHOT_DIR
)

BOOK_CARD = 'flt-semantics[role="group"][aria-label*="Mã: BOOK"]'


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


# ── TC-17: Suspended member (MEM004) borrow → rejected, but WRONG message (BUG-03) ─
# Screenshot evidence: system shows "Thành viên đã hết hạn" (expired msg) for SUSPENDED member.
# Both suspended (MEM004) and expired (MEM005) receive the same "hết hạn" message.
# The bug is that the system does NOT differentiate messages: suspended should show a suspension
# message (e.g. "tạm ngưng"), NOT an expired message ("hết hạn").
@pytest.mark.xfail(
    strict=False,
    reason="BUG-03 (actual): Suspended member MEM004 receives 'Thành viên đã hết hạn' "
           "(expired message) instead of a suspension-specific message. "
           "System uses the same message for both Suspended and Expired statuses.",
)
def test_TC17_suspended_member_borrow_rejected_wrong_message(page):
    """Manual verdict: PASS (borrow rejected) — but message is wrong: shows 'expired' not 'suspended'"""
    login(page, "cu.le@email.com", "password123")
    page.wait_for_timeout(2000)
    enable_flutter_semantics(page)
    ok = _borrow_first_available(page)
    if not ok:
        page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC-17_suspended_borrow.png"))
        pytest.skip("No borrow button visible — UI may have correctly blocked suspended member")

    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC-17_suspended_borrow.png"))
    sem = " ".join(page.locator("flt-semantics").all_text_contents())

    is_success = any(kw in sem.lower() for kw in ["thành công", "success", "successfully"])
    assert not is_success, \
        f"TC-17 FAIL: Suspended member should NOT be able to borrow. Got success. sem: {sem[:300]}"

    # EXPECTED (per SRS): message cites SUSPENSION (e.g. "tạm ngưng", "đình chỉ")
    # ACTUAL (BUG-03): message says "hết hạn" (expired) — wrong status reason
    has_correct_suspended_msg = any(kw in sem.lower() for kw in ["tạm ngưng", "suspended", "đình chỉ", "tạm khóa"])
    assert has_correct_suspended_msg, \
        f"TC-17 FAIL (BUG-03): Suspended member should see 'suspension' message, not 'expired'. Got: {sem[:300]}"


# ── TC-18: Expired member (MEM005) → correctly rejected with 'expired' message ──
# Screenshot evidence: system shows "Thành viên đã hết hạn. Không thể mượn sách."
# This IS the correct message for expired member per SRS.
# BUG-03 note: the system uses the SAME "hết hạn" message for BOTH suspended & expired
# members → only the expired member gets the correct reason; suspended member gets wrong reason.
def test_TC18_expired_member_borrow_rejected(page):
    """Manual verdict: FAIL → BUG-03 — actual: expired member gets 'hết hạn' (correct);
    but suspended member also gets 'hết hạn' (wrong) — messages are not differentiated."""
    login(page, "binh.pham@email.com", "password123")
    page.wait_for_timeout(2000)
    enable_flutter_semantics(page)
    ok = _borrow_first_available(page)
    if not ok:
        pytest.skip("No available book for TC-18 expired member test")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC-18_expired_borrow.png"))
    sem = " ".join(page.locator("flt-semantics").all_text_contents())
    is_success = any(kw in sem.lower() for kw in ["thành công", "success", "successfully"])
    has_expired_msg = any(kw in sem.lower() for kw in ["hết hạn", "expired", "quá hạn thành viên"])
    assert not is_success, \
        f"TC-18 FAIL: Expired member should not be able to borrow. Got: {sem[:300]}"
    assert has_expired_msg, \
        f"TC-18 FAIL: Expired member should see rejection with 'hết hạn' message. Got: {sem[:300]}"


# ── TC-19: 4th borrow allowed — 3-book limit not enforced (BUG-01) ─────────
@pytest.mark.xfail(
    strict=True,
    reason="BUG-01: System allows 4th borrow — borrow limit uses '>' instead of '>=' "
           "causing off-by-one. Manual verdict: FAIL.",
)
def test_TC19_borrow_limit_3_books_not_enforced(page):
    """Manual verdict: FAIL → BUG-01 — 4th book is allowed; limit of 3 not enforced"""
    # Use MEM002 who starts with 1 active borrow (BOOK003)
    login(page, "ba.nguyen@email.com", "password123")
    page.wait_for_timeout(2000)
    enable_flutter_semantics(page)

    # Borrow 2 more to reach 3 total
    for _ in range(2):
        _borrow_first_available(page)
        page.wait_for_timeout(1000)
        enable_flutter_semantics(page)

    # 4th borrow attempt — MUST be rejected
    _borrow_first_available(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC-19_borrow_limit.png"))
    sem = " ".join(page.locator("flt-semantics").all_text_contents())
    has_limit_msg = any(kw in sem for kw in ["giới hạn", "tối đa", "3 sách", "limit",
                                              "3 quyển", "vượt quá"])
    assert has_limit_msg, \
        f"TC-19 FAIL (BUG-01): 4th borrow should be rejected with limit message. Got: {sem[:300]}"


# ── TC-20: Lost book (BOOK007) → borrow rejected ──────────────────────────
def test_TC20_lost_book_cannot_be_borrowed(page):
    """Manual verdict: PASS — BOOK007 'Thất lạc' has no borrow button"""
    login(page, "biet.hoang@email.com", "password123")
    page.wait_for_timeout(2000)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC-20_lost_book.png"))
    lost_cards = page.locator(f'{BOOK_CARD}[aria-label*="Thất lạc"]')
    if lost_cards.count() == 0:
        pytest.skip("BOOK007 (Thất lạc) not visible in Flutter virtual list viewport")
    borrow_btn = lost_cards.first.locator('flt-semantics[role="button"]:has-text("Mượn sách này")')
    assert borrow_btn.count() == 0, \
        "TC-20 FAIL: Lost book (BOOK007) should NOT have a borrow button"

