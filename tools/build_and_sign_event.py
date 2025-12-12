import json
import time
import uuid

from nacl.signing import SigningKey

from app.engine.validation.hash_validation import (
    canonical_event_bytes,
    compute_event_hash,
)


def load_private_key(path="data/keys/truetrace_priv.bin"):
    with open(path, "rb") as f:
        return SigningKey(f.read())


def build_event(event_type: str, payload: dict):
    return {
        "event_id": f"evt-{uuid.uuid4().hex[:12]}",
        "event_type": event_type,
        "payload": payload,
        "timestamp": int(time.time() * 1000),
    }


def sign_event(event, signing_key):
    msg = canonical_event_bytes(event)
    signature = signing_key.sign(msg).signature.hex()
    event["signature"] = signature
    event["pubkey"] = signing_key.verify_key.encode().hex()
    event["hash"] = compute_event_hash(event)
    return event


if __name__ == "__main__":
    signing_key = load_private_key()

    evt = build_event("example", {"test": True})
    evt = sign_event(evt, signing_key)

    print(json.dumps(evt, indent=2))
