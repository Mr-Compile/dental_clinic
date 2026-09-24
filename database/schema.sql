-- Mirasol Dental Center — schema
-- Compatible with MySQL 8.4+ and MariaDB 10.4+
-- The app also creates/migrates these tables on startup (dental_app/core/database.py);
-- this file is for manual provisioning and fresh installs.

SET NAMES utf8mb4;

CREATE TABLE IF NOT EXISTS `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,           -- scrypt hash (legacy plaintext auto-upgrades on login)
  `phone_number` varchar(11) NOT NULL,
  `role` enum('client','staff','admin') DEFAULT 'client',
  `booking_allowed` tinyint GENERATED ALWAYS AS (`role` = 'client') STORED,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `uq_phone_number` (`phone_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE IF NOT EXISTS `appointments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `service` varchar(100) NOT NULL,
  `appointment_date` date NOT NULL,
  `appointment_time` time NOT NULL,
  `status` enum('pending','confirmed','completed','cancelled') DEFAULT 'pending',
  -- NULL for inactive rows, so the UNIQUE key only blocks double-booked active slots
  `active_slot` varchar(32) GENERATED ALWAYS AS (
    IF(`status` IN ('pending','confirmed'),
       CONCAT(`appointment_date`, ' ', `appointment_time`), NULL)
  ) STORED,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_active_slot` (`active_slot`),
  KEY `idx_appointment_date` (`appointment_date`),
  KEY `idx_status` (`status`),
  CONSTRAINT `appointments_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE IF NOT EXISTS `reports` (
  `report_id` int NOT NULL AUTO_INCREMENT,
  `staff_id` int NOT NULL,
  `report_type` varchar(100) NOT NULL,
  `generated_date` datetime NOT NULL DEFAULT current_timestamp(),
  `description` text NOT NULL,
  `report_data` longtext NOT NULL,             -- JSON: filename, filters, rows
  PRIMARY KEY (`report_id`),
  KEY `staff_id` (`staff_id`),
  CONSTRAINT `reports_ibfk_1` FOREIGN KEY (`staff_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
