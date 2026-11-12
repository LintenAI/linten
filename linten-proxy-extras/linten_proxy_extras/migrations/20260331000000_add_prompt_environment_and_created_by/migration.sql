-- AlterTable
ALTER TABLE "Linten_PromptTable" ADD COLUMN "environment" TEXT NOT NULL DEFAULT 'development';
ALTER TABLE "Linten_PromptTable" ADD COLUMN "created_by" TEXT;

-- DropIndex (old unique constraint)
DROP INDEX IF EXISTS "Linten_PromptTable_prompt_id_version_key";

-- CreateIndex (new unique constraint)
CREATE UNIQUE INDEX "Linten_PromptTable_prompt_id_version_environment_key" ON "Linten_PromptTable"("prompt_id", "version", "environment");

-- CreateIndex (new composite index)
CREATE INDEX "Linten_PromptTable_prompt_id_environment_idx" ON "Linten_PromptTable"("prompt_id", "environment");
