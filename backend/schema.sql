CREATE DATABASE IF NOT EXISTS account_db DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE account_db;

-- ============================
-- system_users（系统用户）
-- 来源：auth.py
-- ============================
CREATE TABLE IF NOT EXISTS system_users (
    id VARCHAR(64) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);

-- ============================
-- accounts（养号账号）
-- 来源：accounts.py
-- ============================
CREATE TABLE IF NOT EXISTS accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    platform VARCHAR(255),
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(255),
    status VARCHAR(50) DEFAULT 'active',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    tags TEXT,
    account_ip VARCHAR(255),
    account_port INT
);

-- ============================
-- email_accounts（邮箱账号）
-- 来源：email_accounts.py
-- ============================
CREATE TABLE IF NOT EXISTS email_accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email_address VARCHAR(255) NOT NULL,
    email_password VARCHAR(255) NOT NULL,
    protocol VARCHAR(50),
    host VARCHAR(255),
    port INT,
    status VARCHAR(50) DEFAULT 'active',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    tags TEXT
);

-- ============================
-- email_metadata（邮箱验证记录）
-- 来源：email_verify.py
-- ============================
CREATE TABLE IF NOT EXISTS email_metadata (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email_address VARCHAR(255) NOT NULL,
    last_checked DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_valid BOOLEAN DEFAULT NULL,
    message TEXT
);

-- ============================
-- proxy_verify（代理验证记录）
-- 来源：proxy_verify.py
-- ============================
CREATE TABLE IF NOT EXISTS proxy_verify (
    id INT AUTO_INCREMENT PRIMARY KEY,
    proxy VARCHAR(255) NOT NULL,
    last_checked DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_valid BOOLEAN DEFAULT NULL,
    message TEXT
);
