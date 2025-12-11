import importlib
import pytest

@pytest.mark.unit
def test_validator_module_importable():
    """Validator module imports correctly."""
    mod = importlib.import_module("app.engine.validation.validator")
    assert hasattr(mod, "EventValidator")


@pytest.mark.unit
def test_signature_validation_smoke():
    """verify_signature should return a boolean even on malformed event."""
    sig = importlib.import_module("app.engine.validation.signature_validation")
    result = sig.verify_signature({"payload": {}})
    assert isinstance(result, bool)
