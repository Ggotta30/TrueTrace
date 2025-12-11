# app/api/v1/endpoints/events_chain.py

from fastapi import APIRouter
from app.engine.validation.validator import EventValidator
from app.engine.state.event_chain import get_all_events

router = APIRouter()
validator = EventValidator()


@router.get("/chain")
def read_chain():
    """
    Returns the full chain with validation status for each event.
    """

    chain = get_all_events()
    validated_chain = []

    for event in chain:
        is_valid, result = validator.validate(event)

        validated_chain.append({
            "event": event,
            "valid": is_valid,
            "errors": result.get("errors") if not is_valid else None,
            "computed_hash": result.get("computed_hash"),
        })

    return {"chain_length": len(validated_chain), "chain": validated_chain}
