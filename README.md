TrueTrace - Clean Full Engine (generated)
=======================================

This package contains a clean, unified TrueTrace engine:
- canonical JSON canonicalization and hashing
- Ed25519 signing using raw 32-byte seed (tools/keys/truetrace_priv.bin)
- API endpoint: POST /api/v1/events/create
- Simple file-based chain storage: event_chain.json

To run:
  pip install -r requirements.txt
  uvicorn app.main:app --reload

Keys:
  tools/keys/truetrace_priv.bin  (32 bytes)
  tools/keys/truetrace_pub.bin   (32 bytes)

Use tools/keys/generate_keys.py to generate a proper keypair using PyNaCl if needed.
