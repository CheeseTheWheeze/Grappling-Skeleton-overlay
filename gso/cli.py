from __future__ import annotations

import json
import os
import sys
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

import typer

APP_DIR = Path.home() / ".gso"
QUEUE_FILE = APP_DIR / "queue.json"
SUMMARY_FILE = APP_DIR / "summaries.json"

app = typer.Typer(add_completion=False, help="Grappling Skeleton Overlay CLI.")


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


@app.command("import")
def import_video(path: Path) -> None:
    """Import a video file into the processing queue."""
    if not path.exists():
        raise typer.BadParameter(f"{path} does not exist.")
    _ensure_app_dir()
    queue = _load_queue()
    queue.append(QueueItem(path=str(path.resolve()), imported_at=_utc_now()))
    _save_queue(queue)
    typer.echo(f"Queued {path.name}. Queue length: {len(queue)}")


@app.command()
def queue() -> None:
    """List queued video files."""
    queue_items = _load_queue()
    if not queue_items:
        typer.echo("Queue is empty.")
        return
    for idx, item in enumerate(queue_items, start=1):
        typer.echo(f"{idx}. {item.path} (imported {item.imported_at})")


@app.command()
def process() -> None:
    """Process all queued video files."""
    queue_items = _load_queue()
    if not queue_items:
        typer.echo("Queue is empty.")
        return
    summaries = _load_summaries()
    typer.echo(f"Processing {len(queue_items)} video(s)...")
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
        typer.echo(f"Completed analysis for {path.name}.")
    _save_queue(queue_items)
    _save_summaries(summaries)
    typer.echo("All queued videos processed.")


@app.command()
def export(
    output: Path = typer.Option(
        Path("analysis_summary.json"),
        "--output",
        "-o",
        help="Output file path.",
    ),
    format: str = typer.Option("json", "--format", "-f", help="json or csv"),
) -> None:
    """Export analysis summaries."""
    summaries = _load_summaries()
    if not summaries:
        typer.echo("No summaries to export.")
        return
    output.parent.mkdir(parents=True, exist_ok=True)
    if format.lower() == "json":
        _save_json(output, [asdict(item) for item in summaries])
    elif format.lower() == "csv":
        lines = [
            "path,file_size_bytes,imported_at,processed_at,estimated_frames"
        ]
        for item in summaries:
            lines.append(
                f"{item.path},{item.file_size_bytes},{item.imported_at},"
                f"{item.processed_at},{item.estimated_frames}"
            )
        output.write_text("\n".join(lines))
    else:
        raise typer.BadParameter("Format must be json or csv.")
    typer.echo(f"Exported {len(summaries)} summaries to {output}.")


def run() -> None:
    app()


if __name__ == "__main__":
    run()
