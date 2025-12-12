import json

from app.engine.state.event_chain import get_all_events
from app.engine.validation.validator import EventValidator


def run_cli_diagnostics():
    validator = EventValidator()
    events = get_all_events()

    print("\n=== TrueTrace Local Diagnostics ===\n")
    print(f"Loaded {len(events)} events\n")

    last_hash = None

    for i, event in enumerate(events):
        is_valid, result = validator.validate(event)
        event_id = event.get("event_id")
        prev_hash = event.get("prev_hash")

        print(f"[{i}] Event ID: {event_id}")

        if not is_valid:
            print("  ❌ Validation Errors:")
            for err in result["errors"]:
                print(f"     - {err}")
        else:
            print("  ✅ Valid")

        if last_hash and prev_hash != last_hash:
            print(f"  ❌ Chain linkage mismatch (expected prev_hash={last_hash})")

        print("")

        last_hash = result.get("computed_hash")

    print("=== End Diagnostics ===")
