-- AlterTable
ALTER TABLE "Linten_MCPServerTable" ADD COLUMN IF NOT EXISTS "oauth_passthrough" BOOLEAN NOT NULL DEFAULT false;
