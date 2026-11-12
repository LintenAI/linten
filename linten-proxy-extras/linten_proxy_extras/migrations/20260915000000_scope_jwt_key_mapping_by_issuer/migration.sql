-- DropIndex
DROP INDEX IF EXISTS "Linten_JWTKeyMapping_jwt_claim_name_jwt_claim_value_is_act_idx";

-- DropIndex
DROP INDEX IF EXISTS "Linten_JWTKeyMapping_jwt_claim_name_jwt_claim_value_key";

-- AlterTable
-- NOT NULL DEFAULT '' (not nullable): Postgres unique constraints treat every
-- NULL as distinct, so a nullable column would let multiple unscoped mappings
-- collide on the same claim without a constraint violation. The constant
-- default is a fast, metadata-only backfill for existing rows, not a rewrite.
ALTER TABLE "Linten_JWTKeyMapping" ADD COLUMN IF NOT EXISTS "jwt_issuer" TEXT NOT NULL DEFAULT '';

-- CreateIndex
CREATE INDEX IF NOT EXISTS "Linten_JWTKeyMapping_jwt_issuer_jwt_claim_name_jwt_claim_v_idx" ON "Linten_JWTKeyMapping"("jwt_issuer", "jwt_claim_name", "jwt_claim_value", "is_active");

-- CreateIndex
CREATE UNIQUE INDEX IF NOT EXISTS "Linten_JWTKeyMapping_jwt_issuer_jwt_claim_name_jwt_claim_v_key" ON "Linten_JWTKeyMapping"("jwt_issuer", "jwt_claim_name", "jwt_claim_value");
