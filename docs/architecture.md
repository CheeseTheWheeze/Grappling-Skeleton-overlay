# Architecture: Pose, Tracking, and Cross-Video Re-ID

## Decisions

### Pose Estimation: **MoveNet (Lightning/Thunder)**
**API**: TensorFlow Hub MoveNet SinglePose/Multipose (`movenet/singlepose/lightning`, `movenet/multipose/lightning`, `movenet/multipose/thunder`).

**Expected input**
- RGB frame (H×W×3), `uint8` or `float32` normalized depending on wrapper.
- Typical inference size: 192×192 (Lightning) or 256×256 (Thunder) for fast real-time use.

**Expected output**
- 17 keypoints per person (COCO format), each with `(y, x, score)`.
- Multipose returns up to N detections with keypoints + overall confidence.

**Tradeoffs**
- **Pros**: Fast, mobile-friendly, good real-time latency; well-supported TF Hub API.
- **Cons**: Slightly less accurate than heavier models (e.g., OpenPose/HRNet), especially for occlusion-heavy grappling positions.

### Tracking Layer: **ByteTrack**
**API**: ByteTrack in YOLOX or standalone integration (input: per-frame detections; output: track IDs).

**Expected input**
- Per-frame person detections with bounding boxes `(x1, y1, x2, y2)` and confidence scores.
- Optionally, per-detection features for track association.

**Expected output**
- Tracklets with stable `track_id`, updated per frame with bbox + confidence.

**Tradeoffs**
- **Pros**: Robust at linking high/low confidence detections, minimal parameter tuning; widely used with strong benchmarks.
- **Cons**: Requires reliable detector outputs; pure geometry association can drift during heavy occlusion unless aided by appearance cues.

### Cross-Video Re-ID Strategy: **Appearance Embeddings + Temporal/Context Filtering**
**API**: Person Re-ID model (e.g., OSNet or FastReID) to compute embeddings per track; cosine similarity for matching.

**Expected input**
- Cropped person images from tracks (bbox + frame), resized to the model’s expected size (e.g., 256×128).
- Optional context metadata (video timestamp, camera label, event info).

**Expected output**
- Fixed-length embedding vector per crop or per track (aggregated over frames).
- Cross-video match scores based on cosine similarity + metadata constraints.

**Tradeoffs**
- **Pros**: Works across different sessions/cameras; embeddings are compact and fast to compare; aggregation across frames improves stability.
- **Cons**: Accuracy drops with heavy occlusion, similar uniforms, or low-resolution crops; needs periodic re-calibration and hard-negative mining to avoid identity swaps.

## Expected Pipeline Data Flow
1. **Detect people** (detector) → bboxes + scores.
2. **Track** with ByteTrack → stable track IDs per video.
3. **Estimate pose** with MoveNet → 17 keypoints per person per frame.
4. **Compute Re-ID embeddings** per track → cross-video grouping using cosine similarity + metadata constraints.

## Notes
- If occlusion is frequent, consider switching MoveNet to a heavier model (e.g., OpenPose) or adding a pose smoothing step.
- For best Re-ID results, store multiple embeddings per track and use temporal attention (median or weighted mean) before matching across videos.
