# Grappling-Skeleton-overlay

CLI for importing videos, managing a processing queue, displaying analysis progress,
and exporting summaries.

## Setup

```bash
pip install -r requirements.txt
```

## Usage

```bash
python -m gso.cli import /path/to/video.mp4
python -m gso.cli queue
python -m gso.cli process
python -m gso.cli export --format json --output analysis_summary.json
```
