-- AlterTable
ALTER TABLE "Linten_EndUserTable" ADD COLUMN IF NOT EXISTS "models" TEXT[] DEFAULT ARRAY[]::TEXT[];
