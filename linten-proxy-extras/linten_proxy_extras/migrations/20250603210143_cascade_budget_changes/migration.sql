-- DropForeignKey
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'Linten_TeamMembership_budget_id_fkey') THEN
        ALTER TABLE "Linten_TeamMembership" DROP CONSTRAINT "Linten_TeamMembership_budget_id_fkey";
    END IF;
END $$;

-- AddForeignKey
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'Linten_TeamMembership_budget_id_fkey') THEN
        ALTER TABLE "Linten_TeamMembership" ADD CONSTRAINT "Linten_TeamMembership_budget_id_fkey" FOREIGN KEY ("budget_id") REFERENCES "Linten_BudgetTable"("budget_id") ON DELETE CASCADE ON UPDATE CASCADE;
    END IF;
END $$;

