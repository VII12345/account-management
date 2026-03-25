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
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_autostra_strategy (group_id, account_id, strategy_name),
  KEY idx_autostra_group (group_id),
  KEY idx_autostra_group_account (group_id, account_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;