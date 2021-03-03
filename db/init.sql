create database nl2ml;
CREATE USER 'robot'@'172.24.0.1' IDENTIFIED BY 'nl2ml123!';
GRANT ALL PRIVILEGES ON nl2ml. * TO 'robot'@'172.24.0.1';