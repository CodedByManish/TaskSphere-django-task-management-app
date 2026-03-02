# 🚀 TaskSphere  
### Modern, Scalable & Production-Ready Task Management System

<p align="center">
  <img src="docs/images/logo.png" width="140" alt="TaskSphere Logo"/>
</p>

<p align="center">
  <strong>Organize. Prioritize. Achieve.</strong><br>
  A powerful full-stack Django task management web application.
</p>

---

<p align="center">
  <img src="https://img.shields.io/badge/Django-4.2-092E20?style=for-the-badge&logo=django">
  <img src="https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python">
  <img src="https://img.shields.io/badge/tailwindcss-4.1-7952B3?style=for-the-badge&logo=tailwindcss">
  <img src="https://img.shields.io/badge/PostgreSQL-Production-336791?style=for-the-badge&logo=postgresql">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge">
</p>

---

# 📌 Table of Contents

- [Overview](#-overview)
- [Live Demo](#-live-demo)
- [Screenshots](#-screenshots)
- [Features](#-features)
- [Architecture](#-system-architecture)
- [Database Schema](#-database-schema)
- [Technology Stack](#-technology-stack)
- [Installation](#-installation)
- [Docker Setup](#-docker-setup)
- [Environment Variables](#-environment-variables)
- [API Documentation](#-api-documentation)
- [Security](#-security)
- [Performance Considerations](#-performance-considerations)
- [Deployment Guide](#-production-deployment)
- [CI/CD Integration](#-cicd)
- [Testing](#-testing)
- [Future Roadmap](#-future-roadmap)
- [Contributing](#-contributing)
- [License](#-license)

---

# 🌟 Overview

**TaskSphere** is a production-ready task management web application built with Django that allows users to efficiently create, manage, prioritize, and track tasks with a modern responsive interface.

It is designed with:

- Clean architecture
- Scalable backend
- Production deployment support
- Secure authentication
- Responsive UI
- Modular Django apps

---

# 🌐 Live Demo

> Add your deployed link here

```
https://tasksphere-anzd.onrender.com
```

---


---

# 📸 screenshots

### 🔐 Authentication
| Login (Light) | Login (Dark) | Register (Light) | Register (Dark) |
| :---: | :---: | :---: | :---: |
| <img src="docs/images/login1.png" width="220"> | <img src="docs/images/login2.png" width="220"> | <img src="docs/images/register1.png" width="220"> | <img src="docs/images/register2.png" width="220"> |

---

### 🏠 Home & Dashboard
| Home (Light) | Home (Dark) | Dash (Light) | Dash (Dark) |
| :---: | :---: | :---: | :---: |
| <img src="docs/images/home1.png" width="220"> | <img src="docs/images/home2.png" width="220"> | <img src="docs/images/dashboard1.png" width="220"> | <img src="docs/images/dashboard2.png" width="220"> |

---

### 📝 Task Management
| Add (Light) | Add (Dark) | Edit (Light) | Edit (Dark) |
| :---: | :---: | :---: | :---: |
| <img src="docs/images/add_task1.png" width="220"> | <img src="docs/images/add_task2.png" width="220"> | <img src="docs/images/edit_task1.png" width="220"> | <img src="docs/images/edit_task2.png" width="220"> |

---

# ✨ Features

## 🔐 Authentication & Profiles
- User Registration
- Secure Login / Logout
- Email Verification
- Profile Auto Creation (Django Signals)
- Avatar Upload
- Bio Management
- Password Reset

---

## 📋 Task Management
- Create / Edit / Delete Tasks
- Set Priority (Low, Medium, High)
- Assign Due Dates
- Overdue Indicators
- Task Completion Timestamp
- Soft Status Tracking:
  - To Do
  - In Progress
  - Completed

---

## 🔎 Filtering & Search
- Search by title
- Filter by priority
- Filter by status
- Filter overdue tasks

---

## 📊 Dashboard Analytics
- Total Tasks
- Completed Tasks
- Pending Tasks
- Overdue Tasks
- Completion Rate %

---

## 🎨 UI & UX
- Bootstrap 5
- Fully Responsive
- Clean Card Layout
- Toast Notifications
- Dark Mode Toggle
- Interactive Forms

---

# 🏗 System Architecture

```
Client (Browser)
     │
     ▼
Django Views
     │
     ▼
Service Layer (Business Logic)
     │
     ▼
Models (ORM)
     │
     ▼
Database (SQLite / PostgreSQL)
```

---

## 🔹 Architecture Pattern

- MTV (Model-Template-View)
- Modular Django apps:
  - `accounts`
  - `tasks`
- Separation of concerns
- Environment-based configuration
- Production ready structure

---

# 🗄 Database Schema

## 🔹 User Model (Django Default)

| Field | Type |
|-------|------|
| username | CharField |
| email | EmailField |
| password | Hashed |

---

## 🔹 Profile Model

| Field | Type |
|-------|------|
| user | OneToOneField(User) |
| avatar | ImageField |
| bio | TextField |
| created_at | DateTime |

---

## 🔹 Task Model

| Field | Type |
|-------|------|
| user | ForeignKey(User) |
| title | CharField |
| description | TextField |
| status | CharField |
| priority | CharField |
| due_date | DateField |
| completed_at | DateTime |
| created_at | DateTime |

---

## 🔹 ER Relationship

User  
⬇ (One-to-One)  
Profile  

User  
⬇ (One-to-Many)  
Task  

---

# 🛠 Technology Stack

### Backend
- Django 4.2
- Python 3.9+

### Frontend
- HTML5
- tailwindcss
- JavaScript

### Database
- SQLite (Development)
- PostgreSQL (Production)

### Deployment
- Gunicorn
- WhiteNoise

---

# ⚙️ Installation

## 1️⃣ Clone Repository

```bash
git clone https://github.com/yourusername/tasksphere.git
cd tasksphere
```

## 2️⃣ Virtual Environment

```bash
python -m venv env
source env/bin/activate
```

## 3️⃣ Install Requirements

```bash
pip install -r requirements.txt
```

## 4️⃣ Environment Setup

Create `.env`

```
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

## 5️⃣ Run Migrations

```bash
python manage.py migrate
```

## 6️⃣ Create Superuser

```bash
python manage.py createsuperuser
```

## 7️⃣ Run Server

```bash
python manage.py runserver
```

---

# 🐳 Docker Setup

```bash
docker-compose up --build
```

Access:

```
http://localhost:8000
```

---

# 🔐 Environment Variables

| Variable | Description |
|----------|------------|
| SECRET_KEY | Django secret key |
| DEBUG | Debug mode |
| ALLOWED_HOSTS | Production hosts |
| DATABASE_URL | Database URL |
| EMAIL_HOST | SMTP server |
| EMAIL_PORT | SMTP port |

---

# 📡 API Documentation

## Get All Tasks

```
GET /tasks/api/tasks/
```

## Get Task Detail

```
GET /tasks/api/task/<id>/
```

## Update Status

```
PATCH /tasks/api/task/<id>/status/
```

## Dashboard Statistics

```
GET /tasks/api/statistics/
```

---

# 🔒 Security

- CSRF Protection
- LoginRequiredMixin
- Secure Password Hashing
- Environment Variables
- DEBUG=False in production
- Secure Cookies
- XSS Protection via Django templates

---

# ⚡ Performance Considerations

- Query Optimization using `select_related`
- Static file compression
- WhiteNoise for static serving
- Database indexing (user + status)
- Pagination support

---

# 🚀 Production Deployment

## 🔹 Render Deployment

1. Push to GitHub
2. Create Web Service
3. Add Environment Variables
4. Set Build Command:
   ```
   pip install -r requirements.txt
   ```
5. Start Command:
   ```
   gunicorn tasksphere.wsgi:application
   ```

---

## 🔹 Production Checklist

- DEBUG=False
- Set ALLOWED_HOSTS
- Use PostgreSQL
- Collect Static Files
- Configure HTTPS

---

# 🔄 CI/CD

Example GitHub Actions workflow:

`.github/workflows/django.yml`

```yaml
name: Django CI

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run Tests
        run: python manage.py test
```

---

# 🧪 Testing

Run tests:

```bash
python manage.py test
```

---

# 🗺 Future Roadmap

- Django REST Framework integration
- Task Categories
- Task Sharing
- Real-time notifications
- Email reminders
- Calendar integration
- AI-powered task prioritization

---

# 🤝 Contributing

1. Fork repository
2. Create branch
3. Commit changes
4. Push branch
5. Create Pull Request

---

# 📄 License

MIT License

---

# 👨‍💻 Author

**Manish Kafle**  
Django Developer | IT Student  

---

# ⭐ Show Your Support

If you like this project:

- ⭐ Star this repository
- 🍴 Fork it
- 📢 Share it
- 💡 Suggest improvements

---

<p align="center">
  *** Built using Django ***
</p>





---
---
# How to Connect to Your Render PostgreSQL
---

1. Open **pgAdmin**.
2. Right-click **Servers → Register → Server...**

### General Tab
- **Name:** `TaskSphere_Production`

### Connection Tab
Use your database URL:
`postgresql://manish:YOUR_PASSWORD@dpg-d6ijm8juibrs73ad8610-a.oregon-postgres.render.com/taskspare_db`

Fill in:
- **Host name/address:** `dpg-d6ijm8juibrs73ad8610-a.oregon-postgres.render.com`
- **Port:** `5432`
- **Maintenance database:** `taskspare_db`
- **Username:** `manish`
- **Password:** `YOUR_PASSWORD`
- ✅ Check **Save password**

Click **Save**.

Your Render PostgreSQL database is now connected.