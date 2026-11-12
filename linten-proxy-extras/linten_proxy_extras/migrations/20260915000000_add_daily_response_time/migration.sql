-- AlterTable
ALTER TABLE "Linten_DailyUserSpend" ADD COLUMN IF NOT EXISTS "total_response_time_ms" BIGINT NOT NULL DEFAULT 0;
ALTER TABLE "Linten_DailyUserSpend" ADD COLUMN IF NOT EXISTS "timed_requests" BIGINT NOT NULL DEFAULT 0;

-- AlterTable
ALTER TABLE "Linten_DailyOrganizationSpend" ADD COLUMN IF NOT EXISTS "total_response_time_ms" BIGINT NOT NULL DEFAULT 0;
ALTER TABLE "Linten_DailyOrganizationSpend" ADD COLUMN IF NOT EXISTS "timed_requests" BIGINT NOT NULL DEFAULT 0;

-- AlterTable
ALTER TABLE "Linten_DailyEndUserSpend" ADD COLUMN IF NOT EXISTS "total_response_time_ms" BIGINT NOT NULL DEFAULT 0;
ALTER TABLE "Linten_DailyEndUserSpend" ADD COLUMN IF NOT EXISTS "timed_requests" BIGINT NOT NULL DEFAULT 0;

-- AlterTable
ALTER TABLE "Linten_DailyAgentSpend" ADD COLUMN IF NOT EXISTS "total_response_time_ms" BIGINT NOT NULL DEFAULT 0;
ALTER TABLE "Linten_DailyAgentSpend" ADD COLUMN IF NOT EXISTS "timed_requests" BIGINT NOT NULL DEFAULT 0;

-- AlterTable
ALTER TABLE "Linten_DailyTeamSpend" ADD COLUMN IF NOT EXISTS "total_response_time_ms" BIGINT NOT NULL DEFAULT 0;
ALTER TABLE "Linten_DailyTeamSpend" ADD COLUMN IF NOT EXISTS "timed_requests" BIGINT NOT NULL DEFAULT 0;

-- AlterTable
ALTER TABLE "Linten_DailyTagSpend" ADD COLUMN IF NOT EXISTS "total_response_time_ms" BIGINT NOT NULL DEFAULT 0;
ALTER TABLE "Linten_DailyTagSpend" ADD COLUMN IF NOT EXISTS "timed_requests" BIGINT NOT NULL DEFAULT 0;
