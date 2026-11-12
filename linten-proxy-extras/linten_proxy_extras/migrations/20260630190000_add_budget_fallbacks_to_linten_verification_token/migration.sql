-- AlterTable
ALTER TABLE "Linten_VerificationToken" ADD COLUMN IF NOT EXISTS "budget_fallbacks" JSONB NOT NULL DEFAULT '{}';

-- AlterTable
ALTER TABLE "Linten_DeletedVerificationToken" ADD COLUMN IF NOT EXISTS "budget_fallbacks" JSONB NOT NULL DEFAULT '{}';
