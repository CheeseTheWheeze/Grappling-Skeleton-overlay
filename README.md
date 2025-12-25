# Grappling Skeleton Overlay - Clean Scaffold

This branch contains a clean, ground-up scaffold for a portable Windows app and a
future API service. It intentionally removes legacy code to provide a fresh
structure for the new model and training pipeline.

## Repository layout

- `core/` — model loading, inference, tracking, smoothing
- `adapters/` — video/file/API input adapters
- `apps/windows/` — Windows entrypoint and packaging hooks
- `apps/api/` — API wrapper (e.g., FastAPI) for inference
- `training/` — dataset registry and master model pipeline
- `packaging/` — build scripts for portable distributions
- `docs/` — documentation
- `scripts/` — automation scripts
- `tests/` — test suite
- `assets/` — static assets
- `models/` — model weights and metadata

## Day 1 goal

Establish a Windows-first prototype that uses the shared `core/` inference module
and prepare the API surface for future cross-platform usage.

## Quick start

```bash
python apps/windows/main.py
```

This generates `output/pose_tracks.json` using the placeholder inference core.
