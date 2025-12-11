# app/engine/visual/frame_hashing.py
"""Frame hashing utilities used to create frame chains."""
import hashlib
from typing import Iterable, List


def hash_frame_bytes(frame_bytes: bytes) -> str:
    """Return SHA256 hex digest of frame bytes."""
    h = hashlib.sha256()
    h.update(frame_bytes)
    return h.hexdigest()


def build_frame_chain_hash(frame_hashes: Iterable[str]) -> str:
    """Compute an aggregate chain hash for a sequence of frame hex digests.

    We compute the running SHA256 by concatenating previous hash + current frame hash
    (simple and deterministic). This allows detection of dropped/inserted frames.
    """
    running = hashlib.sha256()
    for fh in frame_hashes:
        running.update(bytes.fromhex(fh))
    return running.hexdigest()


def hash_all_frames(frames: Iterable[bytes]) -> List[str]:
    """Hash many raw frames and return list of hex digests."""
    return [hash_frame_bytes(f) for f in frames]
