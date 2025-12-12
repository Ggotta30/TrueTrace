# app/api/v1/endpoints/events_verify.py

from typing import Any, Dict

from fastapi import APIRouter

from app.engine.state.event_chain import get_all_events
from app.engine.validation.validator import EventValidator

router = APIRouter()
validator = EventValidator()


@router.get("/verify")
def verify_all_events():
    """
    Verifies the entire event chain:
      - hash correctness
      - signature correctness
      - canonicalization integrity
    """

    chain = get_all_events()
    results = []

    for event in chain:
        is_valid, result = validator.validate(event)

        results.append(
            {
                "event_id": event.get("event_id"),
                "valid": is_valid,
                "errors": result.get("errors") if not is_valid else None,
                "computed_hash": result.get("computed_hash"),
            }
        )

    return {"count": len(results), "results": results}
