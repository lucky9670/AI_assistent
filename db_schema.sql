BEGIN;
--
-- Create model Activity
--
CREATE TABLE "rest_apis_activity" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(255) NOT NULL, "description" text NOT NULL);
--
-- Create model User
--
CREATE TABLE "rest_apis_user" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "password" varchar(128) NOT NULL, "last_login" datetime NULL, "is_superuser" bool NOT NULL, "username" varchar(150) NOT NULL UNIQUE, "first_name" varchar(150) NOT NULL, "last_name" varchar(150) NOT NULL, "is_staff" bool NOT NULL, "is_active" bool NOT NULL, "date_joined" datetime NOT NULL, "email" varchar(50) NOT NULL UNIQUE, "phone" varchar(13) NOT NULL, "gender" varchar(20) NOT NULL, "age" varchar(50) NOT NULL, "address" varchar(250) NOT NULL, "image" varchar(100) NULL, "prefrence" text NULL CHECK ((JSON_VALID("prefrence") OR "prefrence" IS NULL)));
CREATE TABLE "rest_apis_user_groups" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "user_id" bigint NOT NULL REFERENCES "rest_apis_user" ("id") DEFERRABLE INITIALLY DEFERRED, "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE "rest_apis_user_user_permissions" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "user_id" bigint NOT NULL REFERENCES "rest_apis_user" ("id") DEFERRABLE INITIALLY DEFERRED, "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model Reminder
--
CREATE TABLE "rest_apis_reminder" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "title" varchar(255) NOT NULL, "description" text NOT NULL, "due_date" datetime NOT NULL, "user_id" bigint NOT NULL REFERENCES "rest_apis_user" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model Task
--
CREATE TABLE "rest_apis_task" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(255) NOT NULL, "description" text NOT NULL, "trigger" text NULL CHECK ((JSON_VALID("trigger") OR "trigger" IS NULL)), "user_id" bigint NOT NULL REFERENCES "rest_apis_user" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE UNIQUE INDEX "rest_apis_user_groups_user_id_group_id_2339733c_uniq" ON "rest_apis_user_groups" ("user_id", "group_id");
CREATE INDEX "rest_apis_user_groups_user_id_d5c9f47b" ON "rest_apis_user_groups" ("user_id");
CREATE INDEX "rest_apis_user_groups_group_id_f1a93ca1" ON "rest_apis_user_groups" ("group_id");
CREATE UNIQUE INDEX "rest_apis_user_user_permissions_user_id_permission_id_db116667_uniq" ON "rest_apis_user_user_permissions" ("user_id", "permission_id");
CREATE INDEX "rest_apis_user_user_permissions_user_id_7cb95ff8" ON "rest_apis_user_user_permissions" ("user_id");
CREATE INDEX "rest_apis_user_user_permissions_permission_id_5d8a0046" ON "rest_apis_user_user_permissions" ("permission_id");
CREATE INDEX "rest_apis_reminder_user_id_e069ae2b" ON "rest_apis_reminder" ("user_id");
CREATE INDEX "rest_apis_task_user_id_7b42eeed" ON "rest_apis_task" ("user_id");
COMMIT;