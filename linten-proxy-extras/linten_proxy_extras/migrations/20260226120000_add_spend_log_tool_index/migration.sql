-- CreateTable
CREATE TABLE IF NOT EXISTS "Linten_SpendLogToolIndex" (
    "request_id" TEXT NOT NULL,
    "tool_name" TEXT NOT NULL,
    "start_time" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "Linten_SpendLogToolIndex_pkey" PRIMARY KEY ("request_id","tool_name")
);

-- CreateIndex
CREATE INDEX IF NOT EXISTS "Linten_SpendLogToolIndex_tool_name_start_time_idx" ON "Linten_SpendLogToolIndex"("tool_name", "start_time");
