-- AlterTable
ALTER TABLE "Linten_OrganizationTable" ADD COLUMN IF NOT EXISTS "object_permission_id" TEXT;

-- AlterTable
ALTER TABLE "Linten_TeamTable" ADD COLUMN IF NOT EXISTS "object_permission_id" TEXT;

-- AlterTable
ALTER TABLE "Linten_UserTable" ADD COLUMN IF NOT EXISTS "object_permission_id" TEXT;

-- AlterTable
ALTER TABLE "Linten_VerificationToken" ADD COLUMN IF NOT EXISTS "object_permission_id" TEXT;

-- CreateTable
CREATE TABLE IF NOT EXISTS "Linten_ObjectPermissionTable" (
    "object_permission_id" TEXT NOT NULL,
    "mcp_servers" TEXT[] DEFAULT ARRAY[]::TEXT[],

    CONSTRAINT "Linten_ObjectPermissionTable_pkey" PRIMARY KEY ("object_permission_id")
);

-- AddForeignKey
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'Linten_OrganizationTable_object_permission_id_fkey') THEN
        ALTER TABLE "Linten_OrganizationTable" ADD CONSTRAINT "Linten_OrganizationTable_object_permission_id_fkey" FOREIGN KEY ("object_permission_id") REFERENCES "Linten_ObjectPermissionTable"("object_permission_id") ON DELETE SET NULL ON UPDATE CASCADE;
    END IF;
END $$;

-- AddForeignKey
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'Linten_TeamTable_object_permission_id_fkey') THEN
        ALTER TABLE "Linten_TeamTable" ADD CONSTRAINT "Linten_TeamTable_object_permission_id_fkey" FOREIGN KEY ("object_permission_id") REFERENCES "Linten_ObjectPermissionTable"("object_permission_id") ON DELETE SET NULL ON UPDATE CASCADE;
    END IF;
END $$;

-- AddForeignKey
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'Linten_UserTable_object_permission_id_fkey') THEN
        ALTER TABLE "Linten_UserTable" ADD CONSTRAINT "Linten_UserTable_object_permission_id_fkey" FOREIGN KEY ("object_permission_id") REFERENCES "Linten_ObjectPermissionTable"("object_permission_id") ON DELETE SET NULL ON UPDATE CASCADE;
    END IF;
END $$;

-- AddForeignKey
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'Linten_VerificationToken_object_permission_id_fkey') THEN
        ALTER TABLE "Linten_VerificationToken" ADD CONSTRAINT "Linten_VerificationToken_object_permission_id_fkey" FOREIGN KEY ("object_permission_id") REFERENCES "Linten_ObjectPermissionTable"("object_permission_id") ON DELETE SET NULL ON UPDATE CASCADE;
    END IF;
END $$;

