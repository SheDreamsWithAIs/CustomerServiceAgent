from app.tools.billing_accounts import lookup_account


def test_lookup_account_user_123():
    acct = lookup_account("user_123")
    assert acct.get("email") == "jess@example.com"
    assert acct.get("plan") == "Pro"
    assert acct.get("last_invoice_id") == "INV-1001"

