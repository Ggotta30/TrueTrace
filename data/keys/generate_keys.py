#!/usr/bin/env python3
# Generate ed25519 raw key files (requires pynacl)
try:
    from nacl.signing import SigningKey
except Exception as e:
    print("PyNaCl is required to generate keys. Install with: pip install pynacl")
    raise
sk = SigningKey.generate()
seed = sk._seed
pub = sk.verify_key._key
from pathlib import Path
p = Path(__file__).parent
(p / "truetrace_priv.bin").write_bytes(seed)
(p / "truetrace_pub.bin").write_bytes(pub)
print("Generated keys at:", p)
