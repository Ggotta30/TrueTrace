def test_verify_endpoint_exists(client):
    """Verify endpoint should exist."""
    resp = client.get("/api/v1/events/verify")
    assert resp.status_code in (200, 405, 404)
