"""Shared inference interface for pose tracking."""

from dataclasses import dataclass
from typing import Iterable, List, Sequence


@dataclass(frozen=True)
class Keypoint:
    name: str
    x: float
    y: float
    confidence: float


@dataclass(frozen=True)
class PoseFrame:
    frame_index: int
    keypoints: Sequence[Keypoint]


def run_inference(frames: Iterable[int]) -> List[PoseFrame]:
    """Run a placeholder inference pass over frame indices.

    Args:
        frames: Iterable of frame indices.

    Returns:
        List of PoseFrame results with mock keypoints.
    """
    results: List[PoseFrame] = []
    for frame_index in frames:
        results.append(PoseFrame(frame_index=frame_index, keypoints=_mock_keypoints(frame_index)))
    return results


def _mock_keypoints(frame_index: int) -> List[Keypoint]:
    """Generate stable mock keypoints for scaffolding."""
    base_x = 100.0 + (frame_index % 5) * 2.0
    base_y = 120.0 + (frame_index % 3) * 1.5
    return [
        Keypoint(name="head", x=base_x, y=base_y - 40.0, confidence=0.9),
        Keypoint(name="left_hand", x=base_x - 15.0, y=base_y, confidence=0.85),
        Keypoint(name="right_hand", x=base_x + 15.0, y=base_y, confidence=0.85),
        Keypoint(name="left_foot", x=base_x - 10.0, y=base_y + 60.0, confidence=0.8),
        Keypoint(name="right_foot", x=base_x + 10.0, y=base_y + 60.0, confidence=0.8),
    ]
