# app/engine/visual/motion_analysis.py
"""Basic optical-flow based motion analysis using scikit-image.

This is intentionally a lightweight, dependency-friendly baseline. It produces
motion vectors and a simple motion signature useful for physics checks.
"""
import numpy as np
from typing import List, Dict
from skimage.color import rgb2gray
from skimage.registration import optical_flow_tvl1


def compute_dense_optical_flow(prev_frame: np.ndarray, next_frame: np.ndarray) -> np.ndarray:
    """Compute dense optical flow (TV-L1) between two RGB frames.

    Returns a float32 array shape (H, W, 2) containing flow vectors.
    """
    prev_gray = rgb2gray(prev_frame).astype("float32")
    next_gray = rgb2gray(next_frame).astype("float32")
    v, u = optical_flow_tvl1(prev_gray, next_gray)
    # optical_flow_tvl1 returns (v, u) where v is vertical, u is horizontal displacement
    flow = np.stack([u, v], axis=-1).astype("float32")
    return flow


def summarize_flow_magnitude(flow: np.ndarray) -> float:
    """Return a scalar summary of motion intensity (mean magnitude)."""
    mag = np.sqrt(flow[..., 0] ** 2 + flow[..., 1] ** 2)
    return float(np.mean(mag))


def motion_signature_from_frames(frames: List[np.ndarray]) -> Dict[str, float]:
    """Compute a lightweight motion signature for a sequence of frames.

    Output example:
    {"mean_magnitude": 1.2, "std_magnitude": 0.3, "peak": 4.5}
    """
    if not frames or len(frames) < 2:
        return {"mean_magnitude": 0.0, "std_magnitude": 0.0, "peak": 0.0}

    magnitudes = []
    for i in range(len(frames) - 1):
        prev = frames[i]
        nxt = frames[i + 1]
        flow = compute_dense_optical_flow(prev, nxt)
        mag = np.sqrt(flow[..., 0] ** 2 + flow[..., 1] ** 2)
        magnitudes.append(float(np.mean(mag)))

    mean = float(np.mean(magnitudes))
    std = float(np.std(magnitudes))
    peak = float(np.max(magnitudes))

    return {"mean_magnitude": mean, "std_magnitude": std, "peak": peak}
