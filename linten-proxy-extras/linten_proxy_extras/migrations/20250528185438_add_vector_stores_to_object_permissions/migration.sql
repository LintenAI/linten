-- AlterTable
ALTER TABLE "Linten_ObjectPermissionTable" ADD COLUMN IF NOT EXISTS "vector_stores" TEXT[] DEFAULT ARRAY[]::TEXT[];

