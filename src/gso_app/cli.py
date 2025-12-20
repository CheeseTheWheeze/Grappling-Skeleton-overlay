import argparse
import json
from pathlib import Path
from typing import Sequence


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Analyze a grappling video and write analysis artifacts.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    analyze_parser = subparsers.add_parser(
        "analyze",
        help="Analyze a video and produce output artifacts.",
    )
    analyze_parser.add_argument(
        "--input",
        required=True,
        help="Path to the input video file.",
    )
    analyze_parser.add_argument(
        "--output",
        required=True,
        help="Directory to write analysis artifacts.",
    )
    return parser


def analyze_video(input_path: Path, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    analysis_payload = {
        "input": str(input_path),
        "status": "queued",
        "artifacts": {
            "summary": str(output_dir / "summary.txt"),
            "metrics": str(output_dir / "metrics.json"),
        },
    }

    (output_dir / "summary.txt").write_text(
        "Analysis placeholder. Replace with real model output.\n",
        encoding="utf-8",
    )
    (output_dir / "metrics.json").write_text(
        json.dumps({"frames": 0, "detections": 0}, indent=2) + "\n",
        encoding="utf-8",
    )
    (output_dir / "analysis.json").write_text(
        json.dumps(analysis_payload, indent=2) + "\n",
        encoding="utf-8",
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "analyze":
        input_path = Path(args.input).expanduser().resolve()
        output_dir = Path(args.output).expanduser().resolve()
        if not input_path.exists():
            parser.error(f"Input video not found: {input_path}")
        analyze_video(input_path, output_dir)
        return 0

    parser.error("No command provided.")


if __name__ == "__main__":
    raise SystemExit(main())
