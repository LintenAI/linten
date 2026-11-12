-- AlterTable
ALTER TABLE "Linten_MCPServerTable" ADD COLUMN IF NOT EXISTS "static_headers" JSONB DEFAULT '{}';
