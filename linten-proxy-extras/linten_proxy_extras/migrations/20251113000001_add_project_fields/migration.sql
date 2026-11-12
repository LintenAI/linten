-- AlterTable: Add new fields to Linten_ProjectTable
ALTER TABLE "Linten_ProjectTable" ADD COLUMN IF NOT EXISTS "description" TEXT;
ALTER TABLE "Linten_ProjectTable" ADD COLUMN IF NOT EXISTS "model_rpm_limit" JSONB NOT NULL DEFAULT '{}';
ALTER TABLE "Linten_ProjectTable" ADD COLUMN IF NOT EXISTS "model_tpm_limit" JSONB NOT NULL DEFAULT '{}';

