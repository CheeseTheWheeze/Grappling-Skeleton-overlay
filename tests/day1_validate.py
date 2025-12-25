"""Validate Day-1 output schema for the Windows entrypoint."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    output_file = repo_root / "output" / "pose_tracks.json"

    if not output_file.exists():
        print(f"Missing output file: {output_file}")
        return 1

    try:
        payload = json.loads(output_file.read_text())
    except json.JSONDecodeError as exc:
        print(f"Invalid JSON in {output_file}: {exc}")
        return 1

    if not isinstance(payload, list) or not payload:
        print("Output JSON must be a non-empty list of frames.")
        return 1

    for index, frame in enumerate(payload):
        if not isinstance(frame, dict):
            print(f"Frame {index} is not an object.")
            return 1

        if "frame_index" not in frame:
            print(f"Frame {index} missing frame_index.")
            return 1

        keypoints = frame.get("keypoints")
        if not isinstance(keypoints, list) or not keypoints:
            print(f"Frame {index} keypoints must be a non-empty list.")
            return 1

        for point_index, keypoint in enumerate(keypoints):
            if not isinstance(keypoint, dict):
                print(f"Frame {index} keypoint {point_index} is not an object.")
                return 1

            missing_fields = [
                field
                for field in ("name", "x", "y", "confidence")
                if field not in keypoint
            ]
            if missing_fields:
                print(
                    "Frame "
                    f"{index} keypoint {point_index} missing fields: "
                    f"{', '.join(missing_fields)}"
                )
                return 1

    print(f"Day-1 output validation passed: {output_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
