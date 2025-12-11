import json
import os

from app.core.paths import CHAIN_FILE
from app.engine.validation.hash_validation import compute_event_hash


def load_chain():
    """
    Load entire chain from JSONL file.
    Returns a list of event dicts.
    """
    if not os.path.exists(CHAIN_FILE):
        return []

    with open(CHAIN_FILE, "r", encoding="utf-8") as f:
        return [json.loads(line.strip()) for line in f if line.strip()]


def get_all_events():
    """Return the full list of events."""
    return load_chain()


def get_event_by_index(index: int):
    """Return event at index or None."""
    chain = load_chain()
    if index < 0 or index >= len(chain):
        return None
    return chain[index]


def get_chain_length():
    """Return number of events in chain."""
    return len(load_chain())


def get_last_event_hash():
    """Return event_hash of last event, or None."""
    chain = load_chain()
    if not chain:
        return None
    return chain[-1].get("event_hash")


def get_latest_event():
    """Return the last event object in the chain."""
    chain = load_chain()
    if not chain:
        return None
    return chain[-1]


def append_event_to_chain(event: dict):
    """
    Append an event to the chain.
    - Computes event_hash
    - Adds prev_hash
    - Appends to JSONL file
    """
    chain = load_chain()
    prev_hash = chain[-1]["event_hash"] if chain else None

    event_hash = compute_event_hash(event, prev_hash)

    event["prev_hash"] = prev_hash
    event["event_hash"] = event_hash

    with open(CHAIN_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")

    return event
