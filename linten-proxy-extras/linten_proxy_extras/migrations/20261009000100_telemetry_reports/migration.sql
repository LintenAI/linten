SET LOCAL lock_timeout = '10s';

CREATE TABLE IF NOT EXISTS "Linten_TelemetryReport" (
    "id" TEXT NOT NULL,
    "window_start" DOUBLE PRECISION NOT NULL,
    "window_end" DOUBLE PRECISION NOT NULL,
    "report" JSONB NOT NULL,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT "Linten_TelemetryReport_pkey" PRIMARY KEY ("id")
);

CREATE INDEX IF NOT EXISTS "Linten_TelemetryReport_window_end_idx" ON "Linten_TelemetryReport"("window_end");

CREATE INDEX IF NOT EXISTS "Linten_TelemetryReport_created_at_idx" ON "Linten_TelemetryReport"("created_at");
