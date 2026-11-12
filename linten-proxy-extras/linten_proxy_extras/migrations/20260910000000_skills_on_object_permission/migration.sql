ALTER TABLE "Linten_ObjectPermissionTable" ADD COLUMN IF NOT EXISTS "skills" TEXT[] DEFAULT ARRAY[]::TEXT[];
