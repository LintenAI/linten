CREATE INDEX CONCURRENTLY IF NOT EXISTS "Linten_ManagedFileTable_created_by_created_at_idx"
ON "Linten_ManagedFileTable" ("created_by", "created_at" DESC);
