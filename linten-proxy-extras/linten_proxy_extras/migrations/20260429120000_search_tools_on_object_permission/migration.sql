-- Search tool allowlists live on Linten_ObjectPermissionTable (with agents, MCP, vector stores).
ALTER TABLE "Linten_ObjectPermissionTable" ADD COLUMN IF NOT EXISTS "search_tools" TEXT[] DEFAULT ARRAY[]::TEXT[];
