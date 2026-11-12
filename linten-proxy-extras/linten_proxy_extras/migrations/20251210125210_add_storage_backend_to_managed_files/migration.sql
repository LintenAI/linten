-- AlterTable
ALTER TABLE "Linten_ManagedFileTable" ADD COLUMN IF NOT EXISTS "storage_backend" TEXT;
ALTER TABLE "Linten_ManagedFileTable" ADD COLUMN IF NOT EXISTS "storage_url" TEXT;

