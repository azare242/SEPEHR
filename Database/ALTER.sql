ALTER TABLE sepehr.users
ADD COLUMN deleted INT NULL DEFAULT 0 AFTER EMAIL;
