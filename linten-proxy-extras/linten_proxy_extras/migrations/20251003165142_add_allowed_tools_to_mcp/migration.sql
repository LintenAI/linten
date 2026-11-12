-- AlterTable
ALTER TABLE "Linten_MCPServerTable" ADD COLUMN IF NOT EXISTS "allowed_tools" TEXT[] DEFAULT ARRAY[]::TEXT[];

