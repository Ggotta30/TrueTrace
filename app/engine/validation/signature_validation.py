from typing import Any, Dict

from nacl.exceptions import BadSignatureError
from nacl.signing import VerifyKey

from app.engine.validation.hash_validation import canonical_event_bytes

# -----------------------------------------------------------
# Raw Ed25519 Verification
# -----------------------------------------------------------


def verify_ed25519(signature_hex: str, message: bytes, pubkey_hex: str) -> bool:
    """
    Low-level Ed25519 signature check.
    """
    try:
        verify_key = VerifyKey(bytes.fromhex(pubkey_hex))
        signature_bytes = bytes.fromhex(signature_hex)

        verify_key.verify(message, signature_bytes)
        return True

    except BadSignatureError:
        return False
    except Exception:
        return False


# -----------------------------------------------------------
# High-Level Event Verification
# -----------------------------------------------------------


def verify_signature(event: Dict[str, Any]) -> bool:
    """
    Returns True if:
    - signature is valid, OR
    - event is missing signature/pubkey (unsigned events are allowed)

    Returns False only if the signature is present AND invalid.
    """
    signature = event.get("signature")
    pubkey = event.get("pubkey")

    # If no signature fields exist → treat as unsigned (VALID)
    if not signature or not pubkey:
        return True

    msg = canonical_event_bytes(event)
    return verify_ed25519(signature, msg, pubkey)
