-- DropForeignKey
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'Linten_TeamMembership_budget_id_fkey') THEN
        ALTER TABLE "Linten_TeamMembership" DROP CONSTRAINT "Linten_TeamMembership_budget_id_fkey";
    END IF;
END $$;

-- AlterTable
ALTER TABLE "Linten_ManagedFileTable" ALTER COLUMN "file_object" DROP NOT NULL;

-- AddForeignKey
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'Linten_TeamMembership_budget_id_fkey') THEN
        ALTER TABLE "Linten_TeamMembership" ADD CONSTRAINT "Linten_TeamMembership_budget_id_fkey" FOREIGN KEY ("budget_id") REFERENCES "Linten_BudgetTable"("budget_id") ON DELETE SET NULL ON UPDATE CASCADE;
    END IF;
END $$;

