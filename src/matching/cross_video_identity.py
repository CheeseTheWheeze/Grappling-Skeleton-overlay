"""Cross-video identity matching and profile export utilities."""
from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Iterable, Protocol

from tracking.skeleton_tracker import TrackedFrame


@dataclass(frozen=True)
class ProfileEmbedding:
    """Compact representation of a subject across a video."""

    profile_id: str
    embedding: tuple[float, ...]
    source_video_id: str
    track_id: str


@dataclass(frozen=True)
class ProfileMatch:
    """Mapping from a video-specific track to a global profile."""

    profile_id: str
    source_video_id: str
    track_id: str
    similarity: float


@dataclass(frozen=True)
class ProfileMap:
    """Cross-video profile assignments."""

    profiles: tuple[ProfileMatch, ...]

    def to_dict(self) -> dict:
        return {
            "profiles": [
                {
                    "profile_id": match.profile_id,
                    "source_video_id": match.source_video_id,
                    "track_id": match.track_id,
                    "similarity": match.similarity,
                }
                for match in self.profiles
            ]
        }


class CrossVideoIdentityBuilder(Protocol):
    """Protocol for building cross-video profile embeddings and matches."""

    def build_embeddings(
        self, video_id: str, tracked_frames: Iterable[TrackedFrame]
    ) -> Iterable[ProfileEmbedding]:
        """Build per-subject embeddings for a single video."""

    def match_profiles(
        self, embeddings: Iterable[ProfileEmbedding]
    ) -> ProfileMap:
        """Resolve embeddings into a global profile map."""


@dataclass
class StubCrossVideoIdentityBuilder:
    """Placeholder matcher that assigns deterministic profile IDs."""

    def build_embeddings(
        self, video_id: str, tracked_frames: Iterable[TrackedFrame]
    ) -> Iterable[ProfileEmbedding]:
        seen: set[str] = set()
        for frame in tracked_frames:
            for tracked in frame.tracked:
                if tracked.track_id in seen:
                    continue
                seen.add(tracked.track_id)
                yield ProfileEmbedding(
                    profile_id=f"{video_id}:{tracked.track_id}",
                    embedding=(),
                    source_video_id=video_id,
                    track_id=tracked.track_id,
                )

    def match_profiles(
        self, embeddings: Iterable[ProfileEmbedding]
    ) -> ProfileMap:
        matches = tuple(
            ProfileMatch(
                profile_id=embedding.profile_id,
                source_video_id=embedding.source_video_id,
                track_id=embedding.track_id,
                similarity=1.0,
            )
            for embedding in embeddings
        )
        return ProfileMap(profiles=matches)


def export_profile_map(profile_map: ProfileMap, path: str | Path) -> Path:
    """Export a profile map to JSON or Parquet, based on file suffix."""

    destination = Path(path)
    if destination.suffix == ".json":
        destination.write_text(json.dumps(profile_map.to_dict(), indent=2))
        return destination

    if destination.suffix == ".parquet":
        try:
            import pyarrow as pa
            import pyarrow.parquet as pq
        except ModuleNotFoundError as exc:
            raise RuntimeError(
                "pyarrow is required to export profile maps to Parquet"
            ) from exc

        table = pa.Table.from_pylist(profile_map.to_dict()["profiles"])
        pq.write_table(table, destination)
        return destination

    raise ValueError(f"Unsupported export format: {destination.suffix}")
