SET LOCAL lock_timeout = '10s';

CREATE TYPE "AccountingEventKind" AS ENUM ('inbound_usage', 'outbound_usage', 'cost');

CREATE TYPE "AccountingDeliveryState" AS ENUM ('pending', 'applied', 'parked');

CREATE TYPE "AccountingDeliveryTarget" AS ENUM ('Linten_VerificationToken', 'Linten_UserTable', 'Linten_TeamTable', 'Linten_TeamMembership', 'Linten_OrganizationTable', 'Linten_OrganizationMembership', 'Linten_EndUserTable', 'Linten_AgentsTable', 'Linten_TagTable', 'Linten_ProjectTable', 'Linten_ModelAccessGroupBudgetTable', 'Linten_BudgetTable', 'Linten_BudgetWindowSpend', 'Linten_DailyUserSpend', 'Linten_DailyTeamSpend', 'Linten_DailyOrganizationSpend', 'Linten_DailyEndUserSpend', 'Linten_DailyAgentSpend', 'Linten_DailyTagSpend', 'Linten_DailyModelUsage', 'Linten_DailyToolSpend', 'Linten_AutoRouterDailySpend');

-- CreateTable
CREATE TABLE IF NOT EXISTS "Linten_AccountingEvent" (
    "event_id" TEXT NOT NULL,
    "kind" "AccountingEventKind" NOT NULL,
    "source_event_id" TEXT,
    "schema_version" INTEGER NOT NULL,
    "payload_hash" TEXT NOT NULL,
    "occurred_at" TIMESTAMP(3) NOT NULL,
    "recorded_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "payload" JSONB NOT NULL,

    CONSTRAINT "Linten_AccountingEvent_schema_version_check" CHECK ("schema_version" > 0),
    CONSTRAINT "Linten_AccountingEvent_pkey" PRIMARY KEY ("event_id")
);

-- CreateTable
CREATE TABLE IF NOT EXISTS "Linten_AccountingDelivery" (
    "event_id" TEXT NOT NULL,
    "target" "AccountingDeliveryTarget" NOT NULL,
    "version" INTEGER NOT NULL,
    "state" "AccountingDeliveryState" NOT NULL DEFAULT 'pending',
    "attempts" INTEGER NOT NULL DEFAULT 0,
    "next_attempt_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "applied_at" TIMESTAMP(3),
    "last_error" TEXT,

    CONSTRAINT "Linten_AccountingDelivery_version_check" CHECK ("version" > 0),
    CONSTRAINT "Linten_AccountingDelivery_attempts_check" CHECK ("attempts" >= 0),
    CONSTRAINT "Linten_AccountingDelivery_pkey" PRIMARY KEY ("event_id","target","version")
);

-- CreateIndex
CREATE INDEX IF NOT EXISTS "Linten_AccountingEvent_recorded_at_idx" ON "Linten_AccountingEvent"("recorded_at");

-- CreateIndex
CREATE INDEX IF NOT EXISTS "Linten_AccountingEvent_kind_source_event_id_idx" ON "Linten_AccountingEvent"("kind", "source_event_id");

-- CreateIndex
CREATE INDEX IF NOT EXISTS "Linten_AccountingDelivery_target_state_next_attempt_at_idx" ON "Linten_AccountingDelivery"("target", "state", "next_attempt_at");
