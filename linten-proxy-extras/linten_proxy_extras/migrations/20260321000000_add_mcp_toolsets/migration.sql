-- CreateTable: Linten_MCPToolsetTable
CREATE TABLE IF NOT EXISTS "Linten_MCPToolsetTable" (
    "toolset_id" TEXT NOT NULL,
    "toolset_name" TEXT NOT NULL,
    "description" TEXT,
    "tools" JSONB NOT NULL DEFAULT '[]',
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "created_by" TEXT,
    "updated_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_by" TEXT,

    CONSTRAINT "Linten_MCPToolsetTable_pkey" PRIMARY KEY ("toolset_id")
);

-- CreateIndex
CREATE UNIQUE INDEX IF NOT EXISTS "Linten_MCPToolsetTable_toolset_name_key" ON "Linten_MCPToolsetTable"("toolset_name");

-- AlterTable: add mcp_toolsets to ObjectPermissionTable
ALTER TABLE "Linten_ObjectPermissionTable" ADD COLUMN IF NOT EXISTS "mcp_toolsets" TEXT[] DEFAULT ARRAY[]::TEXT[];
