-- Enable necessary extensions
create extension if not exists "pgvector" with schema "extensions";
create extension if not exists "pgcrypto" with schema "public";

-- Table to store information about processed videos
create table public.videos (
  id uuid primary key default gen_random_uuid(),
  youtube_id text not null unique,
  title text,
  duration_seconds float,
  created_at timestamptz default now(),
  status text default 'PENDING' -- e.g., PENDING, PROCESSING, COMPLETED, FAILED
);

-- Table to store video segments (transcript chunks) and their embeddings
create table public.segments (
  id uuid primary key default gen_random_uuid(),
  video_id uuid not null references public.videos(id) on delete cascade,
  start_time float not null,
  end_time float not null,
  text text,
  embedding vector(384), -- Dimension for sentence-transformers/all-MiniLM-L6-v2
  object_detections jsonb, -- Store detected objects for frames in this segment
  created_at timestamptz default now()
);

-- Create an index for efficient similarity search on embeddings
create index on public.segments using ivfflat (embedding vector_l2_ops) with (lists = 100);

-- Function to perform semantic search
create or replace function match_segments (
  query_embedding vector(384),
  match_threshold float,
  match_count int
)
returns table (
  id uuid,
  video_id uuid,
  text text,
  start_time float,
  similarity float
)
language sql stable
as $$
  select
    segments.id,
    segments.video_id,
    segments.text,
    segments.start_time,
    1 - (segments.embedding <=> query_embedding) as similarity
  from segments
  where 1 - (segments.embedding <=> query_embedding) > match_threshold
  order by similarity desc
  limit match_count;
$$;
