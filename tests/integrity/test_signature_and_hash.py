from copy import deepcopy

import pytest


@pytest.mark.unit
def test_signature_and_hash_roundtrip(helpers, sign_fn, pubkey_hex):
    """
    Build a minimal event, sign it, compute hash and assert signature+hash validate
    using your EventValidator and signature verification helpers.
    """
    hv = helpers["hash_validation"]
    sv = helpers["signature_validation"]
    validator_pkg = helpers["validator_mod"]

    # Sanity: required helpers present
    for name in ("canonical_event_bytes", "compute_event_hash", "filtered_for_hash"):
        pytest.importorskip(
            "app.engine.validation.hash_validation", reason=f"{name} missing"
        )

    # Minimal event
    event = {
        "event_id": "evt-test-0001",
        "event_version": "1.5",
        "timestamp": 1234567890,
        "event_type": "test",
        "payload": {"hello": "world"},
        "prev_hash": "",
        "origin": "test",
        "trace_id": "trace-test-1",
    }

    # Prepare for hash (use the same helper your app uses)
    filtered = hv.filtered_for_hash(event)
    canonical_bytes = hv.canonical_event_bytes(filtered)

    # sign
    signature_hex = sign_fn(canonical_bytes)
    event["signature"] = signature_hex
    event["pubkey"] = pubkey_hex

    # compute hash using the repo helper and attach
    event["hash"] = hv.compute_event_hash(event)

    # Validate via high-level validator
    Validator = getattr(validator_pkg, "EventValidator", None)
    assert Validator is not None, "EventValidator missing"
    validator = Validator()

    is_valid, result = validator.validate(deepcopy(event))
    assert is_valid is True, f"Expected event to validate but it failed: {result}"

    # Negative checks: tamper payload -> signature should fail
    tampered = deepcopy(event)
    tampered["payload"]["hello"] = "evil"
    is_valid2, _ = validator.validate(tampered)
    assert is_valid2 is False, "Tampered event should fail signature/hash validation"
