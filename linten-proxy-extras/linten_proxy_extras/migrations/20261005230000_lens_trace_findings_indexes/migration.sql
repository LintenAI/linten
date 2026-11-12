CREATE INDEX CONCURRENTLY IF NOT EXISTS "Linten_LensRun_completed_executions_idx"
ON "Linten_LensRun" USING GIN ((data->'sample'->'executions') jsonb_path_ops)
WHERE data->>'status'='completed';
