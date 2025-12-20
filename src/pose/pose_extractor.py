"""Pose extraction interfaces and stub implementations."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Protocol


@dataclass(frozen=True)
class SkeletonKeypoint:
    """Single keypoint extracted from a pose estimator."""

    name: str
    x_px: float
    y_px: float
    confidence: float
    visibility: float | None = None


@dataclass(frozen=True)
class FrameSkeleton:
    """Skeleton extracted for a single subject in a frame."""

    subject_id: str
    keypoints: tuple[SkeletonKeypoint, ...]


class PoseExtractor(Protocol):
    """Protocol for extracting skeletons from a single video frame."""

    def extract(self, image: object) -> Iterable[FrameSkeleton]:
        """Return skeletons detected in the provided frame image."""


@dataclass
class StubPoseExtractor:
    """Placeholder extractor that yields no skeletons."""

    def extract(self, image: object) -> Iterable[FrameSkeleton]:
        return ()
