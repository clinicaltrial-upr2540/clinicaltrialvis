
BEGIN;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'ro_role') THEN
        CREATE ROLE ro_role;
    END IF;
END
$$;
GRANT usage ON SCHEMA curated TO ro_role;
GRANT usage ON SCHEMA application TO ro_role;
GRANT SELECT ON ALL TABLES IN SCHEMA curated TO ro_role;
GRANT SELECT ON ALL TABLES IN SCHEMA application TO ro_role;
ALTER DEFAULT PRIVILEGES IN SCHEMA curated GRANT SELECT ON TABLES TO ro_role;
ALTER DEFAULT PRIVILEGES IN SCHEMA application GRANT SELECT ON TABLES TO ro_role;

COMMIT;