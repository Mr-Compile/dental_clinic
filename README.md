# Mirasol Dental Center — Dental Clinic Management System

A desktop application for managing a dental clinic, built with Python, Tkinter (ttkbootstrap), and MySQL.

## Features

- User authentication (login/register)
- Role-based access control (client, staff, admin)
- Appointment booking and management
- Appointment status tracking (pending, confirmed, completed, cancelled)
- User management (admin only)
- PDF appointment report generation (staff/admin)
- Public clinic landing page

## Requirements

- Python 3.8+
- WAMP (or any MySQL-compatible server) with MySQL running on port 3306
- WAMP also ships MariaDB on port 3307 — the app uses port 3306 by default

## Installation

1. Clone the repository or download the source code.

2. Create a virtual environment (recommended):
```bash
python -m venv venv
venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Create your environment file:
```bash
copy .env.example .env
```
Edit `.env` to set database credentials and your Semaphore SMS API key (leave `SEMAPHORE_API_KEY` empty to disable SMS notifications).

5. Set up the MySQL database (see below).

## Database Setup (WAMP)

1. Start WAMP and confirm the MySQL service is running (port 3306).

2. Create the database:
```bash
C:\wamp64\bin\mysql\mysql8.4.7\bin\mysql.exe -u root -e "CREATE DATABASE dental CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;"
```

3. Import the schema and seed data:
```bash
C:\wamp64\bin\mysql\mysql8.4.7\bin\mysql.exe -u root dental < database\schema.sql
C:\wamp64\bin\mysql\mysql8.4.7\bin\mysql.exe -u root dental < database\seed.sql
```

Alternatively, open phpMyAdmin (http://localhost/phpmyadmin), select the MySQL server, create a `dental` database, and import `database/schema.sql` then `database/seed.sql` from the Import tab.

4. Database access is configured via `.env` (`DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`). Defaults match a stock WAMP install: `root` with an empty password on `localhost:3306`.

The application also auto-creates and migrates all tables on first run if they do not exist — including adding the `reports` table, the `phone_number` unique key, and the `active_slot` unique key on older databases.

## Usage

Start the application:
```bash
python main.py
```

### Default accounts (seeded by database/seed.sql)

| Role   | Email             | Password  |
|--------|-------------------|-----------|
| Admin  | admin@dental.com  | admin123  |
| Staff  | staff@dental.com  | staff123  |
| Client | client@dental.com | client123 |

Seeded passwords are plaintext in the database but are transparently upgraded to a scrypt hash on first login. Change them after first sign-in.

### Role capabilities

- **Client**: Book appointments, view and cancel their own appointments
- **Staff**: View and manage all appointments, update statuses, generate PDF reports
- **Admin**: Full access — user management, appointment management, and reports

## Project Structure

```
dental/
├── main.py                       # Entry point
├── dental_app/                   # Application package
│   ├── app.py                    # Window, service wiring, screen routing
│   ├── core/
│   │   ├── config.py             # .env-based config (DB creds, SMS key, paths)
│   │   └── database.py           # Single shared connection, schema setup/migrations
│   ├── repositories/             # All SQL lives here — views never write queries
│   │   ├── user_repository.py
│   │   ├── appointment_repository.py
│   │   └── report_repository.py
│   ├── services/                 # Business logic
│   │   ├── auth_service.py       # Login/register + scrypt password hashing
│   │   ├── booking_service.py    # Slot availability, book/cancel/reschedule
│   │   ├── sms_service.py        # Semaphore SMS notifications
│   │   └── report_service.py     # PDF generation (reportlab)
│   ├── ui/
│   │   ├── styles.py             # Colors + ttk style config (applied once)
│   │   ├── components/           # Reusable widgets
│   │   │   ├── modal.py          # ModernModal dialog shell
│   │   │   ├── confirm_dialog.py # Yes/no confirmation dialog
│   │   │   ├── logout_dialog.py
│   │   │   ├── stat_card.py      # Dashboard stat card
│   │   │   ├── scrollable_frame.py  # Canvas+scrollbar, leak-free wheel binding
│   │   │   ├── calendar_picker.py   # Month calendar (booking + reschedule)
│   │   │   ├── time_slot_picker.py  # Availability-colored slot grid
│   │   │   └── recent_activity.py   # Recent-activity list
│   │   └── views/
│   │       ├── base_dashboard.py    # Shared dashboard scaffold
│   │       ├── login_view.py
│   │       ├── register_view.py
│   │       ├── landing_view.py
│   │       ├── admin/          # dashboard, users, appointments, reports
│   │       ├── staff/          # dashboard, appointments (+ PDF report)
│   │       └── client/         # dashboard, booking, my appointments
│   └── utils/
│       ├── constants.py        # Services, time slots, statuses, colors
│       ├── validators.py       # Phone/email validation
│       ├── formatting.py       # Time formatting
│       └── images.py           # Circular logo/image loading
├── assets/                     # Images
├── reports/                    # Generated PDFs (gitignored)
├── database/
│   ├── schema.sql              # Table definitions
│   └── seed.sql                # Default accounts + sample appointments
├── docs/                       # Design docs / presentations
├── tests/                      # pytest unit tests
├── .env.example                # Copy to .env and fill in
└── requirements.txt
```

## Security Notes

- Queries use parameterized statements via mysql-connector-python
- Passwords are hashed with scrypt (Werkzeug); legacy plaintext rows upgrade on login
- Role-based access control enforced per dashboard
- `booking_allowed` is a generated column restricting booking to client accounts
- `active_slot` is a generated column with a UNIQUE key — the database itself rejects double-booked active slots
- Secrets (DB password, Semaphore API key) live in `.env`, never in code
- `phone_number` has a UNIQUE constraint in addition to app-level checks
