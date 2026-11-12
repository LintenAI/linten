SET LOCAL lock_timeout = '10s';

CREATE SEQUENCE IF NOT EXISTS "linten_environment_variables_revision_seq";
GRANT USAGE ON SEQUENCE "linten_environment_variables_revision_seq" TO PUBLIC;

CREATE OR REPLACE FUNCTION linten_bump_environment_variables_revision() RETURNS TRIGGER AS $$
DECLARE
  next_revision BIGINT := nextval(format('%I.linten_environment_variables_revision_seq', TG_TABLE_SCHEMA)::regclass);
BEGIN
  IF TG_OP = 'UPDATE' THEN
    NEW."reload_revision" := GREATEST(next_revision, OLD."reload_revision" + 1);
  ELSE
    NEW."reload_revision" := next_revision;
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS "linten_environment_variables_revision" ON "Linten_Config";
CREATE TRIGGER "linten_environment_variables_revision"
BEFORE INSERT OR UPDATE ON "Linten_Config"
FOR EACH ROW WHEN (NEW."param_name" = 'environment_variables')
EXECUTE PROCEDURE linten_bump_environment_variables_revision();
