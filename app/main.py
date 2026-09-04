from fastapi import FastAPI
from app.routers import books


app = FastAPI()

app.include_router(books.router)

@app.get("/")
async def read_root():
    return {"msg": "Book API is running!"}