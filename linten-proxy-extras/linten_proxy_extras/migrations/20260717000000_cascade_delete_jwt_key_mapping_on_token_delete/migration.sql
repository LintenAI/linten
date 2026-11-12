-- DropForeignKey
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'Linten_JWTKeyMapping_token_fkey') THEN
        ALTER TABLE "Linten_JWTKeyMapping" DROP CONSTRAINT "Linten_JWTKeyMapping_token_fkey";
    END IF;
END $$;

-- AddForeignKey
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'Linten_JWTKeyMapping_token_fkey') THEN
        ALTER TABLE "Linten_JWTKeyMapping" ADD CONSTRAINT "Linten_JWTKeyMapping_token_fkey" FOREIGN KEY ("token") REFERENCES "Linten_VerificationToken"("token") ON DELETE CASCADE ON UPDATE CASCADE;
    END IF;
END $$;
