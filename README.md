# FinAudit

FinAudit is a modern personal finance and budgeting web application designed to help users track income, expenses, budgets, savings goals, and financial performance through an intuitive and scalable platform.

The project is built with a separated frontend and backend architecture:

- Frontend: HTML, CSS, JavaScript
- Backend API: Django REST Framework
- Database: PostgreSQL


# Features

## Authentication & User Management
- User registration
- Secure login/logout
- JWT authentication
- User profile management

## Expense Management
- Add, edit, and delete expenses
- Expense categorization
- Recurring expense tracking

## Income Management
- Multiple income source tracking
- Recurring income support

## Budget Management
- Monthly budgeting
- Category-based spending limits
- Budget monitoring and alerts

## Savings Goals
- Savings target creation
- Progress tracking

## Analytics Dashboard
- Income vs expense summaries
- Spending breakdowns
- Financial trend analysis
- Budget utilization insights

## Reports
- Monthly summaries
- Downloadable financial reports
- Transaction history tracking


# Project Structure

FinAudit_App/
│
├── finaudit_backend/
│   ├── apps/
│   ├── config/
│   ├── requirements/
│   ├── manage.py
│
├── docs/
│   ├── index.html
│   ├── css/
│   ├── js/
│   └── assets/
│
├── README.md
└── .gitignore


# Tech Stack

## Backend
- Python
- Django
- Django REST Framework
- PostgreSQL
- JWT Authentication

## Frontend
- HTML
- CSS
- JavaScript

## Deployment
- Frontend: GitHub Pages
- Backend: Render / Railway / VPS


# Backend Setup

## 1. Clone Repository

mkdir FinAudit_App
git clone https://github.com/DannyTechStudio/finaudit_app.git
cd FinAudit_App

## 2. Create Virtual Environment

cd finaudit_backend
python -m venv finaudit_env

## 3. Activate Virtual Environment

### Windows

```powershell
.\finaudit_env\Scripts\Activate.ps1

### Linux / macOS

```bash
source finaudit_env/bin/activate

## 4. Install Dependencies

```bash
pip install -r requirements.txt

---

# MySQL Setup

Create a MySQL database:

```sql
CREATE DATABASE finaudit_db;
```

# Environment Variables

Create a `.env` file inside `finaudit_backend/`.

Example:

```env
SECRET_KEY=your_secret_key
DEBUG=True

DB_NAME=finaudit_db
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306

# Run Migrations

```bash
python manage.py migrate

# Run Development Server

```bash
python manage.py runserver

API will be available at:

```text
http://127.0.0.1:8000/
```

# Frontend Setup

Frontend files are located inside the `docs/` directory.

You can open `index.html` directly in the browser during early development.


# GitHub Pages Deployment

The frontend is designed to be deployed using GitHub Pages.

GitHub Pages will serve the `/docs` directory directly.

Deployment URL format:

```text
https://username.github.io/FinAudit_App/

# API Architecture

The frontend communicates with the backend via REST API requests.

Example:

```javascript
fetch("https://your-api-url.com/api/expenses/")

# Planned API Endpoints

## Authentication

```http
POST /api/auth/register/
POST /api/auth/login/
POST /api/auth/password-reset/
POST /api/auth/logout/
POST /api/auth/refresh/


## Categories

```http
GET /api/categories/
POST /api/categories/
GET /api/categories/{id}/
PUT /api/catgeories/{id}/
DELETE /api/categories/{id}/


## Incomes

```http
GET /api/incomes/
POST /api/incomes/
GET /api/incomes/{id}/
PUT /api/incomes/{id}/
DELETE /api/incomes/{id}/


## Expenses

```http
GET /api/expenses/
POST /api/expenses/
GET /api/expenses/{id}/
PUT /api/expenses/{id}/
DELETE /api/expenses/{id}/


## Budgets

```http
GET    /api/budgets/
POST   /api/budgets/


## Analytics

GET /api/analytics/monthly-summary/
GET /api/analytics/category-breakdown/


# Security

FinAudit implements:
- JWT authentication
- Password hashing
- Environment variable management
- Secure database credentials
- CORS protection
- HTTPS-ready configuration


# Future Improvements

- Mobile application
- AI-powered financial insights
- Bank integrations
- Multi-currency support
- Receipt scanning
- Email notifications
- Advanced analytics

# License

This project is currently under MIT License.

# Author

Developed by Daniel.
