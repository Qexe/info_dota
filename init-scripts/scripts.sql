-- init.sql
DO $$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'app') THEN
    CREATE ROLE app WITH LOGIN PASSWORD '3226';
  END IF;
END $$;

CREATE DATABASE infododa_db WITH OWNER app;
\c infododa_db;

CREATE TABLE main_data(
    id SERIAL PRIMARY KEY,
    url text,
    request_body text,
    response text
);
CREATE TABLE metadata(
    id SERIAL REFERENCES main_data(id),
    datetime text,
    status text,
    req_timing text
);