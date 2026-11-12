-- AlterTable
ALTER TABLE "Linten_DailyUserSpend" ADD COLUMN IF NOT EXISTS "api_requests" INTEGER NOT NULL DEFAULT 0;

