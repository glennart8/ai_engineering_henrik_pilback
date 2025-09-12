from fastapi import FastAPI, HTTPException, status, Query
from data_processing import Glossary, read_json
from pprint import pprint

# Skapa en stans av app
app = FastAPI()

# ladda data
glossary = read_json("fastapi_glossary.json")

# pprint(glossary)


# CREATE
@app.post("/glossary/add/")
def add_glossary(glossary_item: Glossary):
    for i in glossary:
        if glossary_item.word.casefold() in i.word.casefold():
            raise HTTPException(status_code=400, detail="Word already exists.")
    
    glossary.append(glossary_item)
    
    return glossary_item, {"message": f"The word '{glossary_item.word}' was added successfully."}


# READ
@app.get("/glossary/")
async def read_glossary(word: str = Query(None)):
    if word:
        for i in glossary:
            if word.casefold() in i.word.casefold():
                return i
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Word '{word}' not found.")
        
    return glossary

# UPDATE
@app.put("/glossary/update")
def update_glossary(glossary_item: Glossary):
    for i, g in enumerate(glossary):
        if glossary_item.id == g.id:
            glossary[i] = glossary_item
            
            return f"The glossary '{glossary_item.word}' updated"  

# DELETE 
@app.delete("/glossary/{id}")
def delete_glossary(id : int):
    for i, j in enumerate(glossary):
        if id == j.id:
            deleted_item = glossary[i]
            del glossary[i]
            
            return f"Glossary '{deleted_item.word}' removed"