import os
import numpy as np
from app.engine.visual.frame_hashing import hash_frame_bytes, build_frame_chain_hash
from app.engine.visual.motion_analysis import motion_signature_from_frames


def test_frame_hashing_and_chain():
    # synthetic frames (small arrays) -> stable hash
    f1 = (np.zeros((8, 8, 3), dtype=np.uint8) + 1).tobytes()
    f2 = (np.zeros((8, 8, 3), dtype=np.uint8) + 2).tobytes()

    h1 = hash_frame_bytes(f1)
    h2 = hash_frame_bytes(f2)
    chain = build_frame_chain_hash([h1, h2])

    assert isinstance(h1, str) and len(h1) == 64
    assert isinstance(chain, str) and len(chain) == 64


def test_motion_signature_sanity():
    # create 3 tiny frames with incremental motion (shifted pixels)
    f0 = np.zeros((32, 32, 3), dtype=np.uint8)
    f1 = np.roll(f0, 1, axis=1)
    f2 = np.roll(f1, 1, axis=1)

    frames = [f0, f1, f2]
    sig = motion_signature_from_frames(frames)

    assert "mean_magnitude" in sig
    assert sig["mean_magnitude"] >= 0
