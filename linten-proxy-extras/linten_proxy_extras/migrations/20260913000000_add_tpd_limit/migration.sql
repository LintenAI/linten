-- AlterTable
ALTER TABLE "Linten_BudgetTable" ADD COLUMN IF NOT EXISTS "tpd_limit" BIGINT;

-- AlterTable
ALTER TABLE "Linten_TeamTable" ADD COLUMN IF NOT EXISTS "tpd_limit" BIGINT;

-- AlterTable
ALTER TABLE "Linten_DeletedTeamTable" ADD COLUMN IF NOT EXISTS "tpd_limit" BIGINT;

-- AlterTable
ALTER TABLE "Linten_VerificationToken" ADD COLUMN IF NOT EXISTS "tpd_limit" BIGINT;

-- AlterTable
ALTER TABLE "Linten_DeletedVerificationToken" ADD COLUMN IF NOT EXISTS "tpd_limit" BIGINT;
