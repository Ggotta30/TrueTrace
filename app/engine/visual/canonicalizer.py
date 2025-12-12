# app/engine/visual/canonicalizer.py
"""Video canonicalization utilities using Pillow (PIL).

Rules enforced here:
- normalize color space to RGB
- normalize resolution (configurable)
- remove audio (handled at ingestion)
- frame ordering deterministic
"""
from typing import Tuple

import numpy as np
from PIL import Image


def canonicalize_frame_bytes(
    frame_bytes: bytes,
    shape: Tuple[int, int, int],
    target_size: Tuple[int, int] = None,
) -> np.ndarray:
    """Convert raw frame bytes back to a canonical numpy array (H, W, 3), uint8.

    `shape` should be the original (H, W, C) of the frame bytes so we can reshape correctly.
    If target_size provided, resize using Lanczos for down/upscaling.
    """
    h, w, c = shape
    arr = np.frombuffer(frame_bytes, dtype=np.uint8).reshape((h, w, c))
    img = Image.fromarray(arr)

    if target_size:
        # Pillow expects (width, height)
        img = img.resize((target_size[1], target_size[0]), resample=Image.LANCZOS)

    out = np.ascontiguousarray(np.array(img.convert("RGB")), dtype=np.uint8)
    return out
