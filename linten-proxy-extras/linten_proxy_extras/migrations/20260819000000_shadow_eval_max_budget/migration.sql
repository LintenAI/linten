-- AlterTable
ALTER TABLE "Linten_ShadowEvalJob" ADD COLUMN     "max_budget" DOUBLE PRECISION;

-- AlterTable
ALTER TABLE "Linten_ShadowEvalAttempt" ADD COLUMN     "shadow_cost" DOUBLE PRECISION NOT NULL DEFAULT 0;
