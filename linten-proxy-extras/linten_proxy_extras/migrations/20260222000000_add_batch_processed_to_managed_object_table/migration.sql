-- Add batch_processed column to Linten_ManagedObjectTable
-- Set to true by CheckBatchCost after cost has been computed for a completed batch
ALTER TABLE "Linten_ManagedObjectTable" ADD COLUMN IF NOT EXISTS "batch_processed" BOOLEAN NOT NULL DEFAULT false;
