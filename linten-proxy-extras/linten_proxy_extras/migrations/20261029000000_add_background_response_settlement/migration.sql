SET LOCAL lock_timeout = '10s';

-- CreateTable
CREATE TABLE IF NOT EXISTS "Linten_BackgroundResponseSettlement" (
    "response_id" TEXT NOT NULL,
    "settled_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "Linten_BackgroundResponseSettlement_pkey" PRIMARY KEY ("response_id")
);
