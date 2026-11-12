SET LOCAL lock_timeout = '10s';

CREATE TABLE IF NOT EXISTS "Linten_ClaudeCodePluginUpload" (
    "plugin_name" TEXT NOT NULL,
    "content" BYTEA NOT NULL,
    CONSTRAINT "Linten_ClaudeCodePluginUpload_pkey" PRIMARY KEY ("plugin_name"),
    CONSTRAINT "Linten_ClaudeCodePluginUpload_plugin_name_fkey" FOREIGN KEY ("plugin_name")
        REFERENCES "Linten_ClaudeCodePluginTable"("name") ON DELETE CASCADE ON UPDATE CASCADE
);
