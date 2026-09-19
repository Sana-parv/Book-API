from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import books

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://book-api-frontend.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(books.router)


@app.get("/")
async def read_root():
    return {"msg": "Book API is running!"}