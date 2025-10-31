from app.api.v1.routers.chat import _short_snippet


def test_short_snippet_truncates_cleanly():
    text = (
        "Title: Policy\nPlans A, B, C. Invoices follow a pattern. This sentence should be cut after here. "
        "Extra words that will be truncated mid flow if not careful."
    )
    out = _short_snippet(text, max_len=80)
    assert out.endswith("…") or out.endswith(".")
    assert len(out) <= 85

