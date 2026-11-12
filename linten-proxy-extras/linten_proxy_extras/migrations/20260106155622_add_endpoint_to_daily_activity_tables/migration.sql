-- DropIndex
DROP INDEX IF EXISTS "Linten_DailyAgentSpend_agent_id_date_api_key_model_custom__key";

-- DropIndex
DROP INDEX IF EXISTS "Linten_DailyEndUserSpend_end_user_id_date_api_key_model_cu_key";

-- DropIndex
DROP INDEX IF EXISTS "Linten_DailyOrganizationSpend_organization_id_date_api_key_key";

-- DropIndex
DROP INDEX IF EXISTS "Linten_DailyTagSpend_tag_date_api_key_model_custom_llm_pro_key";

-- DropIndex
DROP INDEX IF EXISTS "Linten_DailyTeamSpend_team_id_date_api_key_model_custom_ll_key";

-- DropIndex
DROP INDEX IF EXISTS "Linten_DailyUserSpend_user_id_date_api_key_model_custom_ll_key";

-- AlterTable
ALTER TABLE "Linten_DailyAgentSpend" ADD COLUMN IF NOT EXISTS "endpoint" TEXT;

-- AlterTable
ALTER TABLE "Linten_DailyEndUserSpend" ADD COLUMN IF NOT EXISTS "endpoint" TEXT;

-- AlterTable
ALTER TABLE "Linten_DailyOrganizationSpend" ADD COLUMN IF NOT EXISTS "endpoint" TEXT;

-- AlterTable
ALTER TABLE "Linten_DailyTagSpend" ADD COLUMN IF NOT EXISTS "endpoint" TEXT;

-- AlterTable
ALTER TABLE "Linten_DailyTeamSpend" ADD COLUMN IF NOT EXISTS "endpoint" TEXT;

-- AlterTable
ALTER TABLE "Linten_DailyUserSpend" ADD COLUMN IF NOT EXISTS "endpoint" TEXT;

-- CreateIndex
CREATE INDEX IF NOT EXISTS "Linten_DailyAgentSpend_endpoint_idx" ON "Linten_DailyAgentSpend"("endpoint");

-- CreateIndex
CREATE UNIQUE INDEX IF NOT EXISTS "Linten_DailyAgentSpend_agent_id_date_api_key_model_custom__key" ON "Linten_DailyAgentSpend"("agent_id", "date", "api_key", "model", "custom_llm_provider", "mcp_namespaced_tool_name", "endpoint");

-- CreateIndex
CREATE INDEX IF NOT EXISTS "Linten_DailyEndUserSpend_endpoint_idx" ON "Linten_DailyEndUserSpend"("endpoint");

-- CreateIndex
CREATE UNIQUE INDEX IF NOT EXISTS "Linten_DailyEndUserSpend_end_user_id_date_api_key_model_cu_key" ON "Linten_DailyEndUserSpend"("end_user_id", "date", "api_key", "model", "custom_llm_provider", "mcp_namespaced_tool_name", "endpoint");

-- CreateIndex
CREATE INDEX IF NOT EXISTS "Linten_DailyOrganizationSpend_endpoint_idx" ON "Linten_DailyOrganizationSpend"("endpoint");

-- CreateIndex
CREATE UNIQUE INDEX IF NOT EXISTS "Linten_DailyOrganizationSpend_organization_id_date_api_key_key" ON "Linten_DailyOrganizationSpend"("organization_id", "date", "api_key", "model", "custom_llm_provider", "mcp_namespaced_tool_name", "endpoint");

-- CreateIndex
CREATE INDEX IF NOT EXISTS "Linten_DailyTagSpend_endpoint_idx" ON "Linten_DailyTagSpend"("endpoint");

-- CreateIndex
CREATE UNIQUE INDEX IF NOT EXISTS "Linten_DailyTagSpend_tag_date_api_key_model_custom_llm_pro_key" ON "Linten_DailyTagSpend"("tag", "date", "api_key", "model", "custom_llm_provider", "mcp_namespaced_tool_name", "endpoint");

-- CreateIndex
CREATE INDEX IF NOT EXISTS "Linten_DailyTeamSpend_endpoint_idx" ON "Linten_DailyTeamSpend"("endpoint");

-- CreateIndex
CREATE UNIQUE INDEX IF NOT EXISTS "Linten_DailyTeamSpend_team_id_date_api_key_model_custom_ll_key" ON "Linten_DailyTeamSpend"("team_id", "date", "api_key", "model", "custom_llm_provider", "mcp_namespaced_tool_name", "endpoint");

-- CreateIndex
CREATE INDEX IF NOT EXISTS "Linten_DailyUserSpend_endpoint_idx" ON "Linten_DailyUserSpend"("endpoint");

-- CreateIndex
CREATE UNIQUE INDEX IF NOT EXISTS "Linten_DailyUserSpend_user_id_date_api_key_model_custom_ll_key" ON "Linten_DailyUserSpend"("user_id", "date", "api_key", "model", "custom_llm_provider", "mcp_namespaced_tool_name", "endpoint");

