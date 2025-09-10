from fastapi import FastAPI, Query
from data_processing import library_data, Book

app = FastAPI()

library = library_data("library.json")

# Hämta böcker från bibliotek
books = library.books

# Lägg till endpointen /books för att hitta i uvicorn
@app.get("/books")
async def read_books():
    return books


# path parameter
@app.get("/books/title/{title}")
async def read_books_by_title(title: str):
    return [book for book in books if book.title.casefold() == title.casefold()] # casefold() är som lower()


# add a book
@app.post("/books/create_book")
async def create_book(book_request: Book):
    new_book = Book.model_validate(book_request)
    books.append(new_book)
    return new_book, f"Book '{new_book.title}' added"


# delete
@app.delete("/books/delete/{book_id}")
async def delete_book(book_id: int):
    for i, b in enumerate(books):
        if book_id == b.id:
            deleted_book = books[i]
            del books[i] # eftersom det är en lista funkar del med index
            return f"Book '{deleted_book.title}' deleted"
        
        
# update
@app.put("/books/{book_id}")
async def update_book(book_item: Book):
    for i, b in enumerate(books):
        if book_item.id == b.id:
            books[i] = book_item
            return f"Book '{book_item.title}' added"    
  
  
# adding different query parameters
@app.get("/books/")
async def search_book(book_year: int = Query(default=1600, gt = 0, lt = 2026, description="Filter books later than year"),
                      book_author: str = Query(default=None, description="Filter books by author"),
                      book_title: str = Query(default=None, description="Filter books by title")):
    
    filtered_books = [book for book in books if book_year < book.year]
    
    if book_author:    
        filtered_books = [book for book in filtered_books if book_author.casefold() in book.author.casefold()]
    if book_title:
        filtered_books = [book for book in filtered_books if book_title.casefold() in book.title.casefold()]
    
    return filtered_books
    
# --- BYGGA UT --- 

# Söka via olika bibliotek (då måste vi lägga in det)
# Lägga in datan i databas typ duckdb
# Filtrera via genre, eller rekommenderad ålder
# Uppdatera inte ID - kontrollera så att ID:n är unika
# Undvik att dubletter läggs in
# Allmän felhantering
# Streamlit