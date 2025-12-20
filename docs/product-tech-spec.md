# Grappling Skeleton Overlay: Product/Tech Spec (Short)

## Overview
A lightweight tool that ingests grappling videos and produces pose-based analytics artifacts (profile maps, partner group IDs, limb tracks). The primary goal is to streamline athlete/coaching review by turning raw video into structured motion data and overlays.

## Supported OS Targets
- **Desktop**: macOS 12+, Windows 10/11, Ubuntu 20.04+
- **GPU acceleration (optional)**: NVIDIA CUDA-capable GPUs on Windows/Linux

## Input Formats
- **Video**: MP4 (H.264/H.265), MOV (H.264/H.265), MKV (H.264/H.265)
- **Resolution**: 720p minimum; 1080p+ recommended
- **Frame rate**: 24–60 FPS

## Expected Outputs
- **Profile maps**
  - Per-athlete pose heatmaps over time (joint occupancy and movement density)
  - Exported as PNG (preview) + JSON (data)
- **Partner group IDs**
  - Track-level identifiers that associate each detected person to a stable ID across frames
  - Exported as JSON/CSV
- **Limb tracks**
  - Joint trajectories with timestamps (e.g., wrists, elbows, knees, ankles)
  - Exported as JSON/CSV
- **Optional overlay video**
  - Pose skeletons and IDs composited on original video (MP4)

## Key User Flows
1. **Import videos**
   - Drag-and-drop or file picker
   - Validate format, resolution, and duration
2. **Process**
   - Pose detection + tracking
   - Auto-association of partners (group IDs)
   - Generate outputs (profile maps, limb tracks)
3. **Review results**
   - Timeline scrubber with overlay preview
   - Toggle per-person overlays and joint paths
4. **Export**
   - Export data artifacts (JSON/CSV)
   - Export overlay video (MP4)

## MVP Scope
- **Single-person tracking only**
  - Focus on high-quality pose detection and limb tracking for one athlete
  - Output profile maps + limb tracks (no partner group IDs)
- **Manual person selection**
  - User chooses a single subject from the first frame
- **Basic review UI**
  - Playback, pause, frame scrub
  - Overlay on/off
- **Exports**
  - JSON for limb tracks, PNG/JSON for profile maps

## Post-MVP (Out of Scope)
- Multi-person tracking and automatic partner association
- Real-time processing
- Cloud sync and team sharing
- Advanced analytics (e.g., technique classification)
