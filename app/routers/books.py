from app.database import get_db
from app  import models
from app.schemas import BookCreate

from app import schemas
from fastapi import APIRouter, Depends, HTTPException,Query
from sqlalchemy.orm import Session

router = APIRouter(
    prefix = "/books",
    tags = ["Books"]
)

@router.post("/", response_model=schemas.BookResponse)
def create_book(book : BookCreate, db : Session = Depends(get_db)):

    db_book = models.Book(**book.model_dump())

    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@router.get("/search",response_model=list[schemas.BookResponse])
def search_books(title: str | None = None,
                author: str | None = None,
                price : int | None = None,
                skip : int = Query(default=0, ge=0),
                limit : int = Query(default=10, gt=0),
                db: Session = Depends(get_db)):
    
    query = db.query(models.Book)

    if title:
        query = query.filter(models.Book.title.ilike(f"%{title}%"))

    if author:
        query = query.filter(models.Book.author.ilike(f"%{author}%"))

    if price is not None:
        query = query.filter(models.Book.price == price)

    return query.offset(skip).limit(limit).all()

@router.get("/{book_id}", response_model=schemas.BookResponse)
def get_book_by_id(book_id : int,
                   db: Session = Depends(get_db)):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@router.get("/",response_model=list[schemas.BookResponse])
def view_all_books(skip : int = Query(default=0, ge=0),
                   limit : int = Query(default=10, gt=0),
                   db: Session = Depends(get_db)):
    db_books = db.query(models.Book).offset(skip).limit(limit).all()
    return db_books



@router.put("/{book_id}", response_model=schemas.BookResponse)
def update_book(book_id: int, book: BookCreate, db: Session = Depends(get_db)):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()

    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    db_book.title = book.title
    db_book.author = book.author
    db_book.description = book.description
    db_book.price = book.price

    db.commit()
    db.refresh(db_book)
    return db_book

@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(db_book)
    db.commit()
    return {"msg": "Book deleted successfully"}
