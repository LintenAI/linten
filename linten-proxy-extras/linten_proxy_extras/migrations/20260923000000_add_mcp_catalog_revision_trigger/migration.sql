CREATE OR REPLACE FUNCTION linten_bump_mcp_catalog_revision() RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO "Linten_Config" ("param_name", "reload_revision")
  VALUES ('mcp_catalog', 1)
  ON CONFLICT ("param_name") DO UPDATE SET "reload_revision" = "Linten_Config"."reload_revision" + 1;
  RETURN NULL;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS "linten_mcp_catalog_revision" ON "Linten_MCPServerTable";
CREATE TRIGGER "linten_mcp_catalog_revision"
AFTER INSERT OR UPDATE OR DELETE ON "Linten_MCPServerTable"
FOR EACH STATEMENT EXECUTE PROCEDURE linten_bump_mcp_catalog_revision();
