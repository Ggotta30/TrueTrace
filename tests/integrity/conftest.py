import pytest
from nacl.signing import SigningKey
from pathlib import Path
import importlib

@pytest.fixture(scope="session")
def signing_key():
    """Ephemeral SigningKey for tests (Ed25519)."""
    return SigningKey.generate()

@pytest.fixture
def pubkey_hex(signing_key):
    return signing_key.verify_key.encode().hex()

@pytest.fixture
def sign_fn(signing_key):
    """Return a helper that signs canonical bytes and returns hex signature."""
    def _sign(msg_bytes: bytes) -> str:
        return signing_key.sign(msg_bytes).signature.hex()
    return _sign


@pytest.fixture
def helpers():
    """
    Try to import canonical/json/hash helpers from your validation package.
    Tests will gracefully skip if required functions are missing.
    """
    hv = importlib.import_module("app.engine.validation.hash_validation")
    sv = importlib.import_module("app.engine.validation.signature_validation")
    validator_mod = importlib.import_module("app.engine.validation.validator")
    return {
        "hash_validation": hv,
        "signature_validation": sv,
        "validator_mod": validator_mod,
    }
