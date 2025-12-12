import json
from hashlib import sha256
from typing import Any, Dict

# -----------------------------------------------------------
# Canonicalizer Helpers
# -----------------------------------------------------------


def canonical_json_bytes(obj: Any) -> bytes:
    """
    Converts any JSON-compatible object to stable canonical JSON bytes.
    Removes whitespace, sorts keys, ensures deterministic structure.
    """
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")


def filtered_for_hash(event: Dict[str, Any]) -> Dict[str, Any]:
    """
    Returns the version of an event used for hashing.
    Removes signature, public key, and the event's own hash.
    """
    filtered = {
        k: v for k, v in event.items() if k not in ("hash", "signature", "pubkey")
    }
    return filtered


# -----------------------------------------------------------
# NEW REQUIRED FUNCTION
# -----------------------------------------------------------


def canonical_event_bytes(event: Dict[str, Any]) -> bytes:
    """
    This function is REQUIRED because signatures and hashing must use
    the same canonical JSON representation.

    This function:
    - Removes signature/pubkey/hash
    - Produces canonical JSON bytes
    """
    filtered = filtered_for_hash(event)
    return canonical_json_bytes(filtered)


# -----------------------------------------------------------
# Hashing Function
# -----------------------------------------------------------


def compute_event_hash(event_for_hash: Dict[str, Any]) -> str:
    """
    Produces deterministic SHA-256 hash for the event.
    Matches exactly what signatures use.
    """
    filtered = filtered_for_hash(event_for_hash)
    b = canonical_json_bytes(filtered)
    return sha256(b).hexdigest()
