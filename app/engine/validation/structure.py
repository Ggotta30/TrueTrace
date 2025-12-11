def validate_structure(event: dict):
    """
    Ensures the event contains required fields.
    Does not validate hash/signature formats.
    """
    errors = []

    required = ["event_id", "event_type", "payload", "timestamp"]
    for f in required:
        if f not in event:
            errors.append(f"missing_field:{f}")

    return (len(errors) == 0, errors)
