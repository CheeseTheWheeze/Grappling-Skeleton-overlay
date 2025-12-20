-- Schema for per-frame skeletons, tracking, and cross-video profiles.

CREATE TABLE videos (
  id UUID PRIMARY KEY,
  source_uri TEXT NOT NULL,
  file_name TEXT,
  codec TEXT,
  width INTEGER NOT NULL,
  height INTEGER NOT NULL,
  frame_rate REAL NOT NULL,
  duration_ms INTEGER,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE profiles (
  id UUID PRIMARY KEY,
  display_name TEXT,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tracks (
  id UUID PRIMARY KEY,
  video_id UUID NOT NULL REFERENCES videos(id),
  profile_id UUID REFERENCES profiles(id),
  track_label TEXT,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE frames (
  id UUID PRIMARY KEY,
  video_id UUID NOT NULL REFERENCES videos(id),
  frame_index INTEGER NOT NULL,
  timestamp_ms INTEGER NOT NULL,
  UNIQUE (video_id, frame_index)
);

CREATE TABLE skeletons (
  id UUID PRIMARY KEY,
  frame_id UUID NOT NULL REFERENCES frames(id),
  track_id UUID NOT NULL REFERENCES tracks(id),
  overall_confidence REAL,
  -- Flags for full-body visibility/occlusion in the frame.
  is_visible BOOLEAN NOT NULL DEFAULT TRUE,
  is_occluded BOOLEAN NOT NULL DEFAULT FALSE,
  UNIQUE (frame_id, track_id)
);

CREATE TABLE keypoints (
  id UUID PRIMARY KEY,
  skeleton_id UUID NOT NULL REFERENCES skeletons(id),
  name TEXT NOT NULL,
  x REAL NOT NULL,
  y REAL NOT NULL,
  z REAL,
  confidence REAL NOT NULL,
  is_visible BOOLEAN NOT NULL DEFAULT TRUE,
  is_occluded BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE limbs (
  id UUID PRIMARY KEY,
  skeleton_id UUID NOT NULL REFERENCES skeletons(id),
  name TEXT NOT NULL,
  start_keypoint TEXT NOT NULL,
  end_keypoint TEXT NOT NULL,
  visibility_score REAL,
  is_visible BOOLEAN NOT NULL DEFAULT TRUE,
  is_occluded BOOLEAN NOT NULL DEFAULT FALSE
);
