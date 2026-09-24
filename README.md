# Dental Clinic Management System

A desktop application for managing a dental clinic, built with Python and Tkinter.

## Features

- User authentication (login/register)
- Role-based access control (client, staff, admin)
- Appointment booking and management
- User management (admin only)
- Appointment status tracking
- Filtering and viewing appointments

## Requirements

- Python 3.7 or higher
- MySQL Server
- XAMPP (recommended) or other MySQL server

## Installation

1. Clone the repository or download the source code.

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Set up the MySQL database:
- Start your MySQL server (e.g., through XAMPP)
- Create a database named 'dental'
- The application will automatically create the required tables

## Usage

1. Start the application:
```bash
python dental_app.py
```

2. Register a new account or log in with existing credentials.

3. Different roles have different capabilities:
- **Client**: Book appointments, view and cancel their appointments
- **Staff**: View and manage appointments, update appointment status
- **Admin**: Full access to user management and appointment management

## Default Database Configuration

The application uses the following default database configuration:
- Host: localhost
- User: root
- Password: (empty)
- Database: dental

To change these settings, modify the `setup_database` method in `dental_app.py`.

## File Structure

- `dental_app.py`: Main application file
- `register_frame.py`: Registration form implementation
- `client_dashboard.py`: Client interface
- `staff_dashboard.py`: Staff interface
- `admin_dashboard.py`: Admin interface
- `requirements.txt`: Package dependencies

## Security Features

- Passwords are hashed using Werkzeug's security functions
- Role-based access control
- Input validation and sanitization
- Error handling for database operations

## Contributing

Feel free to submit issues and enhancement requests. 