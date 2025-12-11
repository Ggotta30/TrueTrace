from pathlib import Path
import json
from typing import List, Dict, Any

from app.core.paths import CHAIN_FILE


# ------------------------------------------------------------
# Safe Loader
# ------------------------------------------------------------

def load_chain() -> List[Dict[str, Any]]:
    """
    Load the event chain.
    Ensures the result is ALWAYS a list.
    If file missing or corrupted, returns empty list.
    """
    if not CHAIN_FILE.exists():
        return []

    try:
        with CHAIN_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        return []

    # Normalize structure
    if isinstance(data, list):
        return data

    if isinstance(data, dict) and "events" in data and isinstance(data["events"], list):
        return data["events"]

    # Unknown structure → reset to empty chain
    return []


def save_chain(chain: List[Dict[str, Any]]) -> None:
    """Persist chain as a simple list."""
    CHAIN_FILE.parent.mkdir(parents=True, exist_ok=True)
    with CHAIN_FILE.open("w", encoding="utf-8") as f:
        json.dump(chain, f, indent=2)


# ------------------------------------------------------------
# Public API
# ------------------------------------------------------------

def get_latest_hash() -> str:
    """
    Return the event_hash of the last event in the chain.
    If chain empty, return an empty string.
    """
    chain = load_chain()  # FIXED: use correct loader
    if not chain:
        return ""

    last = chain[-1]

    if not isinstance(last, dict):
        return ""

    # FIXED: must match actual event structure
    return last.get("event_hash", "")


def append_event(event: Dict[str, Any]) -> None:
    chain = load_chain()
    chain.append(event)
    save_chain(chain)


def store_event(event: Dict[str, Any]) -> None:
    append_event(event)


def get_all_events() -> List[Dict[str, Any]]:
    return load_chain()
