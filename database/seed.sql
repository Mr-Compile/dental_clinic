-- Mirasol Dental Center — seed data
-- Passwords below are plaintext for first login only; the app rehashes them
-- with scrypt automatically on first successful sign-in.

SET NAMES utf8mb4;

INSERT INTO `users` (`username`, `email`, `password`, `phone_number`, `role`) VALUES
('Admin', 'admin@dental.com', 'admin123', '09123456789', 'admin'),
('Staff', 'staff@dental.com', 'staff123', '09123456788', 'staff'),
('Client', 'client@dental.com', 'client123', '09654207442', 'client');

INSERT INTO `appointments` (`user_id`, `service`, `appointment_date`, `appointment_time`, `status`) VALUES
(3, 'Braces Consultation', '2025-05-12', '09:00:00', 'cancelled'),
(3, 'Filling', '2025-05-20', '10:00:00', 'confirmed'),
(3, 'Braces Consultation', '2025-05-23', '15:00:00', 'confirmed');
