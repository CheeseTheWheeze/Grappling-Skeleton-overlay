"""API scaffold for the shared inference core.

This module intentionally avoids framework dependencies for now. It defines the
expected integration surface for a future FastAPI (or similar) app.
"""

from typing import Iterable, List

from core.inference import PoseFrame, run_inference


def run_inference_for_frames(frames: Iterable[int]) -> List[PoseFrame]:
    """Wrapper used by future API routes."""
    return run_inference(frames)
