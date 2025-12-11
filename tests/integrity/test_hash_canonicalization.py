import pytest

def test_canonicalization_is_deterministic(helpers):
    """
    Ensure canonical_event_bytes gives the same bytes for semantically identical
    events with different key orders (determinism / canonical JSON).
    """
    hv = helpers["hash_validation"]
    pytest.importorskip("app.engine.validation.hash_validation")

    a = {
        "event_id": "evt-A",
        "payload": {"b": 2, "a": 1},
        "event_type": "t",
        "prev_hash": "",
        "origin": "t",
        "trace_id": "x",
        "timestamp": 1,
        "event_version": "1.5"
    }
    b = dict(reversed(list(a.items())))  # reorder keys

    fa = hv.filtered_for_hash(a)
    fb = hv.filtered_for_hash(b)

    ba = hv.canonical_event_bytes(fa)
    bb = hv.canonical_event_bytes(fb)

    assert ba == bb, "Canonical bytes should be identical irrespective of key order"
