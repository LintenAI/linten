-- AlterTable
ALTER TABLE "Linten_DeletedVerificationToken" ADD COLUMN IF NOT EXISTS "last_active" TIMESTAMP(3);

-- AlterTable
ALTER TABLE "Linten_VerificationToken" ADD COLUMN IF NOT EXISTS "last_active" TIMESTAMP(3);

