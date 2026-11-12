-- DropIndex
DROP INDEX IF EXISTS "Linten_PromptTable_prompt_id_key";

-- AlterTable
ALTER TABLE "Linten_PromptTable"
ADD COLUMN IF NOT EXISTS "version" INTEGER NOT NULL DEFAULT 1;

-- CreateIndex
CREATE INDEX IF NOT EXISTS "Linten_PromptTable_prompt_id_idx" ON "Linten_PromptTable" ("prompt_id");

-- CreateIndex
CREATE UNIQUE INDEX IF NOT EXISTS "Linten_PromptTable_prompt_id_version_key" ON "Linten_PromptTable" ("prompt_id", "version");