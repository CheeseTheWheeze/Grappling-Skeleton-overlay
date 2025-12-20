# Pose Pipeline Design

## Overview
This document outlines the planned pipeline for extracting poses from video, normalizing skeletons, linking identities across frames and videos, clustering partner groups, and re-identifying limbs that leave the frame.

## Data Model (Core Fields)
| Field | Type | Description |
| --- | --- | --- |
| `video_id` | string | Unique identifier for a source video. |
| `frame_idx` | int | Zero-based frame index within a video. |
| `timestamp_ms` | int | Frame time in milliseconds. |
| `track_id` | string | Per-video persistent track for a person. |
| `skeleton_id` | string | Per-frame skeleton instance identifier. |
| `joint_positions` | map<string, [float, float, float]> | Joint name to normalized XYZ coordinates. |
| `joint_confidences` | map<string, float> | Joint name to confidence score. |
| `bbox_xywh` | [float, float, float, float] | Person bounding box in pixel space. |
| `camera_pose` | object | Optional camera metadata if known. |
| `partner_group_id` | string | Identifier for a paired/grouped interaction. |
| `limb_id` | string | Stable identifier for a limb segment within a track. |
| `embedding` | float[] | Re-ID embedding vector for a person or limb. |

## Stage 1: Pose Extraction
**Goal:** Detect people per frame and estimate their joint locations.

**Models:**
- **Primary:** Multi-person 2D pose model (e.g., YOLOv8-Pose, OpenPose, or MMPose HRNet)
- **Optional:** 3D lifting model (e.g., VideoPose3D) to estimate depth

**Inputs:**
- `video_id`
- Raw frames (RGB)

**Outputs:**
- `skeleton_id`
- `frame_idx`
- `bbox_xywh`
- `joint_positions` (pixel space)
- `joint_confidences`

**Notes:**
- When a 3D lifting model is used, `joint_positions` is stored as XYZ in camera space.
- Preserve per-joint confidence to inform later linking and re-ID steps.

## Stage 2: Per-Frame Skeleton Normalization
**Goal:** Normalize skeletons for scale, rotation, and translation to enable stable comparisons.

**Inputs:**
- `skeleton_id`
- `frame_idx`
- `joint_positions` (pixel or camera space)
- `joint_confidences`

**Outputs:**
- `skeleton_id`
- `frame_idx`
- `joint_positions` (normalized)
- `root_joint` (e.g., pelvis)
- `scale` (e.g., shoulder or hip distance)
- `orientation` (e.g., torso axis)

**Normalization Steps:**
1. Translate so `root_joint` is at origin.
2. Scale by torso length or hip-shoulder distance.
3. Rotate so torso axis aligns to a canonical forward direction.
4. Optionally mirror left/right if using a single canonical stance.

## Stage 3: Identity Linking Across Frames
**Goal:** Maintain stable `track_id` for each person within a video.

**Inputs:**
- `video_id`
- Per-frame skeletons
- `joint_positions` (normalized)
- `bbox_xywh`
- `embedding` (optional Re-ID for person appearance)

**Outputs:**
- `track_id`
- `skeleton_id` to `track_id` associations

**Linking Strategy:**
- Use motion models (e.g., Kalman filter) on root joint trajectories.
- Use IoU of `bbox_xywh` as a weak prior.
- Use pose similarity (joint distance in normalized space).
- Use optional appearance `embedding` for disambiguation in crossings.

## Stage 4: Identity Linking Across Videos
**Goal:** Match people across different videos for multi-session identity.

**Inputs:**
- `track_id`
- Track-level aggregates (pose signatures, appearance `embedding`, height scale)

**Outputs:**
- `global_person_id` (optional)
- Cross-video linkage table: (`video_id`, `track_id`) -> `global_person_id`

**Linking Strategy:**
- Aggregate per-track features: mean `embedding`, pose signature histogram, scale stats.
- Compare tracks using cosine distance for embeddings and pose-shape similarity.
- Enforce conservative thresholds to avoid false merges.

## Stage 5: Partner-Group Clustering
**Goal:** Identify interacting partners (e.g., grapplers) as groups.

**Inputs:**
- `track_id`
- `frame_idx`
- Root joint positions
- Bounding boxes and pose similarity

**Outputs:**
- `partner_group_id`
- Mapping of `track_id` to `partner_group_id`

**Clustering Logic:**
- Build adjacency graph based on proximity (root joint distance), overlap, and relative motion.
- Require sustained adjacency for N frames before establishing a group.
- Split groups when distance exceeds a threshold for M frames.
- Use pose-to-pose interaction features (e.g., hand-to-torso distance) to strengthen grouping.

## Stage 6: Limb Re-Identification (Occlusion Handling)
**Goal:** Persist limb identities when limbs leave and re-enter the frame.

**Inputs:**
- `track_id`
- Per-limb joint pairs (e.g., shoulder-elbow-wrist)
- `joint_positions` and `joint_confidences`
- Optional per-limb appearance `embedding`

**Outputs:**
- `limb_id` assignments per frame
- Limb continuity metadata (last seen frame, velocity)

**Re-ID Strategy:**
- Maintain per-limb state with last known pose, velocity, and confidence.
- When a limb is missing, propagate its state with a motion model and decrease confidence.
- When candidate joints reappear, assign the `limb_id` with minimal distance to predicted position.
- If ambiguity remains, use per-limb appearance `embedding` or kinematic constraints.

## Stage 7: Export / Persistence
**Goal:** Store and export structured results for downstream use.

**Inputs:**
- `video_id`, `frame_idx`, `skeleton_id`, `track_id`, `partner_group_id`, `limb_id`
- `joint_positions`, `joint_confidences`, `bbox_xywh`

**Outputs:**
- Table or JSONL rows with the full schema
- Optional summarized track-level metrics

**Suggested Record Schema (JSONL):**
```json
{
  "video_id": "match_001",
  "frame_idx": 1423,
  "timestamp_ms": 47433,
  "skeleton_id": "skel_0001423_03",
  "track_id": "track_03",
  "partner_group_id": "group_01",
  "limb_id": "track_03_left_arm",
  "joint_positions": {"left_shoulder": [0.1, 0.2, 0.0]},
  "joint_confidences": {"left_shoulder": 0.98},
  "bbox_xywh": [512.0, 204.0, 180.0, 360.0]
}
```
