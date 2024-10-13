/* The databases for local development. */

-- create user.
CREATE USER dbuser WITH PASSWORD dbpassword;

/* The database for development. */

-- create database for development.
CREATE DATABASE dbname OWNER dbuser;

-- grant privileges.
GRANT ALL PRIVILEGES ON DATABASE dbname TO dbuser;


/* The database for testing */

-- create database for testing.
CREATE DATABASE dbname_test OWNER dbuser;

-- grant privileges.
GRANT ALL PRIVILEGES ON DATABASE dbname_test TO dbuser;
