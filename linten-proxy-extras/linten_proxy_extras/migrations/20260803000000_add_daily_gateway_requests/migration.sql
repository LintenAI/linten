-- CreateTable
CREATE TABLE IF NOT EXISTS "Linten_DailyGatewayRequests" (
    "date" TEXT NOT NULL,
    "category" TEXT NOT NULL,
    "route" TEXT NOT NULL,
    "successful_requests" BIGINT NOT NULL DEFAULT 0,
    "failed_requests" BIGINT NOT NULL DEFAULT 0,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "Linten_DailyGatewayRequests_pkey" PRIMARY KEY ("date","category","route")
);

-- CreateIndex
CREATE INDEX IF NOT EXISTS "Linten_DailyGatewayRequests_date_idx" ON "Linten_DailyGatewayRequests"("date");
