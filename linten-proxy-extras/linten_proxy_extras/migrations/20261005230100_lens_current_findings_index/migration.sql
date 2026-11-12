CREATE INDEX CONCURRENTLY IF NOT EXISTS "Linten_Lens_jobs_idx"
ON "Linten_Lens" USING GIN ((data->'jobs') jsonb_path_ops);
