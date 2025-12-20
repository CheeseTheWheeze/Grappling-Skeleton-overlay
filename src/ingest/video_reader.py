"""Video reader interfaces for frame-level ingestion."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Iterator, Protocol, Sequence


@dataclass(frozen=True)
class VideoFrame:
    """Container for a decoded frame and timing metadata."""

    frame_index: int
    timestamp_ms: int
    image: object


class VideoReader(Protocol):
    """Protocol for iterating through frames of a video source."""

    def frames(self) -> Iterator[VideoFrame]:
        """Yield decoded frames in display order."""

    def frame_rate_fps(self) -> float:
        """Return the video frame rate."""

    def frame_count(self) -> int:
        """Return the total number of frames if known."""


@dataclass
class SequenceVideoReader:
    """Simple reader backed by an in-memory frame sequence.

    This stub is useful for wiring pipelines without a concrete decoder.
    """

    frames_sequence: Sequence[VideoFrame]
    fps: float

    def frames(self) -> Iterator[VideoFrame]:
        yield from self.frames_sequence

    def frame_rate_fps(self) -> float:
        return self.fps

    def frame_count(self) -> int:
        return len(self.frames_sequence)


@dataclass
class IterableVideoReader:
    """Reader backed by an iterable of frames when count is unknown."""

    frames_iterable: Iterable[VideoFrame]
    fps: float

    def frames(self) -> Iterator[VideoFrame]:
        return iter(self.frames_iterable)

    def frame_rate_fps(self) -> float:
        return self.fps

    def frame_count(self) -> int:
        raise NotImplementedError("Frame count is not available for this reader.")
