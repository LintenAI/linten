-- Restore fields dropped by 20260311180521_schema_sync on Linten_MCPServerTable
-- AlterTable
ALTER TABLE "Linten_MCPServerTable"
  ADD COLUMN IF NOT EXISTS "source_url"       TEXT,
  ADD COLUMN IF NOT EXISTS "approval_status"  TEXT DEFAULT 'active',
  ADD COLUMN IF NOT EXISTS "submitted_by"     TEXT,
  ADD COLUMN IF NOT EXISTS "submitted_at"     TIMESTAMP(3),
  ADD COLUMN IF NOT EXISTS "reviewed_at"      TIMESTAMP(3),
  ADD COLUMN IF NOT EXISTS "review_notes"     TEXT;

-- CreateIndex
CREATE INDEX IF NOT EXISTS "Linten_MCPServerTable_approval_status_idx"
  ON "Linten_MCPServerTable"("approval_status");
