-- CreateTable
CREATE TABLE IF NOT EXISTS "Linten_ManagedVectorStoreTable" (
    "id" TEXT NOT NULL,
    "unified_resource_id" TEXT NOT NULL,
    "resource_object" JSONB,
    "model_mappings" JSONB NOT NULL,
    "flat_model_resource_ids" TEXT[] DEFAULT ARRAY[]::TEXT[],
    "storage_backend" TEXT,
    "storage_url" TEXT,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "created_by" TEXT,
    "updated_at" TIMESTAMP(3) NOT NULL,
    "updated_by" TEXT,

    CONSTRAINT "Linten_ManagedVectorStoreTable_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX IF NOT EXISTS "Linten_ManagedVectorStoreTable_unified_resource_id_key" ON "Linten_ManagedVectorStoreTable"("unified_resource_id");

-- CreateIndex
CREATE INDEX IF NOT EXISTS "Linten_ManagedVectorStoreTable_unified_resource_id_idx" ON "Linten_ManagedVectorStoreTable"("unified_resource_id");
