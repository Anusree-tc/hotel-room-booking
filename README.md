# LuxeStay – Hotel Room Booking System

## Project Overview

LuxeStay is a Django-based Hotel Room Booking System that allows guests to explore hotel rooms, check room availability, and make reservations online.

The system also provides staff management features to manage rooms, bookings, and hotel operations.

## Features

### Guest Features
- View available hotel rooms.
- Search rooms based on check-in and check-out dates.
- Check room availability.
- Book hotel rooms.
- View booking details.
- View booking history.
- Guest profile management.
- Cancel bookings according to booking rules.

### Staff Features
- Staff login.
- Staff dashboard.
- Manage rooms and bookings.
- View booking reports.
- Manage booking status.

### Security Features
- Environment variables for SECRET_KEY and DEBUG.
- Booking reference code.
- Double-booking prevention.
- Booking date validation.
- Login attempt protection using Django Axes.

## Technologies Used

- Python
- Django
- SQLite
- HTML
- CSS
- Bootstrap 5
- JavaScript

## Project Structure


LuxeStay/
│
├── home/
├── rooms/
├── staff/
├── templates/
│   ├── rooms/
│   ├── staff/
│   ├── home.html
│   └── base.html
│
├── static/
│   └── css/
│
├── media/
├── manage.py
├── db.sqlite3
├── requirements.txt
├── .env
└── .gitignore


## Installation and Setup

### 1. Clone the Repository

git clone YOUR_GITHUB_REPOSITORY_URL


### 2. Open the Project Folder

cd LuxeStay


### 3. Create a Virtual Environment


python -m venv venv


### 4. Activate Virtual Environment

Windows:


venv\Scripts\activate


### 5. Install Dependencies


pip install -r requirements.txt


### 6. Configure Environment Variables

Create a `.env` file in the project root directory.

Add:


SECRET_KEY=your-secret-key
DEBUG=True


Generate your own Django secret key before running the project.

### 7. Apply Migrations


python manage.py migrate


### 8. Run the Development Server

python manage.py runserver


Open your browser:


http://127.0.0.1:8000/


## Database

This project uses SQLite as its database.

## Project Purpose

This project was developed as a Python Full Stack Development project to demonstrate Django development, database management, CRUD operations, form validation, booking management, and authentication security.

## Author

**Anusree T C**