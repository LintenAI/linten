DO $$
BEGIN
    ALTER TABLE IF EXISTS "Linten_Engine" RENAME TO "Linten_Lens";
    ALTER TABLE IF EXISTS "Linten_EngineRun" RENAME TO "Linten_LensRun";
    ALTER TABLE IF EXISTS "Linten_EngineWorker" RENAME TO "Linten_LensWorker";
    IF EXISTS (
        SELECT 1 FROM pg_attribute
        WHERE attrelid = to_regclass('"Linten_LensRun"')
          AND attname = 'engine_id' AND NOT attisdropped
    ) THEN
        ALTER TABLE "Linten_LensRun" RENAME COLUMN "engine_id" TO "lens_id";
    END IF;
    ALTER INDEX IF EXISTS "Linten_Engine_pkey" RENAME TO "Linten_Lens_pkey";
    ALTER INDEX IF EXISTS "Linten_EngineRun_pkey" RENAME TO "Linten_LensRun_pkey";
    ALTER INDEX IF EXISTS "Linten_EngineWorker_pkey" RENAME TO "Linten_LensWorker_pkey";
    ALTER INDEX IF EXISTS "Linten_EngineWorker_token_hash_key" RENAME TO "Linten_LensWorker_token_hash_key";
    ALTER INDEX IF EXISTS "Linten_EngineRun_engine_id_created_at_idx" RENAME TO "Linten_LensRun_lens_id_created_at_idx";
END $$;
