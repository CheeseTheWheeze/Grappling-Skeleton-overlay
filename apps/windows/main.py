"""Windows-first entrypoint for the scaffolded prototype."""

import json
from pathlib import Path

from core.inference import run_inference


def main() -> int:
    repo_root = Path(__file__).resolve().parents[2]
    output_path = repo_root / "output"
    output_path.mkdir(exist_ok=True)
    frames = range(0, 30)
    pose_frames = run_inference(frames)
    serialized = [
        {
            "frame_index": frame.frame_index,
            "keypoints": [
                {
                    "name": keypoint.name,
                    "x": keypoint.x,
                    "y": keypoint.y,
                    "confidence": keypoint.confidence,
                }
                for keypoint in frame.keypoints
            ],
        }
        for frame in pose_frames
    ]
    output_file = output_path / "pose_tracks.json"
    output_file.write_text(json.dumps(serialized, indent=2))
    print(f"Wrote pose tracks to {output_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
