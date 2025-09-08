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

from fastapi import FastAPI
import ollama

app = FastAPI()

@app.post("/generate")
def generate(promt: str):
    response = ollama.chat(model="mistral", messages = [{"role": "user", "content": promt}])
    return {"response": response["message"]["content"]}

# I konsol:
#   - uvicorn main:app --reload