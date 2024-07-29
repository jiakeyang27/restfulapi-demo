CREATE DATABASE alarm_system;

USE alarm_system;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE alarm_levels (
    id INT AUTO_INCREMENT PRIMARY KEY,
    level VARCHAR(255) NOT NULL,
    description TEXT NOT NULL
);
