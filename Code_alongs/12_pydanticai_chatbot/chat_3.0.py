# Använder:
#       pydantic för validering och strukturerad output
#       pydantic-ai för ageneten
#       logging för att logga
#       sqlite för att spara till databas-fil (placeholders för att undvika sql-injection)
#       asyncio för att köra requests asynkront

import asyncio
import logging
import sqlite3
from datetime import datetime
from pydantic_ai import Agent
from pydantic import BaseModel, Field
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("JokeBot")
load_dotenv()

# Strukturerad och validerad response 
class JokeResponse(BaseModel):
    joke: str = Field(description="The setup or introduction of the joke")
    punchline: str = Field(description="The funny punchline of the joke")
    rating: int = Field(description="A self-evaluation of how funny the joke is, from 1 to 10")
    explanation: str = Field(description="A short nerdy explanation of why it is funny")

# Databas-setup separat
def setup_database(db_file: str):
    """Initierar databasen. Körs en gång vid start."""
    try:
        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS jokes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    user_prompt TEXT,
                    joke TEXT,
                    punchline TEXT,
                    rating INTEGER,
                    explanation TEXT
                )
            """)
            conn.commit()
            logger.info(f"Database initialized/verified at: {db_file}")
    except sqlite3.Error as e:
        logger.error(f"Failed to init DB: {e}")
        raise # Om vi inte kan skapa DB, ska programmet krascha direkt.

# Agenten
class JokeBot:
    def __init__(self, model_name: str, db_file: str):
        self.db_file = db_file
        self.result = None 
        
        self.chat_agent = Agent(
            model_name,
            output_type=JokeResponse,
            system_prompt="""
                You are a joking programming nerd.
                Generate a programming joke based on the user input.
                Be sarcastic but funny.
            """
        )

    async def chat(self, prompt: str) -> dict:
        self.result = await self.chat_agent.run(prompt)
        self._save_interaction(prompt, self.result.output)
        return {"user_prompt": prompt, "bot_response": self.result.output.model_dump()}

    def _save_interaction(self, prompt: str, response: JokeResponse):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            sql = """
                INSERT INTO jokes (timestamp, user_prompt, joke, punchline, rating, explanation)
                VALUES (?, ?, ?, ?, ?, ?)
            """
            cursor.execute(sql, (
                datetime.now().isoformat(), prompt, response.joke, 
                response.punchline, response.rating, response.explanation
            ))
            conn.commit()
            
    def get_best_jokes(self, min_rating=7):
        """Hämtar topplistan från databasen."""
        with sqlite3.connect(self.db_file) as conn:
            # Row factory gör att vi kan använda kolumnnamn (t.ex row['joke'] ist för index)
            conn.row_factory = sqlite3.Row 
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT * FROM jokes WHERE rating >= ? ORDER BY rating DESC", 
                (min_rating,)
            )
            
            # Konverterar SQLite-rader till vanliga Python dictionaries
            return [dict(row) for row in cursor.fetchall()]

async def main():
    DB_FILE = "jokes.db"
    setup_database(DB_FILE)
    
    bot = JokeBot(model_name="google-gla:gemini-2.5-flash", db_file=DB_FILE)

    print("Starting chat...")
    response = await bot.chat("Tell me a joke about DevOps")
    joke_data = response["bot_response"]

    print(f"Joke:     {joke_data['joke']}")
    print(f"Punchline: {joke_data['punchline']}")
    print(f"Betyg: {joke_data['rating']}/10")

    # Topplista
    print("\n--- TOP RATED JOKES (From DB) ---")
    best_jokes = bot.get_best_jokes(min_rating=7)
    
    if not best_jokes:
        print("No high-rated jokes yet. Keep chatting!")
    else:
        for j in best_jokes:
            print(f"{j['rating']}/10: joke:{j['joke']} \n punchline:{j['punchline']}")
    
if __name__ == "__main__":
    asyncio.run(main())