-- AlterTable
ALTER TABLE "Linten_ObjectPermissionTable" ADD COLUMN IF NOT EXISTS "models" TEXT[] DEFAULT ARRAY[]::TEXT[];

