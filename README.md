# Grappling-Skeleton-overlay

CLI for importing videos, managing a processing queue, displaying analysis progress,
and exporting summaries.

This repo ships with a lightweight, simulated analysis flow so it runs immediately
after download without any external model files.

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

## Application Skeleton Usage

Install the application skeleton in editable mode, then run the analyzer CLI:

```bash
pip install -e .
gso-analyze analyze --input /path/to/video.mp4 --output ./artifacts
```

The command will create `analysis.json`, `summary.txt`, and `metrics.json` in the
output directory as placeholder analysis artifacts.
