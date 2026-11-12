SET LOCAL lock_timeout = '10s';
CREATE TABLE IF NOT EXISTS "Linten_ClaudeCodePluginVersion" (
    "id" TEXT NOT NULL,
    "plugin_id" TEXT NOT NULL,
    "version" TEXT,
    "description" TEXT,
    "manifest_json" TEXT,
    "published_at" TIMESTAMP(3),
    "published_by" TEXT,
    "archive_available" BOOLEAN NOT NULL DEFAULT false,
    "content" BYTEA,
    CONSTRAINT "Linten_ClaudeCodePluginVersion_pkey" PRIMARY KEY ("id"),
    CONSTRAINT "Linten_ClaudeCodePluginVersion_plugin_id_fkey" FOREIGN KEY ("plugin_id") REFERENCES "Linten_ClaudeCodePluginTable"("id") ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE UNIQUE INDEX IF NOT EXISTS "Linten_ClaudeCodePluginVersion_plugin_id_version_key" ON "Linten_ClaudeCodePluginVersion"("plugin_id", "version");
CREATE INDEX IF NOT EXISTS "Linten_ClaudeCodePluginVersion_plugin_id_published_at_idx" ON "Linten_ClaudeCodePluginVersion"("plugin_id", "published_at");
