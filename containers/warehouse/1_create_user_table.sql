DROP TABLE IF EXISTS info.userinfo;
DROP SCHEMA IF EXISTS info;
CREATE SCHEMA info;
CREATE TABLE info.userinfo (
    id INT,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(50),
    gender VARCHAR(20),
    ip_address VARCHAR(15)
);
