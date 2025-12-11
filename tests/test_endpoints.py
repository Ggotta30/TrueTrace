def test_read_events_list(client):
    """Smoke test: list of events should not error."""
    resp = client.get("/api/v1/events/read")
    assert resp.status_code in (200, 204, 404)

    if resp.status_code == 200:
        j = resp.json()
        assert isinstance(j, (list, dict))
