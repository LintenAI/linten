CREATE INDEX IF NOT EXISTS "Linten_LensWorker_active_scope_idx"
ON "Linten_LensWorker" USING GIN ((data->'scope') jsonb_path_ops)
WHERE data @> '{"revoked": false}'::jsonb;
