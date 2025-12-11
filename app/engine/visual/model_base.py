# app/engine/visual/model_base.py
"""Base classes and interfaces for future ML models (tamper detection, deepfake detection).

Keep this file lightweight: it defines the abstract API for pluggable models.
"""
from typing import Any, Dict


class BaseModel:
    """Abstract model interface for VPIE models."""

    def predict(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Run inference and return a dict of results."""
        raise NotImplementedError()


class DummyTamperModel(BaseModel):
    """A trivial placeholder model used during development and testing."""

    def predict(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        # returns a safe, neutral prediction
        return {"deepfake_probability": 0.01, "tamper_flags": []}
