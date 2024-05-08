Access Key Manager

Welcome to Access Key Manager, a web application designed to streamline access key management for schools using Micro-Focus Inc.'s multitenant school management platform.

Project Overview

Access Key Manager provides a user-friendly interface for School IT Personnel to purchase access keys, manage key status, and ensure smooth operations for their institution. Additionally, Micro-Focus Admins have access to administrative tools for key revocation, status tracking, and integration endpoints.

Features

School IT Personnel


Sign up and log in with email and password, with account verification and reset password feature to recover lost passwords.
View a list of all access keys, including active, expired, or revoked keys.
View status, date of procurement, and expiry date for each access key.
Restrict the creation of new keys if an active key is already assigned.

Micro-Focus Admin

Log in with email and password.
Manually revoke access keys.
View all access keys generated on the platform, including status, procurement date, and expiry date.
Access an endpoint to retrieve details of active keys for a provided school email.

Technologies Used

Frontend: HTML, CSS (with Tailwind CSS framework), JavaScript
Backend: Django (Python web framework)
Database: PostgreSQL
Payment Gateway API(TEST MODE): Paystack (for processing payments)

Setup Instructions

Clone the repository to your local machine.
Install dependencies using pip install -r requirements.txt.
Set up environment variables (e.g., database credentials, secret keys).
Run migrations to initialize the database schema: python manage.py migrate.
Start the development server: python manage.py runserver.
Access the application in your web browser at http://localhost:8000.

Deployment

The application is deployed at https://accesskeymanager.pythonanywhere.com
