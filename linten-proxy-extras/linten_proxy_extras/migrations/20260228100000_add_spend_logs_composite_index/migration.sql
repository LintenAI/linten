-- CreateIndex
CREATE INDEX IF NOT EXISTS "Linten_SpendLogs_startTime_request_id_idx" ON "Linten_SpendLogs"("startTime", "request_id");
