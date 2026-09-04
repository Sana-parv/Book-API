from turtle import title


def test_create_book(client):
    response = client.post("/books/", json={
        "title": "Harry Potter",
        "author": "J.K. Rowling",
        "description": "A young wizard's journey",
        "price": 500
    })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Harry Potter"
    assert data["author"] == "J.K. Rowling"
    assert data["description"] == "A young wizard's journey"
    assert data["price"] == 500
    assert "id" in data

def test_search_by_author(client):
    client.post("/books/", json={
        "title": "The Hobbit", 
        "author": "J.R.R. Tolkien",
        "description": "A hobbit's adventure",
        "price": 300
    })
    client.post("/books/", json={
        "title": "The Lord of the Rings",
        "author": "J.R.R. Tolkien",
        "description": "An epic fantasy",
        "price": 700
    })
    response = client.get("/books/search?author=J.R.R. Tolkien")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "The Hobbit"
    assert data[1]["title"] == "The Lord of the Rings"

def test_search_by_title(client):
    client.post("/books/", json={
        "title": "1984",
        "author": "George Orwell",
        "description": "Dystopian novel",
        "price": 400
    })
    client.post("/books/", json={
            "title": "The Lord of the Rings",
            "author": "J.R.R. Tolkien",
            "description": "An epic fantasy",
            "price": 700
        })
    response = client.get("/books/search?title=1984")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["author"] == "George Orwell"

def test_search_by_price(client):
    client.post("/books/", json={
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "description": "A classic novel",
        "price": 600
    })
    client.post("/books/", json={
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "description": "A novel about racial injustice",
        "price": 600
    })
    response = client.get("/books/search?price=600")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "The Great Gatsby"
    assert data[1]["title"] == "To Kill a Mockingbird"

def test_search_by_pagination(client):
    client.post("/books/", json={
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "description": "A classic novel",
        "price": 600
    })
    client.post("/books/", json={
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "description": "A novel about racial injustice",
        "price": 600
    })
    client.post("/books/", json={
        "title": "1984",
        "author": "George Orwell",
        "description": "Dystopian novel",
        "price": 400
        })
    client.post("/books/", json={
        "title": "The Lord of the Rings",
        "author": "J.R.R. Tolkien",
        "description": "An epic fantasy",
        "price": 700
    })
    response = client.get("/books/search?skip=1&limit=2")
    assert response.status_code == 200
    assert len(response.json()) == 2

    response = client.get("/books/search?skip=2&limit=2")

    assert response.status_code == 200
    assert len(response.json()) == 2

    
def test_get_book_by_id(client):
    create_response = client.post("/books/",json={
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "description": "A classic novel",
        "price": 600
    })
    
    book_id = create_response.json()["id"]
    
    response = client.get(f"/books/{book_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "The Great Gatsby"

def test_get_book_by_id_not_found(client):
    response = client.get("/books/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"

def test_view_all_books(client):
    client.post("/books/", json={
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "description": "A classic novel",
        "price": 600
    })
    client.post("/books/", json={
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "description": "A novel about racial injustice", 
         "price": 600
    })
    response = client.get("/books/")
    assert response.status_code == 200

def test_update_book(client):
    client.post("/books/", json={
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "description": "A classic novel",
        "price": 600
    })
    response = client.put("/books/1", json={
        "title": "The Great Gatsby Updated",
        "author": "F. Scott Fitzgerald",
        "description": "An updated classic novel",
        "price": 650
    })
    assert response.status_code == 200
    assert response.json()["title"] == "The Great Gatsby Updated"

def test_update_book_not_found(client):
    response = client.put("/books/999", json={
        "title": "Non-existent Book",
        "author": "Unknown",
        "description": "This book does not exist",
        "price": 500
    })
    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"

def test_delete_book(client):
    client.post("/books/", json={
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "description": "A classic novel",
        "price": 600
    })
    response = client.delete("/books/1")
    assert response.status_code == 200  
    assert response.json() == {"msg": "Book deleted successfully"}

def test_create_book_invalid_price(client):
    response = client.post("/books/", json={
        "title": "Test Book",
        "author": "Test Author",
        "description": "Test description",
        "price": -100
    })

    assert response.status_code == 422
