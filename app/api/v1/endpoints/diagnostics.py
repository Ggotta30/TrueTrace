from fastapi import APIRouter

from app.engine.state.event_chain import get_all_events
from app.engine.validation.validator import EventValidator

router = APIRouter()
validator = EventValidator()


@router.get("/diagnostics")
def diagnostics():
    """
    Full-chain integrity diagnostics.
    - Hash validation
    - Signature validation
    - prev_hash linkage
    - Structure validation
    """

    events = get_all_events()
    issues = []
    last_hash = None

    for i, event in enumerate(events):
        event_id = event.get("event_id")
        prev_hash = event.get("prev_hash")

        # Run validator
        is_valid, result = validator.validate(event)

        event_issues = []

        if not is_valid:
            for err in result.get("errors", []):
                event_issues.append(err)

        # Chain linkage check
        if last_hash and prev_hash != last_hash:
            event_issues.append(
                f"chain_link_mismatch: expected prev_hash={last_hash}, got={prev_hash}"
            )

        # Missing required fields
        required = ["event_id", "event_type", "payload", "timestamp", "hash"]
        for req in required:
            if req not in event:
                event_issues.append(f"missing_field:{req}")

        # Attach the results
        if event_issues:
            issues.append(
                {
                    "index": i,
                    "event_id": event_id,
                    "issues": event_issues,
                    "computed_hash": result.get("computed_hash"),
                }
            )

        last_hash = result.get("computed_hash")

    status = "ok" if not issues else "issues_detected"

    return {
        "status": status,
        "event_count": len(events),
        "issues_found": len(issues),
        "details": issues,
    }
