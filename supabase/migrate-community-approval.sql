-- Mysterious: community approval system migration
-- Run this in Supabase Dashboard → SQL Editor

ALTER TABLE rooms ADD COLUMN IF NOT EXISTS requires_approval INT NOT NULL DEFAULT 0;

CREATE TABLE IF NOT EXISTS room_members(
  room_slug TEXT NOT NULL REFERENCES rooms(slug) ON DELETE CASCADE,
  user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  approved INT NOT NULL DEFAULT 0,
  requested_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  PRIMARY KEY(room_slug, user_id)
);

CREATE INDEX IF NOT EXISTS idx_room_members_pending ON room_members(room_slug, approved);
