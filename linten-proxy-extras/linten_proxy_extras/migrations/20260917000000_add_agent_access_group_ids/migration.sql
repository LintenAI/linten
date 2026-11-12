-- AlterTable
ALTER TABLE "Linten_AgentsTable" ADD COLUMN IF NOT EXISTS "access_group_ids" TEXT[] DEFAULT ARRAY[]::TEXT[];
