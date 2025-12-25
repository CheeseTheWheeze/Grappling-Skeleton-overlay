# Day 1 Next Steps

## Goal
Stand up a runnable Windows-first prototype that exercises the shared `core`
interface and writes placeholder pose tracks to disk.

## Steps
1. Run `python apps/windows/main.py` to generate `output/pose_tracks.json`.
2. Confirm the API wrapper can call the shared core via `apps/api/main.py`.
3. Expand the mock data generator with temporal smoothing once the baseline is in place.
