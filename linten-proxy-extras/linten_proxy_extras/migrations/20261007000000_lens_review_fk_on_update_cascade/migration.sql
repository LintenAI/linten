-- DropForeignKey
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'Linten_LensReview_lens_id_fkey' AND conrelid = '"Linten_LensReview"'::regclass) THEN
        ALTER TABLE "Linten_LensReview" DROP CONSTRAINT "Linten_LensReview_lens_id_fkey";
    END IF;
END $$;

-- AddForeignKey
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'Linten_LensReview_lens_id_fkey' AND conrelid = '"Linten_LensReview"'::regclass) THEN
        ALTER TABLE "Linten_LensReview" ADD CONSTRAINT "Linten_LensReview_lens_id_fkey" FOREIGN KEY ("lens_id") REFERENCES "Linten_Lens"("id") ON DELETE CASCADE ON UPDATE CASCADE;
    END IF;
END $$;
