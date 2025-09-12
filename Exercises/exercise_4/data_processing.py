import json
from pydantic import BaseModel
from pathlib import Path
from pprint import pprint


DATA_PATH = Path(__file__).parents[2] / "data"

class Glossary(BaseModel):
    id: int
    word: str
    meaning: str
    
    
def read_json(filename: str):
    with open(DATA_PATH / filename, 'r') as file:
        data = json.load(file)
    return [Glossary.model_validate(item) for item in data]

data = read_json("fastapi_glossary.json")
pprint(data)

# Omvandla varje post i listan till en Pydantic-modell med model_validate()

# glossarylist = {item['word']: Glossary.model_validate(item) for item in data}

