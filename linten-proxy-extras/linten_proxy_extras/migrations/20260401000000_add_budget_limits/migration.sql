-- AlterTable: add budget_limits column to Linten_VerificationToken
ALTER TABLE "Linten_VerificationToken" ADD COLUMN IF NOT EXISTS "budget_limits" JSONB;

-- AlterTable: add budget_limits column to Linten_TeamTable
ALTER TABLE "Linten_TeamTable" ADD COLUMN IF NOT EXISTS "budget_limits" JSONB;
