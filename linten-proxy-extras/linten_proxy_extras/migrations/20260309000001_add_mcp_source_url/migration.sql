-- AlterTable: Add source_url field to Linten_MCPServerTable for GitHub/docs link
ALTER TABLE "Linten_MCPServerTable"
  ADD COLUMN IF NOT EXISTS "source_url" TEXT;
