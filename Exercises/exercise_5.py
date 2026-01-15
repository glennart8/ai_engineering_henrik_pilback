"""
0. Make a PydanticAI model that can take an input of a location and then it should suggest 5 restaurants nearby that place. 
The restaurant model should have

name
type of food (cuisine)
price level
rating
short description
opening hours
location
It's okay if your model is making up a restaurant that doesn't exist.

# 1. FastAPI to serve PydanticAI
# Now make a fastapi with a post endpoint in natural language to prompt for a location and what type of food. 
# Based on these it should generate a restaurant and store it in a duckdb database.

# Also implement a get endpoint for showing all restaurants in the database. Implement a simple frontend for this application.


"""

from pydantic import BaseModel
from pydantic_ai import Agent
from dotenv import load_dotenv
import duckdb
from fastapi import FastAPI
import streamlit as st
import requests

load_dotenv()

# Skapa pydanticmodell
class Restaurant(BaseModel):
    name: str
    cuisine: str
    price_level: str
    rating: float
    description: str
    opening_hours: str
    location: str

# Instansiera en pydantic_ai agent med strukturerad output
agent = Agent(model="google-gla:gemini-2.5-flash", output_type=list[Restaurant], system_prompt="Suggest 5 restaurants nearby the location provided.")
 
# --- DUCKDB ---
try:
    conn = duckdb.connect("restaurants.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS restaurants (
            name VARCHAR,
            cuisine VARCHAR,
            price_level VARCHAR,
            rating FLOAT,
            description VARCHAR,
            opening_hours VARCHAR,
            location VARCHAR
        )
    """)
except Exception as e:
    print(f"Could not connect to database (might be locked by another process): {e}")
    conn = None

# --- FASTAPI ---
app = FastAPI()

@app.post("/generate_restaurant")
async def generate_restaurant(location: str, type_of_food: str):
    agent = Agent(
        model="google-gla:gemini-2.5-flash", 
        output_type=Restaurant, 
        system_prompt="You are a food expert. Suggest a restaurant based on location and cuisine."
    )
    
    prompt = f"Suggest a restaurant in {location} that serves {type_of_food}."
    result = await agent.run(prompt)
    r = result.output
    
    # Spara till DuckDB
    conn.execute("""
        INSERT INTO restaurants VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (r.name, r.cuisine, r.price_level, r.rating, r.description, r.opening_hours, r.location))
    
    return r

@app.get("/restaurants")
def get_restaurants():
    # Hämtar alla restauranger som en lista av dictionaries
    return conn.execute("SELECT * FROM restaurants").fetch_df().to_dict(orient="records")


# Streamlit
st.title("Restaurant Generator")

with st.form("gen_form"):
    loc_input = st.text_input("Location", value="Stockholm")
    food_input = st.text_input("Cuisine", value="Italian")
    submitted = st.form_submit_button("Generate Restaurant")

if submitted:
    with st.spinner("Asking agent..."):
        try:
            response = requests.post("http://127.0.0.1:8000/generate_restaurant", 
                                     params={"location": loc_input, "type_of_food": food_input})
            if response.status_code == 200:
                data = response.json()
                st.success(f"Generated: {data['name']}")
                st.json(data) # Visar json rätt upp och ner
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to backend.")

st.divider()

if st.button("Get em' all!"):
    try:
        response = requests.get("http://127.0.0.1:8000/restaurants")
        if response.status_code == 200:
            st.dataframe(response.json())
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to backend.")
