-- AlterTable
ALTER TABLE "Linten_MCPServerTable" ADD COLUMN IF NOT EXISTS "mcp_info" JSONB DEFAULT '{}';

