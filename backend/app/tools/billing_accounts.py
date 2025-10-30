"""
LangChain Version: v1.0+
Documentation Reference:
  - https://docs.langchain.com/oss/python/langchain/tools
Last Verified: 2025-10-30
"""

import json
from pathlib import Path
from typing import Dict, Any

from langchain_core.tools import tool


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _accounts_path() -> Path:
    return _repo_root() / "backend" / "data" / "accounts.json"


def _load_accounts() -> Dict[str, Any]:
    path = _accounts_path()
    if not path.exists():
        return {"accounts": []}
    return json.loads(path.read_text(encoding="utf-8"))


def lookup_account(selector: str) -> Dict[str, Any]:
    """Direct lookup helper for API usage (not as a tool)."""
    data = _load_accounts()
    accounts = data.get("accounts", [])
    for acct in accounts:
        if selector and (acct.get("user_id") == selector or acct.get("email") == selector):
            return acct
    return {}


@tool
def get_account_info(selector: str) -> str:
    """Lookup a mock account by user_id or email. Pass selector as user_id or email."""
    data = _load_accounts()
    accounts = data.get("accounts", [])
    for acct in accounts:
        if selector and (acct.get("user_id") == selector or acct.get("email") == selector):
            return json.dumps({
                "user_id": acct.get("user_id"),
                "email": acct.get("email"),
                "plan": acct.get("plan"),
                "balance_due": acct.get("balance_due"),
                "currency": acct.get("currency"),
                "last_invoice_id": acct.get("last_invoice_id"),
                "open_tickets": acct.get("open_tickets"),
            })
    return "{}"


