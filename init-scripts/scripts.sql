-- init.sql

\c infodota_db;

CREATE TABLE IF NOT EXISTS main_data(
    id SERIAL PRIMARY KEY,
    url text,
    request_body text,
    response text
);

CREATE TABLE IF NOT EXISTS metadata(
    id SERIAL REFERENCES main_data(id),
    datetime text,
    status text,
    req_timing text
);