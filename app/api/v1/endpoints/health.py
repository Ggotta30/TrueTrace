# app/api/v1/endpoints/health.py

from fastapi import APIRouter
from app.engine.state.event_chain import get_all_events
from app.engine.validation.validator import EventValidator

router = APIRouter()
validator = EventValidator()


@router.get("/")
def health_check():
    """
    Basic health check with a quick event integrity test.
    """
    chain = get_all_events()

    if not chain:
        return {"status": "ok", "message": "no events yet"}

    latest_event = chain[-1]
    is_valid, result = validator.validate(latest_event)

    if not is_valid:
        return {
            "status": "error",
            "message": "latest event failed validation",
            "errors": result.get("errors"),
            "computed_hash": result.get("computed_hash"),
        }

    return {"status": "ok", "message": "chain integrity valid"}
