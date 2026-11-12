-- CreateIndex
CREATE INDEX IF NOT EXISTS "Linten_VerificationToken_user_id_team_id_idx" ON "Linten_VerificationToken"("user_id", "team_id");

-- CreateIndex
CREATE INDEX IF NOT EXISTS "Linten_VerificationToken_team_id_idx" ON "Linten_VerificationToken"("team_id");

-- CreateIndex
CREATE INDEX IF NOT EXISTS "Linten_VerificationToken_budget_reset_at_expires_idx" ON "Linten_VerificationToken"("budget_reset_at", "expires");
