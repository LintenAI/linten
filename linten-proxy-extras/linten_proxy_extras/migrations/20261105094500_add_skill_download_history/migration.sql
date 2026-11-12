SET LOCAL lock_timeout = '10s';

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_attribute
        WHERE attrelid = to_regclass('"Linten_ClaudeCodePluginTable"')
            AND attname = 'anonymous_download_count' AND NOT attisdropped
    ) THEN
        ALTER TABLE "Linten_ClaudeCodePluginTable"
            ADD COLUMN IF NOT EXISTS "anonymous_download_count" BIGINT NOT NULL DEFAULT 0;
    END IF;

    IF to_regclass('"Linten_ClaudeCodePluginDownload"') IS NULL THEN
        CREATE TABLE IF NOT EXISTS "Linten_ClaudeCodePluginDownload" (
            "id" BIGSERIAL NOT NULL,
            "plugin_id" TEXT NOT NULL,
            "downloaded_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
            "version" TEXT,
            "digest" TEXT NOT NULL,
            "authenticated" BOOLEAN NOT NULL,
            "user_id" TEXT,
            "user_email" TEXT,
            "key_alias" TEXT,
            "team_id" TEXT,
            "team_alias" TEXT,
            CONSTRAINT "Linten_ClaudeCodePluginDownload_pkey" PRIMARY KEY ("id"),
            CONSTRAINT "Linten_ClaudeCodePluginDownload_plugin_id_fkey" FOREIGN KEY ("plugin_id")
                REFERENCES "Linten_ClaudeCodePluginTable"("id") ON DELETE CASCADE ON UPDATE CASCADE
        );
    END IF;

    IF to_regclass('"Linten_ClaudeCodePluginDownload_plugin_id_id_idx"') IS NULL THEN
        CREATE INDEX IF NOT EXISTS "Linten_ClaudeCodePluginDownload_plugin_id_id_idx"
            ON "Linten_ClaudeCodePluginDownload"("plugin_id", "id");
    END IF;
END $$;
