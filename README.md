Access Key Manager

Welcome to Access Key Manager, a web application designed to streamline access key management for schools using Micro-Focus Inc.'s multitenant school management platform.

Project Overview

Access Key Manager provides a user-friendly interface for School IT Personnel to purchase access keys, manage key status, and ensure smooth operations for their institution. Additionally, Micro-Focus Admins have access to administrative tools for key revocation, status tracking, and integration endpoints.

Features

School IT Personnel


Sign up and log in with email and password, with account verification and reset password feature to recover lost passwords.

View a list of all access keys, including active, expired, or revoked keys.

View status, date of procurement, and expiry date for each access key.

The creation of new keys is resricted if an active key is already assigned.

Micro-Focus Admin

Log in with email and password.

Manually revoke access keys.

View all access keys generated on the platform, including status, procurement date, and expiry date.

Access an endpoint to retrieve details of active keys for a provided school email.

Get Active Key Details:

This endpoint allows you to retrieve the details of an active access key for a given school email.

URL: `/api/get_key_details/`

Method: `GET`

Query Parameters:
`school_email` (required): The email address associated with the school account.

Success Response:

Code: 200 OK

Content:
  ```json
  
  
  {
    "status": 200,
    "message": "Active access key found",
    "key": "ABC123DEF456GHI7",
    "date_of_procurement": "2023-06-01",
    "expiry_date": "2023-06-30"
  }

Error Response:

Code: 404 
Content:

{
  "status": 404,
  "message": "No active key found"
}

Technologies Used

Frontend: HTML, CSS (with Tailwind CSS framework), JavaScript
Backend: Django (Python web framework)
Database: SQLite


Setup Instructions

Clone the repository to your local machine.
Install dependencies using pip install -r requirements.txt.
Set up environment variables (e.g., database credentials, secret keys).
Run migrations to initialize the database schema: python manage.py migrate.
Start the development server: python manage.py runserver.
Access the application in your web browser at http://localhost:8000.

Deployment

The application is deployed at https://accesskeymanager.pythonanywhere.com
