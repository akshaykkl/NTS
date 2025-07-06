# 📢 NTS - Notification and Tracking System

**NTS** is a Django-based web application built to streamline communication within a college campus. Designed for faculty to post notifications and for students and staff to easily access them, NTS centralizes announcements and helps avoid communication gaps.

## 🎯 Features

- 📬 **Faculty Notification Dashboard** – Post and manage notifications with categories (e.g., academic, exam, general).
- 👨‍🎓 **Student & Staff Portal** – View relevant notifications based on user type.
- 🔔 **Role-based Access** – Separate login for faculty, students, and staff.
- 📂 **Notification History & Filtering** – Browse past notifications with search and filters.
- 📱 **Mobile-Responsive Interface** – Works across devices for convenient access.

## 🛠️ Tech Stack

- **Backend**: Django (Python)
- **Frontend**: HTML5, CSS3, JavaScript (with Django templates or a modern JS framework)
- **Database**: SQLite (default), easily switchable to PostgreSQL or MySQL
- **Authentication**: Django's built-in user auth system

## 🧑‍💻 Installation

### 🔧 Prerequisites

- Python 3.8+
- pip (Python package manager)
- virtualenv (optional but recommended)

### 📥 Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/nts.git
   cd nts
   ```
Create and activate a virtual environment

```bash

python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
Install dependencies

```bash

pip install -r requirements.txt
```
Apply migrations

```bash

python manage.py makemigrations
python manage.py migrate
```
Create a superuser

```bash
python manage.py createsuperuser
```
Run the development server

```bash
python manage.py runserver
```
Open http://127.0.0.1:8000 in your browser.

🔐 User Roles
Admin – Full control over the app, including user management.

Faculty – Can create, edit, and delete notifications.

Student/Staff – Can only view notifications.

📂 Folder Structure
```php

nts/
├── manage.py
├── nts/                  # Main project settings
├── notifications/        # App for notification handling
│   ├── templates/
│   ├── views.py
│   ├── models.py
│   └── urls.py
├── templates/            # Base HTML templates
└── static/               # Static files (CSS, JS, etc.)
```
✨ Future Enhancements
Email/SMS notification support

Push notifications (PWA)

Department/class-wise filtering

File attachments for notices