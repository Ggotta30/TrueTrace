from typing import Any, Dict, Tuple

from app.engine.validation.hash_validation import compute_event_hash
from app.engine.validation.signature_validation import verify_signature
from app.engine.validation.structure import validate_structure
from app.engine.validation.security_rules import run_security_rules


class EventValidator:
    """
    Central event validation engine.
    Performs:
    - Structure validation
    - Security rule enforcement
    - Hash computation
    - Signature validation
    """

    def validate(self, event: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        errors = []

        # -------------------------
        # STRUCTURE CHECKS
        # -------------------------
        struct_ok, struct_errors = validate_structure(event)
        if not struct_ok:
            errors.extend(struct_errors)

        # -------------------------
        # SECURITY RULES
        # -------------------------
        sec_ok, sec_errors = run_security_rules(event)
        if not sec_ok:
            errors.extend(sec_errors)

        # -------------------------
        # HASH CONSISTENCY
        # -------------------------
        computed_hash = compute_event_hash(event)
        stored_hash = event.get("hash")

        if stored_hash and stored_hash != computed_hash:
            errors.append(
                f"hash_mismatch: expected={computed_hash}, stored={stored_hash}"
            )

        # -------------------------
        # SIGNATURE VALIDATION
        # -------------------------
        sig_ok = verify_signature(event)
        if not sig_ok:
            errors.append("invalid_signature")

        # -------------------------
        # RESULT
        # -------------------------
        return (len(errors) == 0, {
            "errors": errors,
            "computed_hash": computed_hash
        })
