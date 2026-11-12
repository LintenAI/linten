-- DropIndex
DROP INDEX IF EXISTS "Linten_DailyAgentSpend_agent_id_idx";

-- DropIndex
DROP INDEX IF EXISTS "Linten_DailyEndUserSpend_end_user_id_idx";

-- DropIndex
DROP INDEX IF EXISTS "Linten_DailyOrganizationSpend_organization_id_idx";

-- DropIndex
DROP INDEX IF EXISTS "Linten_DailyTagSpend_tag_idx";

-- DropIndex
DROP INDEX IF EXISTS "Linten_DailyTeamSpend_team_id_idx";

-- DropIndex
DROP INDEX IF EXISTS "Linten_DailyUserSpend_user_id_idx";

-- CreateIndex
CREATE INDEX IF NOT EXISTS "Linten_DailyAgentSpend_agent_id_date_idx" ON "Linten_DailyAgentSpend"("agent_id", "date");

-- CreateIndex
CREATE INDEX IF NOT EXISTS "Linten_DailyEndUserSpend_end_user_id_date_idx" ON "Linten_DailyEndUserSpend"("end_user_id", "date");

-- CreateIndex
CREATE INDEX IF NOT EXISTS "Linten_DailyOrganizationSpend_organization_id_date_idx" ON "Linten_DailyOrganizationSpend"("organization_id", "date");

-- CreateIndex
CREATE INDEX IF NOT EXISTS "Linten_DailyTagSpend_tag_date_idx" ON "Linten_DailyTagSpend"("tag", "date");

-- CreateIndex
CREATE INDEX IF NOT EXISTS "Linten_DailyTeamSpend_team_id_date_idx" ON "Linten_DailyTeamSpend"("team_id", "date");

-- CreateIndex
CREATE INDEX IF NOT EXISTS "Linten_DailyUserSpend_user_id_date_idx" ON "Linten_DailyUserSpend"("user_id", "date");

