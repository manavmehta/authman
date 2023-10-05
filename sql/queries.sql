CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE team (
    id SERIAL PRIMARY KEY,
    parent_id SERIAL REFERENCES team(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    path TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    updated_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    contact_num BIGINT NOT NULL,
    supervisor_id SERIAL REFERENCES users(id),
    team_id SERIAL NOT NULL REFERENCES team(id),
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    updated_at TIMESTAMP NOT NULL DEFAULT now()
);

---------------

INSERT INTO team (name, path) VALUES ('Kotak', '/');

INSERT INTO team (name, parent_id) VALUES ('Risk', (SELECT id FROM team WHERE name = 'Kotak'));
INSERT INTO team (name, parent_id) VALUES ('Treasury', (SELECT id FROM team WHERE name = 'Kotak'));
INSERT INTO team (name, parent_id) VALUES ('Market Risk', (SELECT id FROM team WHERE name = 'Risk'));
INSERT INTO team (name, parent_id) VALUES ('Credit Risk', (SELECT id FROM team WHERE name = 'Risk'));
INSERT INTO team (name, parent_id) VALUES ('Counterparty Risk', (SELECT id FROM team WHERE name = 'Market Risk'));


INSERT INTO users (name, email, contact_num, team_id) VALUES ('Sougat', 'sougat@chakraborty.com', 1234567890, 'fd75643b-7220-4e43-807a-1f4638448e55');
INSERT INTO users (name, email, contact_num, team_id) VALUES ('Mohit', 'mohit@beniwal.com', 9876543210, '1fe7eb7b-95be-46b8-b3ce-74fa9748e26d');
INSERT INTO users (name, email, contact_num, team_id) VALUES ('Manav', 'manav@mehta.com', 1111111111, '1fe7eb7b-95be-46b8-b3ce-74fa9748e26d');
INSERT INTO users (name, email, contact_num, team_id) VALUES ('Piyush', 'piyush@sharma.com', 2222222222, '11a56ec9-fac9-4d59-9242-3f6945c20d4f');

---------------

SELECT * FROM team;
SELECT * FROM users;
