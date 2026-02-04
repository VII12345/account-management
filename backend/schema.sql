-- MySQL schema for account-management backend
-- Generated based on backend usage in accounts.py, auth.py, email_verify.py, proxy_verify.py

CREATE DATABASE IF NOT EXISTS account_db
  DEFAULT CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE account_db;

-- System users for auth
CREATE TABLE IF NOT EXISTS system_users (
  id CHAR(36) NOT NULL,
  email VARCHAR(255) NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_system_users_email (email)
) ENGINE=InnoDB;

-- Accounts CRUD
CREATE TABLE IF NOT EXISTS accounts (
  id BIGINT NOT NULL AUTO_INCREMENT,
  platform VARCHAR(100) NULL,
  username VARCHAR(255) NOT NULL,
  password VARCHAR(255) NOT NULL,
  email VARCHAR(255) NULL,
  phone VARCHAR(50) NULL,
  status VARCHAR(50) NULL DEFAULT 'active',
  tags VARCHAR(255) NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_accounts_platform (platform),
  KEY idx_accounts_username (username)
) ENGINE=InnoDB;

-- Email verification logs
CREATE TABLE IF NOT EXISTS email_accounts (
  id CHAR(36) NOT NULL,
  email_address VARCHAR(255) NOT NULL,
  email_password VARCHAR(255) NOT NULL,
  protocol VARCHAR(32) NOT NULL,
  host VARCHAR(255) NOT NULL,
  port INT NOT NULL,
  last_login_status VARCHAR(32) NOT NULL,
  last_error TEXT NULL,
  proxy_id CHAR(36) NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_email_accounts_email (email_address),
  KEY idx_email_accounts_proxy (proxy_id)
) ENGINE=InnoDB;

-- Proxy verification logs
CREATE TABLE IF NOT EXISTS proxies (
  id CHAR(36) NOT NULL,
  proxy_url VARCHAR(512) NOT NULL,
  last_check_status VARCHAR(32) NOT NULL,
  latency_ms DOUBLE NULL,
  last_error TEXT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id)
) ENGINE=InnoDB;
