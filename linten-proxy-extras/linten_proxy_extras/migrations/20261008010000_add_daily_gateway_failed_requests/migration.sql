-- CreateTable
CREATE TABLE IF NOT EXISTS "Linten_DailyGatewayFailedRequests" (
    "date" TEXT NOT NULL,
    "category" TEXT NOT NULL,
    "route" TEXT NOT NULL,
    "status_code" INTEGER NOT NULL,
    "failed_requests" BIGINT NOT NULL DEFAULT 0,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "Linten_DailyGatewayFailedRequests_pkey" PRIMARY KEY ("date","category","route","status_code")
);

-- CreateIndex
CREATE INDEX IF NOT EXISTS "Linten_DailyGatewayFailedRequests_date_idx" ON "Linten_DailyGatewayFailedRequests"("date");
