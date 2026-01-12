# Använder:
#       pydantic för validering och strukturerad output
#       pydantic-ai för ageneten
#       logging för att logga ALLT (och sparar till fil)
#       sqlite för att spara till databas-fil (placeholders för att undvika sql-injection)
#       asyncio för att köra requests asynkront

import asyncio
import logging
import sqlite3
from datetime import datetime
from pydantic_ai import Agent, RunContext
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Enkel logger som inte sparar till fil
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger("JokeBot")

# Skapa en konfiguration som har TVÅ "mottagare" (handlers)
logging.basicConfig(
    level=logging.DEBUG, # Vi fångar ALLT (Debug och uppåt)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("jokebot.log", encoding='utf-8'), # Spara till fil
        logging.StreamHandler()                               # Skriv till terminalen
    ]
)

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

# Definiera vad agenten behöver för att jobba (Dependencies)
class JokeDeps:
    def __init__(self, db_file: str):
        self.db_file = db_file

# Agenten
class JokeBot:
    def __init__(self, model_name: str, db_file: str):
        self.db_file = db_file
        self.result = None 
        
        self.chat_agent = Agent(
            model_name,
            deps_type=JokeDeps,  # koppla dependencies
            output_type=JokeResponse,
            system_prompt="""
                You are a joking programming nerd.
                Before telling a joke, check if you have told similar jokes before using your tools.
                If you have told many jokes about a topic, mention that ("I've already told 5 jokes about Java...").
                Generate a programming joke based on the user input.
            """
        )
        
        # Registrera verktyget
        self._register_tools()
        
    def _register_tools(self):
        # Skapa verktyget som agenten får använda
        @self.chat_agent.tool
        def count_jokes_about_topic(ctx: RunContext[JokeDeps], topic: str) -> int:
            """Checks the database to see how many jokes exist about a specific topic."""
            
            # Agenten kommer själv lista ut vilket 'topic' den ska söka på (t.ex. "Java" eller "SQL")
            with sqlite3.connect(ctx.deps.db_file) as conn:
                cursor = conn.cursor()
                # En enkel sökning med LIKE
                cursor.execute(
                    "SELECT COUNT(*) FROM jokes WHERE user_prompt LIKE ? OR joke LIKE ?", 
                    (f"%{topic}%", f"%{topic}%")
                )
                count = cursor.fetchone()[0]
                logger.info(f"Agent checked DB for '{topic}' -> Found {count}")
                return count    

    async def chat(self, prompt: str) -> dict:
        # Skicka in dependencies när vi kör
        deps = JokeDeps(self.db_file)
        # Läs history
        message_history = self.result.all_messages() if self.result else None
        
        self.result = await self.chat_agent.run(
            prompt, 
            message_history=message_history,
            deps=deps 
        )
        
        # Spara och returnera
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
    best_jokes = bot.get_best_jokes(min_rating=8)
    
    if not best_jokes:
        print("No high-rated jokes yet. Keep chatting!")
    else:
        for j in best_jokes:
            print(f"{j['rating']}/10: joke:{j['joke']} \n punchline:{j['punchline']}")
    
if __name__ == "__main__":
    asyncio.run(main())