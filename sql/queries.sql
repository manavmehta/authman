
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

INSERT INTO organization (name, path) VALUES ('Kotak', '/');

INSERT INTO organization (name, parent_id, path) VALUES ('Risk', (SELECT id FROM organization WHERE name = 'Kotak'), '/Kotak/Risk');
INSERT INTO organization (name, parent_id, path) VALUES ('Treasury', (SELECT id FROM organization WHERE name = 'Kotak'), '/Kotak/Treasury');
INSERT INTO organization (name, parent_id, path) VALUES ('Market Risk', (SELECT id FROM organization WHERE name = 'Risk'), '/Kotak/Risk/MarketRisk');
INSERT INTO organization (name, parent_id, path) VALUES ('Credit Risk', (SELECT id FROM organization WHERE name = 'Risk'), '/Kotak/Risk/CreditRisk');
INSERT INTO organization (name, parent_id, path) VALUES ('Counterparty Risk', (SELECT id FROM organization WHERE name = 'Market Risk'), '/Kotak/Risk/MarketRisk/CounterpartyRisk');


INSERT INTO users (name, email, kotak_username, contact_num, organization_id) VALUES ('Sougat', 'sougat@chakraborty.com', 'sougat', 1234567890, 1);
INSERT INTO users (name, email, kotak_username, contact_num, organization_id) VALUES ('Mohit', 'mohit@beniwal.com', 'mohit', 9876543210, 2);
INSERT INTO users (name, email, kotak_username, contact_num, organization_id) VALUES ('Manav', 'manav@mehta.com', 'manav', 1111111111, 2);
INSERT INTO users (name, email, kotak_username, contact_num, organization_id) VALUES ('Piyush', 'piyush@sharma.com', 'piyush', 2222222222, 3);


INSERT INTO user_org_access(user_id, organization_id, access_type) VALUES ((SELECT id FROM users WHERE name = 'Sougat'), (SELECT id FROM organization WHERE name = 'Risk'), 'W');
INSERT INTO user_org_access(user_id, organization_id, access_type) VALUES ((SELECT id FROM users WHERE name = 'Sougat'), (SELECT id FROM organization WHERE name = 'Kotak'), 'R');
INSERT INTO user_org_access(user_id, organization_id, access_type) VALUES ((SELECT id FROM users WHERE name = 'Mohit'), (SELECT id FROM organization WHERE name = 'Credit Risk'), 'W');
INSERT INTO user_org_access(user_id, organization_id, access_type) VALUES ((SELECT id FROM users WHERE name = 'Manav'), (SELECT id FROM organization WHERE name = 'Market Risk'), 'W');
INSERT INTO user_org_access(user_id, organization_id, access_type) VALUES ((SELECT id FROM users WHERE name = 'Mohit'), (SELECT id FROM organization WHERE name = 'Risk'), 'R');
INSERT INTO user_org_access(user_id, organization_id, access_type) VALUES ((SELECT id FROM users WHERE name = 'Manav'), (SELECT id FROM organization WHERE name = 'Risk'), 'R');
INSERT INTO user_org_access(user_id, organization_id, access_type) VALUES ((SELECT id FROM users WHERE name = 'Mohit'), (SELECT id FROM organization WHERE name = 'Treasury'), 'R');
INSERT INTO user_org_access(user_id, organization_id, access_type) VALUES ((SELECT id FROM users WHERE name = 'Manav'), (SELECT id FROM organization WHERE name = 'Treasury'), 'R');

---------------

SELECT * FROM organization;
SELECT * FROM users;

-- ALTER TABLE organization DROP CONSTRAINT organization_parent_id_fkey;

-- ALTER TABLE organization ADD CONSTRAINT organization_parent_id_fkey FOREIGN KEY (parent_id) REFERENCES organization (id) ON DELETE CASCADE;
