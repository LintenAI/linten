-- AlterTable
ALTER TABLE "Linten_AgentsTable" ADD COLUMN IF NOT EXISTS "enabled" BOOLEAN NOT NULL DEFAULT true,
ADD COLUMN IF NOT EXISTS "execution_mode" TEXT NOT NULL DEFAULT 'autonomous',
ADD COLUMN IF NOT EXISTS "identity_managed" BOOLEAN NOT NULL DEFAULT false;

-- AlterTable
ALTER TABLE "Linten_SpendLogs" ADD COLUMN IF NOT EXISTS "billing_agent_id" TEXT;

-- CreateTable
CREATE TABLE IF NOT EXISTS "Linten_AgentIdentity" (
    "agent_id" TEXT NOT NULL,
    "active" BOOLEAN NOT NULL DEFAULT true,
    "provider" TEXT NOT NULL,
    "issuer" TEXT NOT NULL,
    "tenant_id" TEXT NOT NULL,
    "client_id" TEXT NOT NULL,
    "service_principal_id" TEXT,
    "required_roles" TEXT[] DEFAULT ARRAY[]::TEXT[],
    "required_scopes" TEXT[] DEFAULT ARRAY['user_impersonation']::TEXT[],
    "revision" TEXT NOT NULL,
    "last_authenticated_at" TIMESTAMP(3),

    CONSTRAINT "Linten_AgentIdentity_pkey" PRIMARY KEY ("agent_id")
);

-- CreateTable
CREATE TABLE IF NOT EXISTS "Linten_RetiredAgentIdentity" (
    "binding_id" TEXT NOT NULL,
    "agent_id" TEXT,
    "provider" TEXT NOT NULL,
    "issuer" TEXT NOT NULL,
    "tenant_id" TEXT NOT NULL,
    "client_id" TEXT NOT NULL,

    CONSTRAINT "Linten_RetiredAgentIdentity_pkey" PRIMARY KEY ("binding_id")
);

-- CreateTable
CREATE TABLE IF NOT EXISTS "Linten_RetiredAgent" (
    "original_agent_id" TEXT NOT NULL,
    "retired_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "Linten_RetiredAgent_pkey" PRIMARY KEY ("original_agent_id")
);

-- CreateTable
CREATE TABLE IF NOT EXISTS "Linten_VerifiedSubject" (
    "subject_id" TEXT NOT NULL,
    "issuer" TEXT NOT NULL,
    "tenant_id" TEXT NOT NULL,
    "oid" TEXT NOT NULL,
    "kind" TEXT NOT NULL DEFAULT 'human',
    "user_id" TEXT,
    "verified_via" TEXT NOT NULL DEFAULT 'sso_interactive',
    "verified_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "Linten_VerifiedSubject_pkey" PRIMARY KEY ("subject_id")
);

-- CreateIndex
CREATE UNIQUE INDEX IF NOT EXISTS "Linten_AgentIdentity_provider_tenant_id_client_id_key" ON "Linten_AgentIdentity"("provider", "tenant_id", "client_id");

-- CreateIndex
CREATE UNIQUE INDEX IF NOT EXISTS "Linten_AgentIdentity_issuer_service_principal_id_key" ON "Linten_AgentIdentity"("issuer", "service_principal_id");

-- CreateIndex
CREATE UNIQUE INDEX IF NOT EXISTS "Linten_RetiredAgentIdentity_provider_tenant_id_client_id_key" ON "Linten_RetiredAgentIdentity"("provider", "tenant_id", "client_id");

-- CreateIndex
CREATE INDEX IF NOT EXISTS "Linten_VerifiedSubject_user_id_idx" ON "Linten_VerifiedSubject"("user_id");

-- CreateIndex
CREATE UNIQUE INDEX IF NOT EXISTS "Linten_VerifiedSubject_issuer_tenant_id_oid_key" ON "Linten_VerifiedSubject"("issuer", "tenant_id", "oid");

-- AddForeignKey
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'Linten_AgentIdentity_agent_id_fkey') THEN
        ALTER TABLE "Linten_AgentIdentity" ADD CONSTRAINT "Linten_AgentIdentity_agent_id_fkey" FOREIGN KEY ("agent_id") REFERENCES "Linten_AgentsTable"("agent_id") ON DELETE CASCADE ON UPDATE CASCADE;
    END IF;
END $$;

-- AddForeignKey
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'Linten_RetiredAgentIdentity_agent_id_fkey') THEN
        ALTER TABLE "Linten_RetiredAgentIdentity" ADD CONSTRAINT "Linten_RetiredAgentIdentity_agent_id_fkey" FOREIGN KEY ("agent_id") REFERENCES "Linten_AgentsTable"("agent_id") ON DELETE SET NULL ON UPDATE CASCADE;
    END IF;
END $$;

-- AddForeignKey
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'Linten_VerifiedSubject_user_id_fkey') THEN
        ALTER TABLE "Linten_VerifiedSubject" ADD CONSTRAINT "Linten_VerifiedSubject_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "Linten_UserTable"("user_id") ON DELETE CASCADE ON UPDATE CASCADE;
    END IF;
END $$;
