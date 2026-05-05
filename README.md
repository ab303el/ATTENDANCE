# ATTENDANCE

------------------------------
## 📅 Smart Attendance Portal
A robust Django-based attendance tracking system featuring automated employee onboarding, role-based dashboards, and a RESTful API for seamless integration.
## 🚀 Key Features

* Role-Based Dashboards:
* Managers (Admins): Full visibility of company-wide attendance logs and late reports.
   * Employees: Personalized view of their own attendance history and simple clock-in/out actions.
* Automated Onboarding: Uses Django Signals to automatically create employee profiles and assign the "Employees" group upon user registration.
* Secure Authentication: Integrated with Django’s session-based auth for the web portal and JWT (JSON Web Tokens) for the API endpoints.
* Modern UI: Built with a clean, responsive interface using Tailwind CSS.
* REST API: Fully documented endpoints for managing attendance and employee records via mobile or third-party apps.

## 🛠️ Tech Stack

* Backend: Python 3.11 / Django 5.x
* Database: PostgreSQL
* API Framework: Django REST Framework (DRF)
* Styling: Tailwind CSS
* Testing: Django TestCase / APITestCase

## 🔧 Quick Setup

   1. Clone the repo & setup VENV:
   
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   
   2. Install dependencies:
   
   pip install django djangorestframework psycopg2-binary
   
   3. Run Migrations:
   
   python manage.py makemigrations
   python manage.py migrate
   
   4. Create Manager Account:
   
   python manage.py createsuperuser
   
   5. Start Server:
   
   python manage.py runserver
   
   
## 🧪 Testing
Run the automated test suite to verify security and API functionality:

python manage.py test

------------------------------


