# app/api/v1/endpoints/events.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime, timezone
import uuid
import hashlib

from nacl.signing import SigningKey

from app.engine.state.event_chain import get_latest_hash, store_event

from app.engine.validation.hash_validation import (
    canonical_json_bytes,
    filtered_for_hash,
)

from app.engine.validation.validator import EventValidator


# Optional DB persistence helper (if available)
try:
    from app.db.event_db import add_event_db as store_event_db
except Exception:
    try:
        from app.db.event_db import store_event_db
    except Exception:
        store_event_db = None

router = APIRouter()
validator = EventValidator()


# -------------------------------------------------------------------
# Load signing key (hex-encoded Ed25519 private key)
# -------------------------------------------------------------------
def load_private_key(path="data/keys/truetrace_priv.bin") -> SigningKey:
    try:
        with open(path, "rb") as f:
            return SigningKey(f.read())
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to load private key: {e}"
        )


class CreateEventRequest(BaseModel):
    event_type: str
    payload: Dict[str, Any]


@router.post("/create")
def create_event(req: CreateEventRequest):
    """
    Create a version 1.5 TrueTrace event with:
      - SHA256 canonical hash
      - Ed25519 signature (HEX)
      - Ed25519 public key (HEX)
    """

    # 1) Build base event (unsigned)
    event_id = f"evt-{uuid.uuid4().hex[:12]}"
    timestamp = int(datetime.now(timezone.utc).timestamp())
    prev_hash = get_latest_hash() or ""

    base_event = {
        "event_id": event_id,
        "event_version": "1.5",
        "timestamp": timestamp,
        "event_type": req.event_type,
        "payload": req.payload,
        "prev_hash": prev_hash,
        "origin": "system",
        "trace_id": uuid.uuid4().hex,
    }

    # 2) Prepare object for hashing
    filtered = filtered_for_hash(base_event)

    # 3) Canonical JSON → hash
    canonical_bytes = canonical_json_bytes(filtered)
    event_hash = hashlib.sha256(canonical_bytes).hexdigest()

    # 4) Build full event
    full_event = dict(filtered)
    full_event["hash"] = event_hash

    # 5) Sign canonical bytes using Ed25519 (HEX)
    try:
        signing_key = load_private_key()
        signature = signing_key.sign(canonical_bytes).signature.hex()
        pubkey = signing_key.verify_key.encode().hex()

        full_event["signature"] = signature
        full_event["pubkey"] = pubkey

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Signing failed: {e}"
        )

    # 6) Validate final event (hash + signature)
    is_valid, result = validator.validate(full_event)
    if not is_valid:
        raise HTTPException(
            status_code=400,
            detail={
                "message": result["message"],
                "errors": result["errors"],
                "computed_hash": result.get("computed_hash"),
            },
        )

    # 7) Persist to JSON chain
    try:
        store_event(full_event)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chain store failed: {e}")

    # 8) Optional SQLite persistence
    if store_event_db:
        try:
            store_event_db(full_event)
        except Exception:
            # DB errors don't block success, chain persistence already done
            pass

    return {"status": "created", "event": full_event}
