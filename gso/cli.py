from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, List

APP_DIR = Path.home() / ".gso"
QUEUE_FILE = APP_DIR / "queue.json"
SUMMARY_FILE = APP_DIR / "summaries.json"


@dataclass
class QueueItem:
    path: str
    imported_at: str


@dataclass
class AnalysisSummary:
    path: str
    file_size_bytes: int
    imported_at: str
    processed_at: str
    estimated_frames: int


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _ensure_app_dir() -> None:
    APP_DIR.mkdir(parents=True, exist_ok=True)


def _load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text())


def _save_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2))


def _load_queue() -> List[QueueItem]:
    data = _load_json(QUEUE_FILE, [])
    return [QueueItem(**item) for item in data]


def _save_queue(items: List[QueueItem]) -> None:
    _save_json(QUEUE_FILE, [asdict(item) for item in items])


def _load_summaries() -> List[AnalysisSummary]:
    data = _load_json(SUMMARY_FILE, [])
    return [AnalysisSummary(**item) for item in data]


def _save_summaries(items: List[AnalysisSummary]) -> None:
    _save_json(SUMMARY_FILE, [asdict(item) for item in items])


def _print_progress(label: str, progress: int, total: int) -> None:
    percent = int((progress / total) * 100)
    bar_width = 30
    filled = int((percent / 100) * bar_width)
    bar = "#" * filled + "-" * (bar_width - filled)
    sys.stdout.write(f"\r{label} [{bar}] {percent:>3}%")
    sys.stdout.flush()
    if progress >= total:
        sys.stdout.write("\n")


def _import_video(path: Path) -> int:
    if not path.exists():
        print(f"Error: {path} does not exist.", file=sys.stderr)
        return 2
    _ensure_app_dir()
    queue = _load_queue()
    queue.append(QueueItem(path=str(path.resolve()), imported_at=_utc_now()))
    _save_queue(queue)
    print(f"Queued {path.name}. Queue length: {len(queue)}")
    return 0


def _show_queue() -> int:
    queue_items = _load_queue()
    if not queue_items:
        print("Queue is empty.")
        return 0
    for idx, item in enumerate(queue_items, start=1):
        print(f"{idx}. {item.path} (imported {item.imported_at})")
    return 0


def _process_queue() -> int:
    queue_items = _load_queue()
    if not queue_items:
        print("Queue is empty.")
        return 0
    summaries = _load_summaries()
    print(f"Processing {len(queue_items)} video(s)...")
    while queue_items:
        item = queue_items.pop(0)
        path = Path(item.path)
        file_size = path.stat().st_size if path.exists() else 0
        total_steps = 10
        for step in range(1, total_steps + 1):
            _print_progress(f"Analyzing {path.name}", step, total_steps)
            time.sleep(0.1)
        summary = AnalysisSummary(
            path=item.path,
            file_size_bytes=file_size,
            imported_at=item.imported_at,
            processed_at=_utc_now(),
            estimated_frames=max(1, file_size // 1024),
        )
        summaries.append(summary)
        print(f"Completed analysis for {path.name}.")
    _save_queue(queue_items)
    _save_summaries(summaries)
    print("All queued videos processed.")
    return 0


def _export_summaries(output: Path, format: str) -> int:
    summaries = _load_summaries()
    if not summaries:
        print("No summaries to export.")
        return 0
    output.parent.mkdir(parents=True, exist_ok=True)
    normalized = format.lower()
    if normalized == "json":
        _save_json(output, [asdict(item) for item in summaries])
    elif normalized == "csv":
        lines = ["path,file_size_bytes,imported_at,processed_at,estimated_frames"]
        for item in summaries:
            lines.append(
                f"{item.path},{item.file_size_bytes},{item.imported_at},"
                f"{item.processed_at},{item.estimated_frames}"
            )
        output.write_text("\n".join(lines))
    else:
        print("Error: format must be json or csv.", file=sys.stderr)
        return 2
    print(f"Exported {len(summaries)} summaries to {output}.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Grappling Skeleton Overlay CLI.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    import_parser = subparsers.add_parser(
        "import", help="Import a video file into the processing queue."
    )
    import_parser.add_argument("path", type=Path, help="Path to the video file.")

    subparsers.add_parser("queue", help="List queued video files.")
    subparsers.add_parser("process", help="Process all queued video files.")

    export_parser = subparsers.add_parser("export", help="Export analysis summaries.")
    export_parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=Path("analysis_summary.json"),
        help="Output file path.",
    )
    export_parser.add_argument(
        "--format",
        "-f",
        default="json",
        help="json or csv",
    )

    return parser


def main(argv: List[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "import":
        return _import_video(args.path)
    if args.command == "queue":
        return _show_queue()
    if args.command == "process":
        return _process_queue()
    if args.command == "export":
        return _export_summaries(args.output, args.format)

    parser.error("No command provided.")


if __name__ == "__main__":
    raise SystemExit(main())
