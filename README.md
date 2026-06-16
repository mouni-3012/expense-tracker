# Expense Tracker

A full-stack Expense Tracker web application built using FastAPI, SQLite, SQLAlchemy, HTML, CSS, and JavaScript.

## Features

* User Registration
* User Login
* Add Expenses
* View Expenses
* Delete Expenses
* Expense Analytics Dashboard
* Responsive UI

## Tech Stack

### Backend

* FastAPI
* SQLAlchemy
* SQLite

### Frontend

* HTML
* CSS
* JavaScript

## Installation

```bash
pip install -r requirements.txt
```

## Run the Application

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/app
```

## Project Structure

```text
expense-tracker/
│
├── app/
│   ├── main.py
│   ├── models.py
│   └── database.py
│
├── static/
│   └── style.css
│
├── templates/
│   ├── index.html
│   └── dashboard.html
│
├── requirements.txt
├── README.md
└── .gitignore
```
