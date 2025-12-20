"""Serialization helpers for analysis exports."""
from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Iterable, Mapping

from matching.cross_video_identity import ProfileMap, ProfileMatch


@dataclass(frozen=True)
class SkeletonProfile:
    """Summary of a tracked subject that can span multiple videos."""

    profile_id: str
    source_video_id: str
    track_id: str
    similarity: float | None = None
    embedding: tuple[float, ...] | None = None

    @classmethod
    def from_match(cls, match: ProfileMatch) -> "SkeletonProfile":
        """Create a profile entry from a profile match."""

        return cls(
            profile_id=match.profile_id,
            source_video_id=match.source_video_id,
            track_id=match.track_id,
            similarity=match.similarity,
        )

    def to_dict(self) -> dict:
        payload = {
            "profile_id": self.profile_id,
            "source_video_id": self.source_video_id,
            "track_id": self.track_id,
        }
        if self.similarity is not None:
            payload["similarity"] = self.similarity
        if self.embedding is not None:
            payload["embedding"] = list(self.embedding)
        return payload


@dataclass(frozen=True)
class PartnerGroup:
    """Grouping metadata for interacting tracks."""

    partner_group_id: str
    track_ids: tuple[str, ...]
    metadata: Mapping[str, object] = field(default_factory=dict)

    def to_dict(self) -> dict:
        payload = {
            "partner_group_id": self.partner_group_id,
            "track_ids": list(self.track_ids),
        }
        if self.metadata:
            payload["metadata"] = dict(self.metadata)
        return payload


@dataclass(frozen=True)
class LimbTrack:
    """Stable limb identity assignment within a track."""

    limb_id: str
    track_id: str
    joint_names: tuple[str, ...]
    first_frame: int | None = None
    last_frame: int | None = None

    def to_dict(self) -> dict:
        payload = {
            "limb_id": self.limb_id,
            "track_id": self.track_id,
            "joint_names": list(self.joint_names),
        }
        if self.first_frame is not None:
            payload["first_frame"] = self.first_frame
        if self.last_frame is not None:
            payload["last_frame"] = self.last_frame
        return payload


@dataclass(frozen=True)
class ExportBundle:
    """Container for serialized analysis data."""

    profiles: tuple[SkeletonProfile, ...] = ()
    partner_groups: tuple[PartnerGroup, ...] = ()
    limb_tracks: tuple[LimbTrack, ...] = ()

    def to_dict(self) -> dict:
        return {
            "profiles": [profile.to_dict() for profile in self.profiles],
            "partner_groups": [group.to_dict() for group in self.partner_groups],
            "limb_tracks": [track.to_dict() for track in self.limb_tracks],
        }


def bundle_from_profile_map(
    profile_map: ProfileMap,
    partner_groups: Iterable[PartnerGroup] = (),
    limb_tracks: Iterable[LimbTrack] = (),
) -> ExportBundle:
    """Create an export bundle from an existing profile map."""

    profiles = tuple(SkeletonProfile.from_match(match) for match in profile_map.profiles)
    return ExportBundle(
        profiles=profiles,
        partner_groups=tuple(partner_groups),
        limb_tracks=tuple(limb_tracks),
    )


def export_bundle(bundle: ExportBundle, path: str | Path) -> Path:
    """Write an export bundle to disk as JSON."""

    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.suffix != ".json":
        raise ValueError(f"Unsupported export format: {destination.suffix}")
    destination.write_text(json.dumps(bundle.to_dict(), indent=2))
    return destination
