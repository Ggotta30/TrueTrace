import pytest

@pytest.mark.integration
def test_health_endpoint(client):
    """Health endpoint should respond 200 and a JSON body."""
    resp = client.get("/api/v1/health")
    assert resp.status_code == 200
    assert resp.headers["content-type"].startswith("application/json")
    j = resp.json()
    assert isinstance(j, dict)
    assert "status" in j


@pytest.mark.integration
def test_create_event_endpoint(client):
    """Create event should accept minimal valid payload."""
    sample_event = {
        "event_type": "test",
        "payload": {"message": "hello from test"}
    }

    resp = client.post("/api/v1/events/create", json=sample_event)

    # Should succeed with validated model
    assert resp.status_code in (200, 201, 202), resp.text

    j = resp.json()
    assert isinstance(j, dict)
    assert "status" in j
    assert "event" in j
    event = j["event"]
    assert "signature" in event
    assert "pubkey" in event
    assert "hash" in event
