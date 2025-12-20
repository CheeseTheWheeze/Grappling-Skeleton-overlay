# Export Definitions

## Overview
This document defines the export formats for:
- **Data files** (CSV and JSON).
- **Overlay video** rendering.
- **Summarized report** output (partner groups, limb tracking stability, and per-video stats).

---

## CSV Export

**Filename:** `session_<session_id>_tracking.csv`

**Encoding:** UTF-8, comma-separated, header row required.

**Row Grain:** One row per tracked keypoint per frame per subject.

| Column | Type | Required | Description |
| --- | --- | --- | --- |
| session_id | string | yes | Unique session identifier. |
| video_id | string | yes | Unique video identifier. |
| frame_index | integer | yes | Zero-based frame index. |
| timestamp_ms | integer | yes | Frame timestamp in milliseconds. |
| subject_id | string | yes | Stable identifier for each tracked subject. |
| partner_group_id | string | no | Stable identifier for paired/partner grouping (if applicable). |
| keypoint_name | string | yes | Anatomical keypoint name (e.g., `left_wrist`). |
| x_px | float | yes | X coordinate in pixel space. |
| y_px | float | yes | Y coordinate in pixel space. |
| confidence | float | yes | Model confidence score in 0–1. |
| visibility | float | no | Visibility score (if supported by the model). |
| limb_id | string | no | Optional limb identifier mapping a keypoint to a limb. |
| limb_state | string | no | Optional state label (e.g., `stable`, `occluded`). |

**Notes**
- If a keypoint is not detected for a frame, omit the row for that keypoint/frame combination.
- `partner_group_id` is optional but should be consistent across frames when available.

---

## JSON Export

**Filename:** `session_<session_id>_tracking.json`

**Structure:**
```json
{
  "session_id": "string",
  "video_id": "string",
  "frame_rate_fps": 30,
  "frame_count": 12345,
  "subjects": [
    {
      "subject_id": "string",
      "partner_group_id": "string or null",
      "keypoints": {
        "left_wrist": [
          { "frame_index": 0, "x_px": 12.3, "y_px": 45.6, "confidence": 0.92 },
          { "frame_index": 1, "x_px": 12.8, "y_px": 45.1, "confidence": 0.90 }
        ]
      }
    }
  ],
  "summary": {
    "partner_groups": [
      { "partner_group_id": "A", "subject_ids": ["s1", "s2"] }
    ],
    "limb_tracking_stability": [
      {
        "subject_id": "s1",
        "limb_id": "left_arm",
        "stability_score": 0.88,
        "unstable_frame_ratio": 0.06
      }
    ],
    "per_video_stats": {
      "mean_confidence": 0.91,
      "missing_keypoint_ratio": 0.03,
      "occluded_frame_ratio": 0.05
    }
  }
}
```

**Notes**
- `summary` is optional but recommended to keep JSON export self-contained.
- Use consistent `subject_id` and `partner_group_id` across all outputs.

---

## Overlay Video Export

**Filename:** `session_<session_id>_overlay.mp4`

**Container/Codec:** MP4 / H.264 (baseline or main profile).

**Resolution:** Match input video.

**Frame Rate:** Match input video.

**Overlay Elements:**
- Skeleton lines and keypoints, colored per subject.
- Optional limb stability indicators (e.g., green=stable, yellow=low confidence, red=occluded).
- Optional partner group indicator (e.g., shared color ring or label).

**Metadata (Sidecar JSON):**
- `session_<session_id>_overlay_metadata.json` containing render settings:
  - `line_thickness_px`
  - `keypoint_radius_px`
  - `subject_color_map`
  - `stability_thresholds`

---

## Summarized Report

**Filename:** `session_<session_id>_summary.json`

**Structure:**
```json
{
  "session_id": "string",
  "video_id": "string",
  "generated_at": "ISO-8601 timestamp",
  "partner_groups": [
    {
      "partner_group_id": "string",
      "subject_ids": ["s1", "s2"],
      "overlap_duration_ms": 123456,
      "mean_distance_px": 42.7
    }
  ],
  "limb_tracking_stability": [
    {
      "subject_id": "s1",
      "limb_id": "left_arm",
      "stability_score": 0.88,
      "unstable_frame_ratio": 0.06,
      "mean_confidence": 0.91
    }
  ],
  "per_video_stats": {
    "frame_count": 12345,
    "duration_ms": 411500,
    "mean_confidence": 0.91,
    "missing_keypoint_ratio": 0.03,
    "occluded_frame_ratio": 0.05,
    "active_subject_count": 2
  }
}
```

**Metric Definitions**
- **stability_score:** 1 - (unstable_frame_ratio), optional smoothing allowed.
- **unstable_frame_ratio:** Proportion of frames where limb confidence is below threshold or keypoints missing.
- **missing_keypoint_ratio:** Total missing keypoints / total expected keypoints.
- **occluded_frame_ratio:** Frames where any keypoint is marked occluded / total frames.

---

## Validation Requirements
- `frame_index` must be within `[0, frame_count-1]`.
- `confidence` must be in `[0, 1]`.
- `partner_group_id` must be stable for the same paired subjects across a session.
- `subject_id` must be stable across all exports.
