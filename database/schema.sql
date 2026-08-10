CREATE TABLE "access_key" (
  "rfid" varchar PRIMARY KEY,
  "privilege" varchar
);

CREATE TABLE "worker" (
  "id_worker" int PRIMARY KEY,
  "name" varchar,
  "surname" varchar,
  "role" varchar,
  "worker_key_rfid" int
);

CREATE TABLE "access_gate" (
  "id_gate" int PRIMARY KEY,
  "location" varchar,
  "required_privilege" varchar
);

CREATE TABLE "access_history" (
  "id_history" int PRIMARY KEY,
  "attempt_time" timestamp,
  "id_worker" int,
  "id_gate" int,
  "rfid" int,
  "successful_access" bool
);

CREATE TABLE "system_account" (
  "username" varchar PRIMARY KEY,
  "password_hash" varchar,
  "account_worker_id" int,
  "privilege" varchar
);

ALTER TABLE "access_key" ADD FOREIGN KEY ("rfid") REFERENCES "worker" ("worker_key_rfid") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "access_history" ADD FOREIGN KEY ("id_worker") REFERENCES "worker" ("id_worker") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "access_history" ADD FOREIGN KEY ("id_gate") REFERENCES "access_gate" ("id_gate") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "worker" ADD FOREIGN KEY ("id_worker") REFERENCES "system_account" ("account_worker_id") DEFERRABLE INITIALLY IMMEDIATE;
