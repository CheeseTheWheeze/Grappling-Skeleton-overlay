"""Skeleton tracking interfaces for within-video association."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Protocol

from pose.pose_extractor import FrameSkeleton


@dataclass(frozen=True)
class FrameDetections:
    """Skeletons detected in a single video frame before tracking."""

    frame_index: int
    timestamp_ms: int
    skeletons: tuple[FrameSkeleton, ...]


@dataclass(frozen=True)
class TrackedSkeleton:
    """Skeleton with a stable within-video identity."""

    track_id: str
    skeleton: FrameSkeleton


@dataclass(frozen=True)
class TrackedFrame:
    """Collection of tracked skeletons for a frame."""

    frame_index: int
    timestamp_ms: int
    tracked: tuple[TrackedSkeleton, ...]


class SkeletonTracker(Protocol):
    """Protocol for associating skeletons across frames in one video."""

    def track(self, frames: Iterable[FrameDetections]) -> Iterable[TrackedFrame]:
        """Return tracked frames with stable track IDs."""


@dataclass
class PassThroughSkeletonTracker:
    """Stub tracker that preserves incoming identities."""

    def track(self, frames: Iterable[FrameDetections]) -> Iterable[TrackedFrame]:
        return (
            TrackedFrame(
                frame_index=frame.frame_index,
                timestamp_ms=frame.timestamp_ms,
                tracked=tuple(
                    TrackedSkeleton(track_id=skeleton.subject_id, skeleton=skeleton)
                    for skeleton in frame.skeletons
                ),
            )
            for frame in frames
        )
