-- Change the password for the 'postgres' user
ALTER USER postgres PASSWORD 'abcd1234';
-- Create the database
CREATE DATABASE crm_dev;
GRANT ALL PRIVILEGES ON DATABASE crm_dev TO postgres;
CREATE USER crm_user WITH ENCRYPTED PASSWORD 'crm_password';
GRANT ALL PRIVILEGES ON DATABASE crm_dev TO crm_user;
ALTER USER crm_user SUPERUSER;