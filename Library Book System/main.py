from fastapi import FastAPI, Query, Response, status
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

# Data
books = [
    {"id": 1, "title": "Python Basics", "author": "John", "genre": "Tech", "is_available": True},
    {"id": 2, "title": "History of India", "author": "Raj", "genre": "History", "is_available": True},
    {"id": 3, "title": "Physics 101", "author": "Albert", "genre": "Science", "is_available": False},
    {"id": 4, "title": "Fiction World", "author": "Alice", "genre": "Fiction", "is_available": True},
    {"id": 5, "title": "Chemistry Lab", "author": "Marie", "genre": "Science", "is_available": True},
    {"id": 6, "title": "Advanced JS", "author": "Brendan", "genre": "Tech", "is_available": False},
]

borrow_records = []
record_counter = 1

queue = []

# Models
class BorrowRequest(BaseModel):
    member_name: str = Field(..., min_length=2)
    book_id: int = Field(..., gt=0)
    borrow_days: int = Field(..., gt=0, le=30)
    member_id: str = Field(..., min_length=4)
    member_type: str = "regular"

class NewBook(BaseModel):
    title: str = Field(..., min_length=2)
    author: str = Field(..., min_length=2)
    genre: str = Field(..., min_length=2)
    is_available: bool = True

# Helpers
def find_book(book_id):
    for b in books:
        if b["id"] == book_id:
            return b
    return None

def calculate_due_date(days, member_type):
    if member_type == "premium":
        days = min(days, 60)
    else:
        days = min(days, 30)
    return f"Return by Day {10 + days}"

def filter_books_logic(genre=None, author=None, is_available=None):
    result = books
    if genre is not None:
        result = [b for b in result if b["genre"].lower() == genre.lower()]
    if author is not None:
        result = [b for b in result if author.lower() in b["author"].lower()]
    if is_available is not None:
        result = [b for b in result if b["is_available"] == is_available]
    return result

# Routes

@app.get("/")
def home():
    return {"message": "Welcome to City Public Library"}

@app.get("/books")
def get_books():
    return {
        "total": len(books),
        "available_count": len([b for b in books if b["is_available"]]),
        "books": books
    }

@app.get("/books/summary")
def summary():
    genre_count = {}
    for b in books:
        genre_count[b["genre"]] = genre_count.get(b["genre"], 0) + 1
    return {
        "total": len(books),
        "available": len([b for b in books if b["is_available"]]),
        "borrowed": len([b for b in books if not b["is_available"]]),
        "genres": genre_count
    }

@app.get("/books/filter")
def filter_books(genre: Optional[str] = None, author: Optional[str] = None, is_available: Optional[bool] = None):
    result = filter_books_logic(genre, author, is_available)
    return {"count": len(result), "books": result}

@app.get("/books/search")
def search_books(keyword: str):
    result = [b for b in books if keyword.lower() in b["title"].lower() or keyword.lower() in b["author"].lower()]
    return {"total_found": len(result), "books": result}

@app.get("/books/sort")
def sort_books(sort_by: str = "title", order: str = "asc"):
    if sort_by not in ["title", "author", "genre"]:
        return {"error": "invalid sort_by"}
    if order not in ["asc", "desc"]:
        return {"error": "invalid order"}
    sorted_books = sorted(books, key=lambda x: x[sort_by], reverse=(order=="desc"))
    return {"books": sorted_books}

@app.get("/books/page")
def paginate(page: int = 1, limit: int = 3):
    start = (page-1)*limit
    total = len(books)
    return {
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": (total + limit - 1)//limit,
        "books": books[start:start+limit]
    }

@app.get("/books/browse")
def browse(keyword: Optional[str]=None, sort_by: str="title", order: str="asc", page: int=1, limit: int=3):
    result = books

    if keyword:
        result = [b for b in result if keyword.lower() in b["title"].lower() or keyword.lower() in b["author"].lower()]

    if sort_by in ["title","author","genre"]:
        result = sorted(result, key=lambda x: x[sort_by], reverse=(order=="desc"))

    total = len(result)
    start = (page-1)*limit
    result = result[start:start+limit]

    return {
        "total": total,
        "page": page,
        "books": result
    }

@app.get("/books/{book_id}")
def get_book(book_id: int):
    book = find_book(book_id)
    if not book:
        return {"error": "Book not found"}
    return book

@app.get("/borrow-records")
def get_records():
    return {"total": len(borrow_records), "records": borrow_records}

@app.get("/borrow-records/search")
def search_records(member_name: str):
    result = [r for r in borrow_records if member_name.lower() in r["member_name"].lower()]
    return {"count": len(result), "records": result}

@app.get("/borrow-records/page")
def page_records(page: int=1, limit: int=3):
    start = (page-1)*limit
    total = len(borrow_records)
    return {
        "page": page,
        "total": total,
        "records": borrow_records[start:start+limit]
    }

@app.post("/borrow")
def borrow(data: BorrowRequest):
    global record_counter

    book = find_book(data.book_id)
    if not book:
        return {"error": "Book not found"}
    if not book["is_available"]:
        return {"error": "Book already borrowed"}

    book["is_available"] = False

    record = {
        "record_id": record_counter,
        "member_name": data.member_name,
        "book_id": data.book_id,
        "due": calculate_due_date(data.borrow_days, data.member_type)
    }

    borrow_records.append(record)
    record_counter += 1

    return record

@app.post("/books")
def add_book(data: NewBook, response: Response):
    for b in books:
        if b["title"].lower() == data.title.lower():
            return {"error": "duplicate title"}

    new = {
        "id": len(books)+1,
        **data.dict()
    }
    books.append(new)
    response.status_code = status.HTTP_201_CREATED
    return new

@app.put("/books/{book_id}")
def update_book(book_id: int, genre: Optional[str]=None, is_available: Optional[bool]=None):
    book = find_book(book_id)
    if not book:
        return {"error": "not found"}

    if genre is not None:
        book["genre"] = genre
    if is_available is not None:
        book["is_available"] = is_available

    return book

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    book = find_book(book_id)
    if not book:
        return {"error": "not found"}
    books.remove(book)
    return {"message": f"{book['title']} deleted"}

@app.post("/queue/add")
def add_queue(member_name: str, book_id: int):
    book = find_book(book_id)
    if not book:
        return {"error": "not found"}
    if book["is_available"]:
        return {"error": "book available"}

    queue.append({"member_name": member_name, "book_id": book_id})
    return {"message": "added to queue"}

@app.get("/queue")
def get_queue():
    return queue

@app.post("/return/{book_id}")
def return_book(book_id: int):
    global record_counter

    book = find_book(book_id)
    if not book:
        return {"error": "not found"}

    book["is_available"] = True

    for q in queue:
        if q["book_id"] == book_id:
            queue.remove(q)
            book["is_available"] = False

            record = {
                "record_id": record_counter,
                "member_name": q["member_name"],
                "book_id": book_id,
                "due": "auto-assigned"
            }
            borrow_records.append(record)
            record_counter += 1

            return {"message": "returned and reassigned"}

    return {"message": "returned and available"}