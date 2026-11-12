-- AlterTable
ALTER TABLE "Linten_ManagedVectorStoresTable"
    ADD COLUMN IF NOT EXISTS "team_id" TEXT,
    ADD COLUMN IF NOT EXISTS "user_id" TEXT;

-- CreateIndex
CREATE INDEX IF NOT EXISTS "Linten_ManagedVectorStoresTable_team_id_idx"
    ON "Linten_ManagedVectorStoresTable"("team_id");

-- CreateIndex
CREATE INDEX IF NOT EXISTS "Linten_ManagedVectorStoresTable_user_id_idx"
    ON "Linten_ManagedVectorStoresTable"("user_id");

