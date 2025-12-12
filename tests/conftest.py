import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# Import the FastAPI app
try:
    from app.main import app
except Exception:
    import importlib
    import sys

    base = Path(__file__).resolve().parents[2]
    sys.path.append(str(base))
    app = importlib.import_module("app.main").app


@pytest.fixture(scope="session")
def client():
    return TestClient(app)
