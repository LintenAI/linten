SET LOCAL lock_timeout = '10s';

-- AlterTable
ALTER TABLE "Linten_AccessGroupTable" ADD COLUMN IF NOT EXISTS "mcp_tool_permissions" JSONB;
