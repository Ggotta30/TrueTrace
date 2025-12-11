import pytest
from copy import deepcopy

@pytest.mark.integration
def test_chain_continuity_and_prev_hash(helpers, sign_fn, pubkey_hex):
    """
    Build a small chain of 5 events using signed canonical bytes and prev_hash linking.
    Then verify each event and ensure continuity checks pass.
    """
    hv = helpers["hash_validation"]
    validator_pkg = helpers["validator_mod"]

    # ensure helpers exist (skip if not)
    pytest.importorskip("app.engine.validation.hash_validation")
    Validator = getattr(validator_pkg, "EventValidator", None)
    assert Validator is not None, "EventValidator missing"
    validator = Validator()

    # Create chain
    chain = []
    prev_hash = ""
    for i in range(5):
        evt = {
            "event_id": f"evt-test-{i:03d}",
            "event_version": "1.5",
            "timestamp": 1234000000 + i,
            "event_type": "batch",
            "payload": {"index": i},
            "prev_hash": prev_hash,
            "origin": "test",
            "trace_id": f"trace-{i}",
        }
        filtered = hv.filtered_for_hash(evt)
        canonical_bytes = hv.canonical_event_bytes(filtered)
        sig = sign_fn(canonical_bytes)
        evt["signature"] = sig
        evt["pubkey"] = pubkey_hex
        evt["hash"] = hv.compute_event_hash(evt)

        chain.append(evt)
        prev_hash = evt["hash"]

    # Validation: each event should validate, and prev_hash should match previous
    for idx, e in enumerate(chain):
        is_valid, result = validator.validate(deepcopy(e))
        assert is_valid is True, f"Event {idx} failed validation: {result}"

        if idx > 0:
            assert e["prev_hash"] == chain[idx - 1]["hash"], \
                "prev_hash mismatch in chain continuity test"

    # Insert an invalid event in the middle (tamper prev_hash) -> should break continuity
    bad_chain = deepcopy(chain)
    bad_chain[2]["prev_hash"] = "deadbeef"  # invalid link
    # The validator.validate on the third event should fail (depending on your validator's implementation)
    is_valid_bad, _ = validator.validate(deepcopy(bad_chain[2]))
    assert is_valid_bad is False, "Tampered prev_hash should cause validation failure"
