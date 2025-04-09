-- MySQL Workbench SQL Dump
-- Version 8.0.  what is the difference between password_reset.html reset_password.html and Pswreset.html
-- http://www.mysql.com
-- Server version: 8.0.23

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

CREATE DATABASE IF NOT EXISTS project_management DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE project_management;

-- Table structure for table projects
CREATE TABLE IF NOT EXISTS projects (
  project_id INT NOT NULL AUTO_INCREMENT,
  project_name VARCHAR(255) NOT NULL,
  project_description TEXT,
  category VARCHAR(50),
  due_date DATE,
  created_by INT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (project_id),
  KEY created_by (created_by)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table structure for table project_members
CREATE TABLE IF NOT EXISTS project_members (
  member_id INT NOT NULL AUTO_INCREMENT,
  project_id INT NOT NULL,
  user_id INT NOT NULL,
  role ENUM('Manager','Contributor') DEFAULT 'Contributor',
  added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (member_id),
  KEY project_id (project_id),
  KEY user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table structure for table roles
CREATE TABLE IF NOT EXISTS roles (
  role_id INT NOT NULL AUTO_INCREMENT,
  role_name VARCHAR(255) NOT NULL,
  role_description TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (role_id),
  UNIQUE KEY role_name (role_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Data for table roles
INSERT INTO roles (role_name, role_description) VALUES
('Admin', 'Full access to all features and settings.'),
('Manager', 'Can create and manage projects and tasks.'),
('Contributor', 'Can be assigned to tasks and add comments.');

-- Table structure for table status
CREATE TABLE IF NOT EXISTS status (
  status_id INT NOT NULL AUTO_INCREMENT,
  status_name VARCHAR(255) NOT NULL,
  PRIMARY KEY (status_id),
  UNIQUE KEY status_name (status_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Data for table status
INSERT INTO status (status_name) VALUES
('Completed'),
('In Progress'),
('Not Started'),
('On Hold');

-- Table structure for table tasks
CREATE TABLE IF NOT EXISTS tasks (
  task_id INT NOT NULL AUTO_INCREMENT,
  task_title VARCHAR(255) NOT NULL,
  task_description TEXT,
  status_id INT NOT NULL,
  assigned_to INT,
  project_id INT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (task_id),
  KEY status_id (status_id),
  KEY assigned_to (assigned_to),
  KEY project_id (project_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table structure for table users
CREATE TABLE IF NOT EXISTS users (
  user_id INT NOT NULL AUTO_INCREMENT,
  user_firstname VARCHAR(255) NOT NULL,
  user_lastname VARCHAR(255) NOT NULL,
  user_email VARCHAR(255) NOT NULL,
  user_password VARCHAR(255) NOT NULL,
  role_id INT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (user_id),
  UNIQUE KEY user_email (user_email),
  KEY role_id (role_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Constraints for table projects
ALTER TABLE projects
  ADD CONSTRAINT projects_ibfk_1 FOREIGN KEY (created_by) REFERENCES users (user_id);

-- Constraints for table project_members
ALTER TABLE project_members
  ADD CONSTRAINT project_members_ibfk_1 FOREIGN KEY (project_id) REFERENCES projects (project_id),
  ADD CONSTRAINT project_members_ibfk_2 FOREIGN KEY (user_id) REFERENCES users (user_id);

-- Constraints for table tasks
ALTER TABLE tasks
  ADD CONSTRAINT tasks_ibfk_1 FOREIGN KEY (status_id) REFERENCES status (status_id),
  ADD CONSTRAINT tasks_ibfk_2 FOREIGN KEY (assigned_to) REFERENCES users (user_id),
  ADD CONSTRAINT tasks_ibfk_3 FOREIGN KEY (project_id) REFERENCES projects (project_id);

-- Constraints for table users
ALTER TABLE users
  ADD CONSTRAINT users_ibfk_1 FOREIGN KEY (role_id) REFERENCES roles (role_id);

-- Insert an Admin user only if it doesn't exist
INSERT IGNORE INTO users (user_firstname, user_lastname, user_email, user_password, role_id) 
VALUES ('Admin', 'User', 'admin@example.com', SHA2('AdminPassword123!', 256), 1);
select * from  users;

SELECT user_email, user_password FROM users WHERE user_email = 'admin@example.com';
UPDATE users 
SET user_password = 'pbkdf2:sha256:1000000$cTzZGfNCwgkXvEle$e38c7dc4170b4d97f2d4f9636517c26a9bd0459760da0cb16af99ac7d98834f0'
WHERE user_email = 'admin@example.com';

-- admin@example.com

-- AdminPassword123!