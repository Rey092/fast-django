CREATE USER test_user WITH PASSWORD 'test_pass';

CREATE DATABASE test_db;
GRANT ALL PRIVILEGES ON DATABASE test_db TO test_user;
