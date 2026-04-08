CREATE DATABASE IF NOT EXISTS account_db
  DEFAULT CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE account_db;

CREATE TABLE IF NOT EXISTS autostra_strategies (
  id BIGINT NOT NULL AUTO_INCREMENT,
  group_id VARCHAR(100) NOT NULL,
  account_id VARCHAR(100) NOT NULL DEFAULT 'default',
  strategy_name VARCHAR(255) NOT NULL,
  flow_json LONGTEXT NOT NULL,
  is_public TINYINT(1) NOT NULL DEFAULT 0,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_autostra_strategy (group_id, account_id, strategy_name),
  KEY idx_autostra_group (group_id),
  KEY idx_autostra_group_account (group_id, account_id),
  KEY idx_autostra_public (group_id, is_public)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS autostra_public_strategy_mappings (
  id BIGINT NOT NULL AUTO_INCREMENT,
  strategy_id BIGINT NOT NULL,
  group_id VARCHAR(100) NOT NULL,
  strategy_name VARCHAR(255) NOT NULL,
  target_account_id VARCHAR(100) NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_mapping (strategy_id, target_account_id),
  KEY idx_strategy (group_id, strategy_name),
  KEY idx_target_account (group_id, target_account_id),
  FOREIGN KEY (strategy_id) REFERENCES autostra_strategies(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;