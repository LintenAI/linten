-- Add api_key and request_tags columns to Linten_ManagedObjectTable
-- Captured at batch-create time so CheckBatchCost can attribute batch-cost spend
-- back to the creating virtual key (and its tags) even when created_by is null.
ALTER TABLE "Linten_ManagedObjectTable" ADD COLUMN IF NOT EXISTS "api_key" TEXT;
ALTER TABLE "Linten_ManagedObjectTable" ADD COLUMN IF NOT EXISTS "request_tags" JSONB DEFAULT '[]';
