# 📚 Library Book System (FastAPI)

A simple Library Management Backend built using **FastAPI**.
This project allows users to manage books, borrow them, handle queues, and perform search, sorting, and pagination.

---

## 🚀 Features

- 📖 View all books and details
- ➕ Add new books
- ✏️ Update book information
- ❌ Delete books
- 📦 Borrow and return books
- ⏳ Queue system for unavailable books
- 🔍 Search books by title/author
- 🔃 Sort books
- 📄 Pagination support
- 📊 Summary and filtering

---

## 🧠 Concepts Covered

This project covers all major FastAPI concepts:

- GET APIs (fetch data)
- POST APIs with Pydantic validation
- Helper functions
- CRUD operations
- Multi-step workflow (borrow → return → queue)
- Search, Sort, Pagination

---

## 📁 Project Structure

```
main.py   # Complete FastAPI backend
README.md # Project documentation
```

---

## ▶️ How to Run

1. Install dependencies:

```
pip install fastapi uvicorn
```

2. Run the server:

```
uvicorn main:app --reload
```

3. Open Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

## 📌 API Overview

### 🏠 Basic Routes

- `GET /` → Welcome message

### 📚 Book Routes

- `GET /books` → All books
- `GET /books/{id}` → Single book
- `POST /books` → Add book
- `PUT /books/{id}` → Update book
- `DELETE /books/{id}` → Delete book

### 🔍 Advanced Book Features

- `GET /books/filter` → Filter books
- `GET /books/search` → Search books
- `GET /books/sort` → Sort books
- `GET /books/page` → Pagination
- `GET /books/browse` → Combined filter + sort + pagination

### 📦 Borrow System

- `POST /borrow` → Borrow a book
- `GET /borrow-records` → View borrow records
- `GET /borrow-records/search` → Search records
- `GET /borrow-records/page` → Paginate records

### ⏳ Queue System

- `POST /queue/add` → Add to queue
- `GET /queue` → View queue

### 🔄 Return Workflow

- `POST /return/{book_id}` → Return book and auto-assign to next user

---

## 🧪 Testing

All endpoints are tested using **Swagger UI**.
You can test:

- Valid inputs
- Invalid inputs (to check validation)
- Edge cases like unavailable books

---

## 🎯 Key Highlights

- Clean and simple code structure
- Uses in-memory data (no database)
- Covers real-world backend logic
- Beginner-friendly implementation

---

## 📌 Notes

- Data is not persistent (resets on server restart)
- No authentication included
- Designed for learning and demonstration purposes

---

## 👨‍💻 Author

Developed as part of FastAPI Internship Final Project.

---
