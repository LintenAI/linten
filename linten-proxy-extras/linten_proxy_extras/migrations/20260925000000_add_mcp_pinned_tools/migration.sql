-- AlterTable
ALTER TABLE "Linten_MCPServerTable" ADD COLUMN IF NOT EXISTS "pinned_tools" JSONB DEFAULT '{}';
