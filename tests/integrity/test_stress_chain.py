import pytest
from copy import deepcopy

@pytest.mark.flaky
def test_mass_chain_sign_and_verify(helpers, sign_fn, pubkey_hex):
    """
    Stress test: generate N events, sign them and validate whole chain.
    Default N=200 for safety; increase locally if you want heavier stress.
    """
    hv = helpers["hash_validation"]
    validator_pkg = helpers["validator_mod"]
    Validator = getattr(validator_pkg, "EventValidator", None)
    pytest.importorskip("app.engine.validation.hash_validation")
    assert Validator is not None, "EventValidator missing"

    N = 200  # safe default; change to 1000 for heavier stress
    chain = []
    prev_hash = ""

    for i in range(N):
        evt = {
            "event_id": f"evt-stress-{i:06d}",
            "event_version": "1.5",
            "timestamp": 1600000000 + i,
            "event_type": "stress",
            "payload": {"i": i},
            "prev_hash": prev_hash,
            "origin": "stress-test",
            "trace_id": f"stress-{i}",
        }
        filtered = hv.filtered_for_hash(evt)
        canonical_bytes = hv.canonical_event_bytes(filtered)
        sig = sign_fn(canonical_bytes)
        evt["signature"] = sig
        evt["pubkey"] = pubkey_hex
        evt["hash"] = hv.compute_event_hash(evt)

        chain.append(evt)
        prev_hash = evt["hash"]

    validator = Validator()
    for e in chain:
        is_valid, result = validator.validate(deepcopy(e))
        assert is_valid is True, f"Chain event failed validation: {result}"
