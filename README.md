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
- MySQL
- JWT Authentication

## Frontend
- HTML
- CSS
- JavaScript

## Deployment
- Frontend: GitHub Pages
- Backend: Render / Railway / VPS

## Entity Relationship Diagram
<img width="781" height="1159" alt="finaudit_ERD drawio" src="https://github.com/user-attachments/assets/738baefe-9b7a-446c-a8ad-04c0dd0907dd" />


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
POST /api/auth/change-password/
POST /api/auth/forgot-password/
POST /api/auth/reset-password/
POST /api/auth/logout/
POST /api/auth/refresh/


## User Details Management

```http
GET /api/users/me/
PATCH /api/users/me/
DELETE /api/users/me/


## Profile

```http
GET /api/profile/
PATCH /api/profile/


## User Settings

```http
GET /api/user/settings/
PATCH /api/user/settings/


## Categories

```http
GET /api/categories/
POST /api/categories/
GET /api/categories/{id}/
PATCH /api/catgeories/{id}/
DELETE /api/categories/{id}/


## Transaction

```http
GET /api/transactions/
POST /api/transactions/
GET /api/transactions/{id}/
PATCH /api/transactions/{id}/
DELETE /api/transactions/{id}/


## Budgets

```http
GET /api/budgets/
POST /api/budgets/
GET /api/budgets/{id}/
PATCH /api/budgets/{id}/
DELETE /api/budgets/{id}/


## Savings Goals

```http
GET /api/savings-goals/
POST /api/savings-goals/
GET /api/savings-goals/{id}/
PATCH /api/savings-goals/{id}/
DELETE /api/savings-goals/{id}/


## Savings Contributions

```http
GET /api/savings-contributions/
POST /api/savings-contributions/
GET /api/savings-contributions/{id}/
PATCH /api/savings-contributions/{id}/
DELETE /api/savings-contributions/{id}/


## Notification

```http
GET /api/notifications/
GET /api/notifications/{id}/
PATCH /api/notifications/{id}/mark-as-read/
PATCH /api/notifications/{id}/mark-all-as-read/
DELETE /api/notifications/{id}/


## Analytics

```http
GET /api/analytics/dashboard/
GET /api/analytics/monthly-summary/
GET /api/analytics/category-breakdown/
GET /api/analytics/cashflow/
GET /api/analytics/budget-performance/
GET /api/analytics/savings-progress/


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
