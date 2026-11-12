ALTER TABLE "Linten_ShadowEvalJob" ADD COLUMN IF NOT EXISTS "group_id" TEXT;

UPDATE "Linten_ShadowEvalJob" SET "group_id" = "id" WHERE "group_id" IS NULL;

ALTER TABLE "Linten_ShadowEvalJob" ALTER COLUMN "group_id" SET NOT NULL;

CREATE INDEX IF NOT EXISTS "Linten_ShadowEvalJob_group_id_idx" ON "Linten_ShadowEvalJob"("group_id");
