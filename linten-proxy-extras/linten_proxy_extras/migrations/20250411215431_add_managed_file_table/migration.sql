-- CreateTable
CREATE TABLE IF NOT EXISTS "Linten_ManagedFileTable" (
    "id" TEXT NOT NULL,
    "unified_file_id" TEXT NOT NULL,
    "file_object" JSONB NOT NULL,
    "model_mappings" JSONB NOT NULL,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "Linten_ManagedFileTable_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX IF NOT EXISTS "Linten_ManagedFileTable_unified_file_id_key" ON "Linten_ManagedFileTable"("unified_file_id");

-- CreateIndex
CREATE INDEX IF NOT EXISTS "Linten_ManagedFileTable_unified_file_id_idx" ON "Linten_ManagedFileTable"("unified_file_id");

