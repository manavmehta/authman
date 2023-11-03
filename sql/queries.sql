
CREATE TABLE organization (
    id SERIAL PRIMARY KEY,
    parent_id INTEGER,
    name VARCHAR(100) NOT NULL,
    path TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    updated_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    kotak_username VARCHAR(50) NOT NULL UNIQUE,
    contact_num BIGINT NOT NULL,
    supervisor_id INTEGER,
    organization_id SERIAL NOT NULL REFERENCES organization(id),
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    updated_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TYPE access_ENUM AS ENUM('R', 'W');

CREATE TABLE user_org_access (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    organization_id INTEGER,
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    updated_at TIMESTAMP NOT NULL DEFAULT now(),
    access_type access_ENUM NOT NULL
);

---------------

-- ALTER TABLE organization DROP CONSTRAINT organization_parent_id_fkey;

-- ALTER TABLE organization ADD CONSTRAINT organization_parent_id_fkey FOREIGN KEY (parent_id) REFERENCES organization (id) ON DELETE CASCADE;

CREATE OR REPLACE FUNCTION generate_organization_path() RETURNS TRIGGER AS $$
BEGIN
    IF NEW.parent_id = -1 THEN
        NEW.path := NEW.name;
    ELSE
        NEW.path := (SELECT path FROM organization WHERE id = NEW.parent_id) || '/' || NEW.name;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER organization_generate_path
BEFORE INSERT ON organization
FOR EACH ROW
EXECUTE FUNCTION generate_organization_path();

-- SET log_statement = 'all';