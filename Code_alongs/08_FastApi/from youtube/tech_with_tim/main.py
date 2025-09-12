# ------- OLLAMA ---------
# Länk: https://www.youtube.com/watch?v=cy6EAp4iNN4
# Använder OLLAMA
# skriv: 
#   - ollama för info
#   - ollama pull mistral för att hämta modellen
#   - ollama run mistral för att köra modellen
#   - /bye för att lämna

# ------- PYCHARM --------
# 

from fastapi import FastAPI, Depends, HTTPException, Header
import ollama
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY_CREDITS = {os.getenv("API_KEY"): 5}

def verify_api_key(x_api_key: str = Header(None)):
    credits = API_KEY_CREDITS.get(x_api_key, 0)
    if credits <= 0:
        raise HTTPException(status_code=401, detail=("Invalid api key, or no credits"))
    
    return x_api_key

app = FastAPI()

# CREATE
@app.post("/generate")
def generate(promt: str, x_api_key: str = Depends(verify_api_key)):
    API_KEY_CREDITS[x_api_key] -= 1
    response = ollama.chat(model="mistral", messages = [{"role": "user", "content": promt}])
    return {"response": response["message"]["content"]}

# I konsol:
#   - uvicorn main:app --reload