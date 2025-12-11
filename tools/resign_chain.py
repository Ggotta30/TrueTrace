import json
import os
import sys
from pathlib import Path

# ---------------------------------------------------------
# Ensure project root is in sys.path (so imports work when
# running directly from the tools/ directory)
# ---------------------------------------------------------
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Now safe to import app modules
from app.core.paths import CHAIN_FILE
from app.engine.validation.hash_validation import compute_event_hash, canonical_event_bytes
from app.engine.state.event_chain import get_all_events

# Keys
KEY_DIR = ROOT / "data" / "keys"
PRIV_KEY_FILE = KEY_DIR / "truetrace_priv.bin"



def load_private_key():
    """Load Ed25519 private key for signing."""
    import nacl.signing
    with open(PRIV_KEY_FILE, "rb") as f:
        return nacl.signing.SigningKey(f.read())


def resign_chain():
    print("\n=== TrueTrace Chain Re-Signer ===\n")

    events = get_all_events()
    print(f"Loaded {len(events)} events")

    if not events:
        print("No events found. Nothing to sign.")
        return

    priv_key = load_private_key()
    pubkey_hex = priv_key.verify_key.encode().hex()

    new_events = []
    prev_hash = None

    for idx, evt in enumerate(events):

        evt = dict(evt)  # make local copy

        # ---------------------------------------------------------
        # Remove prior volatile fields
        # ---------------------------------------------------------
        evt.pop("signature", None)
        evt.pop("hash", None)

        # Ensure pubkey is attached
        evt["pubkey"] = pubkey_hex

        # Apply prev_hash for chain linkage
        evt["prev_hash"] = prev_hash

        # ---------------------------------------------------------
        # Signing – MUST use canonical_event_bytes
        # ---------------------------------------------------------
        msg = canonical_event_bytes(evt)
        signature_hex = priv_key.sign(msg).signature.hex()
        evt["signature"] = signature_hex

        # ---------------------------------------------------------
        # Hashing – MUST use compute_event_hash
        # ---------------------------------------------------------
        new_hash = compute_event_hash(evt)
        evt["hash"] = new_hash

        # Forward-link
        prev_hash = new_hash

        new_events.append(evt)
        print(f"[{idx}] Resigned event {evt.get('event_id')}")

    # ---------------------------------------------------------
    # Backup original chain
    # ---------------------------------------------------------
    backup_path = CHAIN_FILE.with_suffix(".json.bak")

    if not backup_path.exists():
        os.rename(CHAIN_FILE, backup_path)
        print(f"\nBackup created: {backup_path}")
    else:
        print(f"\nBackup already exists at: {backup_path}")

    # ---------------------------------------------------------
    # Write updated chain
    # ---------------------------------------------------------
    with open(CHAIN_FILE, "w") as f:
        json.dump(new_events, f, indent=2)

    print("\n=== Re-Signing Complete ===")
    print(f"Updated chain saved to: {CHAIN_FILE}")
    print("Backup preserved.\n")


if __name__ == "__main__":
    resign_chain()
