-- GTM domain model (SQLite dialect, portable to Postgres with minor type changes).
--
-- Separation that matters most: COMPANY and LOCATION are facts about the world.
-- ACCOUNT, OPPORTUNITY, CUSTOMER and CONTRACT are facts about our relationship with it.
-- Mixing them is how a CRM ends up with three "Riverbend Credit Union" accounts,
-- one per branch, and a whitespace report that counts the same customer three times.

CREATE TABLE company (
    company_id      TEXT PRIMARY KEY,           -- canonical id, never reused
    canonical_name  TEXT NOT NULL,
    domain          TEXT UNIQUE,                -- strongest natural key when present
    industry        TEXT,
    employee_band   TEXT
);

CREATE TABLE location (
    location_id     TEXT PRIMARY KEY,
    company_id      TEXT NOT NULL REFERENCES company(company_id),
    name            TEXT NOT NULL,
    address         TEXT,
    phone_e164      TEXT,
    lat             REAL,
    lon             REAL,
    category        TEXT
);

CREATE TABLE account (                          -- our commercial view of a company
    account_id      TEXT PRIMARY KEY,
    company_id      TEXT NOT NULL UNIQUE REFERENCES company(company_id),
    owner           TEXT,
    tier            TEXT CHECK (tier IN ('A', 'B', 'C', 'D')),
    status          TEXT CHECK (status IN ('prospect', 'customer', 'churned'))
);

CREATE TABLE contact (
    contact_id      TEXT PRIMARY KEY,
    company_id      TEXT NOT NULL REFERENCES company(company_id),
    full_name       TEXT NOT NULL,
    title           TEXT,
    email           TEXT UNIQUE                 -- lowercased before insert
);

CREATE TABLE product (product_id TEXT PRIMARY KEY, name TEXT NOT NULL, family TEXT);
CREATE TABLE service (service_id TEXT PRIMARY KEY, name TEXT NOT NULL);

CREATE TABLE opportunity (
    opportunity_id  TEXT PRIMARY KEY,
    account_id      TEXT NOT NULL REFERENCES account(account_id),
    product_id      TEXT REFERENCES product(product_id),
    name            TEXT NOT NULL,
    stage           TEXT NOT NULL,
    amount          REAL,
    close_date      TEXT
);

CREATE TABLE buying_committee_member (          -- a contact's role on one deal, not on the company
    opportunity_id  TEXT NOT NULL REFERENCES opportunity(opportunity_id),
    contact_id      TEXT NOT NULL REFERENCES contact(contact_id),
    role            TEXT NOT NULL CHECK (role IN ('economic_buyer', 'champion', 'technical_evaluator', 'user', 'blocker')),
    PRIMARY KEY (opportunity_id, contact_id)
);

CREATE TABLE customer (
    customer_id     TEXT PRIMARY KEY,
    account_id      TEXT NOT NULL UNIQUE REFERENCES account(account_id),
    customer_since  TEXT
);

CREATE TABLE contract (
    contract_id     TEXT PRIMARY KEY,
    customer_id     TEXT NOT NULL REFERENCES customer(customer_id),
    product_id      TEXT NOT NULL REFERENCES product(product_id),
    start_date      TEXT NOT NULL,
    end_date        TEXT NOT NULL,
    arr             REAL NOT NULL
);

CREATE TABLE intent_signal (
    signal_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id      TEXT NOT NULL REFERENCES company(company_id),
    type            TEXT NOT NULL,
    value           TEXT,
    observed_at     TEXT NOT NULL,
    source          TEXT NOT NULL,              -- e.g. call:call_005, enrichment:job_change
    confidence      REAL
);

CREATE TABLE activity (
    activity_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id      TEXT NOT NULL REFERENCES account(account_id),
    contact_id      TEXT REFERENCES contact(contact_id),
    type            TEXT NOT NULL,
    occurred_at     TEXT NOT NULL,
    summary         TEXT
);

-- Lineage: every raw record we ingested and which canonical entity it became.
CREATE TABLE source_record (
    source_system   TEXT NOT NULL,
    source_key      TEXT NOT NULL,
    entity_type     TEXT NOT NULL,
    entity_id       TEXT,                       -- NULL while a match is waiting for review
    payload_json    TEXT NOT NULL,
    PRIMARY KEY (source_system, source_key)
);

-- Identity resolution audit trail, including the matches we chose NOT to make.
CREATE TABLE match_decision (
    source_system   TEXT NOT NULL,
    source_key      TEXT NOT NULL,
    candidate_id    TEXT,
    method          TEXT NOT NULL,              -- domain | phone | name_geo | name_only | none
    score           REAL NOT NULL,
    decision        TEXT NOT NULL CHECK (decision IN ('auto_merge', 'review', 'new_entity')),
    PRIMARY KEY (source_system, source_key)
);
