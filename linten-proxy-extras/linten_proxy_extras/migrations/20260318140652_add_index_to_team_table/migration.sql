-- CreateIndex
CREATE INDEX IF NOT EXISTS "Linten_TeamTable_organization_id_idx" ON "Linten_TeamTable"("organization_id");

-- CreateIndex
CREATE INDEX IF NOT EXISTS "Linten_TeamTable_team_alias_idx" ON "Linten_TeamTable"("team_alias");

-- CreateIndex
CREATE INDEX IF NOT EXISTS "Linten_TeamTable_created_at_idx" ON "Linten_TeamTable"("created_at");

