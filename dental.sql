-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 24, 2025 at 11:48 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `dental`
--

-- --------------------------------------------------------

--
-- Table structure for table `appointments`
--

CREATE TABLE `appointments` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `service` varchar(100) NOT NULL,
  `appointment_date` date NOT NULL,
  `appointment_time` time NOT NULL,
  `status` enum('pending','confirmed','completed','cancelled') DEFAULT 'pending'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `appointments`
--

INSERT INTO `appointments` (`id`, `user_id`, `service`, `appointment_date`, `appointment_time`, `status`) VALUES
(1, 3, 'Braces Consultation', '2025-05-12', '09:00:00', 'cancelled'),
(2, 3, 'Filling', '2025-05-20', '10:00:00', 'confirmed'),
(3, 3, 'Braces Consultation', '2025-05-23', '15:00:00', 'confirmed');

-- --------------------------------------------------------

--
-- Table structure for table `reports`
--

CREATE TABLE `reports` (
  `report_id` int(11) NOT NULL,
  `staff_id` int(11) NOT NULL,
  `report_type` varchar(100) NOT NULL,
  `generated_date` datetime NOT NULL DEFAULT current_timestamp(),
  `description` text NOT NULL,
  `report_data` longtext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `reports`
--

INSERT INTO `reports` (`report_id`, `staff_id`, `report_type`, `generated_date`, `description`, `report_data`) VALUES
(6, 2, 'Appointments Report', '2025-05-10 00:41:54', 'Appointments report generated with filters: Date=All, Status=All, Client Search=', '{\"filename\": \"reports\\\\appointments_report_20250510_004154.pdf\", \"filters\": {\"date_filter\": \"All\", \"status_filter\": \"All\", \"client_search\": \"\"}, \"appointments\": [{\"id\": 1, \"appointment_date\": \"2025-05-12\", \"appointment_time\": \"09:00:00\", \"username\": \"Client\", \"service\": \"Braces Consultation\", \"phone_number\": \"09654207442\", \"status\": \"cancelled\"}], \"generated_at\": \"2025-05-10 00:41:54\"}'),
(7, 2, 'Appointments Report', '2025-05-10 07:26:45', 'Appointments report generated with filters: Date=All, Status=All, Client Search=', '{\"filename\": \"reports\\\\appointments_report_20250510_072645.pdf\", \"filters\": {\"date_filter\": \"All\", \"status_filter\": \"All\", \"client_search\": \"\"}, \"appointments\": [{\"id\": 3, \"appointment_date\": \"2025-05-31\", \"appointment_time\": \"13:00:00\", \"username\": \"Client\", \"service\": \"Braces Consultation\", \"phone_number\": \"09654207442\", \"status\": \"pending\"}, {\"id\": 2, \"appointment_date\": \"2025-05-20\", \"appointment_time\": \"15:00:00\", \"username\": \"Client\", \"service\": \"Filling\", \"phone_number\": \"09654207442\", \"status\": \"pending\"}, {\"id\": 1, \"appointment_date\": \"2025-05-12\", \"appointment_time\": \"09:00:00\", \"username\": \"Client\", \"service\": \"Braces Consultation\", \"phone_number\": \"09654207442\", \"status\": \"cancelled\"}], \"generated_at\": \"2025-05-10 07:26:45\"}'),
(8, 2, 'Appointments Report', '2025-05-10 07:31:13', 'Appointments report generated with filters: Date=All, Status=All, Client Search=', '{\"filename\": \"reports\\\\appointments_report_20250510_073113.pdf\", \"filters\": {\"date_filter\": \"All\", \"status_filter\": \"All\", \"client_search\": \"\"}, \"appointments\": [{\"id\": 3, \"appointment_date\": \"2025-05-31\", \"appointment_time\": \"13:00:00\", \"username\": \"Client\", \"service\": \"Braces Consultation\", \"phone_number\": \"09654207442\", \"status\": \"pending\"}, {\"id\": 1, \"appointment_date\": \"2025-05-12\", \"appointment_time\": \"09:00:00\", \"username\": \"Client\", \"service\": \"Braces Consultation\", \"phone_number\": \"09654207442\", \"status\": \"cancelled\"}, {\"id\": 2, \"appointment_date\": \"2025-05-10\", \"appointment_time\": \"10:00:00\", \"username\": \"Client\", \"service\": \"Filling\", \"phone_number\": \"09654207442\", \"status\": \"confirmed\"}], \"generated_at\": \"2025-05-10 07:31:13\"}'),
(9, 2, 'Appointments Report', '2025-05-10 07:32:30', 'Appointments report generated with filters: Date=All, Status=All, Client Search=', '{\"filename\": \"reports\\\\appointments_report_20250510_073230.pdf\", \"filters\": {\"date_filter\": \"All\", \"status_filter\": \"All\", \"client_search\": \"\"}, \"appointments\": [{\"id\": 3, \"appointment_date\": \"2025-05-31\", \"appointment_time\": \"13:00:00\", \"username\": \"Client\", \"service\": \"Braces Consultation\", \"phone_number\": \"09654207442\", \"status\": \"pending\"}, {\"id\": 1, \"appointment_date\": \"2025-05-12\", \"appointment_time\": \"09:00:00\", \"username\": \"Client\", \"service\": \"Braces Consultation\", \"phone_number\": \"09654207442\", \"status\": \"cancelled\"}, {\"id\": 2, \"appointment_date\": \"2025-05-10\", \"appointment_time\": \"10:00:00\", \"username\": \"Client\", \"service\": \"Filling\", \"phone_number\": \"09654207442\", \"status\": \"confirmed\"}], \"generated_at\": \"2025-05-10 07:32:30\"}'),
(10, 2, 'Appointments Report', '2025-05-11 09:12:44', 'Appointments report generated with filters: Date=All, Status=All, Client Search=', '{\"filename\": \"reports\\\\appointments_report_20250511_091244.pdf\", \"filters\": {\"date_filter\": \"All\", \"status_filter\": \"All\", \"client_search\": \"\"}, \"appointments\": [{\"id\": 3, \"appointment_date\": \"2025-05-31\", \"appointment_time\": \"13:00:00\", \"username\": \"Client\", \"service\": \"Braces Consultation\", \"phone_number\": \"09654207442\", \"status\": \"pending\"}, {\"id\": 1, \"appointment_date\": \"2025-05-12\", \"appointment_time\": \"09:00:00\", \"username\": \"Client\", \"service\": \"Braces Consultation\", \"phone_number\": \"09654207442\", \"status\": \"cancelled\"}, {\"id\": 2, \"appointment_date\": \"2025-05-10\", \"appointment_time\": \"10:00:00\", \"username\": \"Client\", \"service\": \"Filling\", \"phone_number\": \"09654207442\", \"status\": \"confirmed\"}], \"generated_at\": \"2025-05-11 09:12:44\"}'),
(11, 2, 'Appointments Report', '2025-05-18 20:42:03', 'Appointments report generated with filters: Date=All, Status=All, Client Search=', '{\"filename\": \"reports\\\\appointments_report_20250518_204203.pdf\", \"filters\": {\"date_filter\": \"All\", \"status_filter\": \"All\", \"client_search\": \"\"}, \"appointments\": [{\"id\": 3, \"appointment_date\": \"2025-05-23\", \"appointment_time\": \"15:00:00\", \"username\": \"Client\", \"service\": \"Braces Consultation\", \"phone_number\": \"09654207442\", \"status\": \"pending\"}, {\"id\": 2, \"appointment_date\": \"2025-05-20\", \"appointment_time\": \"10:00:00\", \"username\": \"Client\", \"service\": \"Filling\", \"phone_number\": \"09654207442\", \"status\": \"confirmed\"}, {\"id\": 1, \"appointment_date\": \"2025-05-12\", \"appointment_time\": \"09:00:00\", \"username\": \"Client\", \"service\": \"Braces Consultation\", \"phone_number\": \"09654207442\", \"status\": \"cancelled\"}], \"generated_at\": \"2025-05-18 20:42:03\"}');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `phone_number` varchar(11) NOT NULL,
  `role` enum('client','staff','admin') DEFAULT 'client',
  `booking_allowed` tinyint(1) GENERATED ALWAYS AS (`role` = 'client') STORED
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `email`, `password`, `phone_number`, `role`) VALUES
(1, 'Admin', 'admin@dental.com', 'admin123', '09123456789', 'admin'),
(2, 'Staff', 'staff@dental.com', 'staff123', '09123456788', 'staff'),
(3, 'Client', 'client@dental.com', 'client123', '09654207442', 'client');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `appointments`
--
ALTER TABLE `appointments`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `reports`
--
ALTER TABLE `reports`
  ADD PRIMARY KEY (`report_id`),
  ADD KEY `staff_id` (`staff_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `appointments`
--
ALTER TABLE `appointments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `reports`
--
ALTER TABLE `reports`
  MODIFY `report_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `appointments`
--
ALTER TABLE `appointments`
  ADD CONSTRAINT `appointments_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `reports`
--
ALTER TABLE `reports`
  ADD CONSTRAINT `reports_ibfk_1` FOREIGN KEY (`staff_id`) REFERENCES `users` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
