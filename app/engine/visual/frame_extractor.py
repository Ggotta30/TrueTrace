# app/engine/visual/frame_extractor.py
"""Frame extraction utilities using imageio.

Primary responsibilities:
- open a video (file-like or path)
- normalize frame rate / timestamps (best-effort)
- yield canonical frames and timestamps
- graceful handling of variable framerate / corrupt frames
"""
from typing import Iterator, Tuple, Optional
import imageio
import numpy as np


def extract_frames(path: str, target_fps: Optional[float] = None) -> Iterator[Tuple[int, bytes]]:
    """Yield (frame_index, rgb_bytes) for each canonicalized frame.

    If target_fps is provided, frames are sampled/resampled to match (best-effort).
    Output frames are returned as raw RGB bytes (H x W x 3) in row-major order.
    """
    try:
        reader = imageio.get_reader(path)
    except Exception as e:
        raise FileNotFoundError(f"Unable to open video: {path} ({e})")

    meta = reader.get_meta_data() if hasattr(reader, "get_meta_data") else {}
    src_fps = float(meta.get("fps", 0) or 0)
    frame_idx = 0
    out_idx = 0

    # sample ratio (best-effort)
    if target_fps and src_fps > 0:
        step = max(1, int(round(src_fps / target_fps)))
    else:
        step = 1

    for frame in reader:
        # imageio delivers frames as HxWxC numpy arrays, usually RGB
        if frame_idx % step == 0:
            arr = np.asarray(frame)
            # ensure RGB (if RGBA, drop alpha)
            if arr.ndim == 3 and arr.shape[2] == 4:
                arr = arr[..., :3]
            if arr.ndim == 2:
                # grayscale -> convert to 3-channel
                arr = np.stack([arr, arr, arr], axis=-1)
            yield out_idx, arr.tobytes()
            out_idx += 1
        frame_idx += 1

    try:
        reader.close()
    except Exception:
        pass
