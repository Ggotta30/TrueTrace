How to run the tests


1. From the repository root (where pytest.ini is located):


pytest -q


2. Run only integration tests:


pytest -q -m integration


3. If your app needs environment variables (DB path, keys), either set them
in your shell or update `tests/conftest.py` to monkeypatch the values before
the TestClient is created (see the tmp_db_path fixture example).


Notes
- The test suite is intentionally permissive for HTTP response shapes so it
can run against different states of the app. Tighten assertions to your
real API contract when you're ready.
- If your validator module exposes different function names, update
`tests/test_validation_components.py` accordingly.
