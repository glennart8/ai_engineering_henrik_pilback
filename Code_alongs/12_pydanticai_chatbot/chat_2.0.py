import asyncio
import json
import logging
import os
from datetime import datetime
from pydantic_ai import Agent
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Logging för spårbarhet
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("JokeBot")

load_dotenv()

# Klass för llm-response
class JokeResponse(BaseModel):
    joke: str = Field(description="The setup or introduction of the joke")
    punchline: str = Field(description="The funny punchline of the joke")
    rating: int = Field(description="A self-evaluation of how funny the joke is, from 1 to 10")
    explanation: str = Field(description="A short nerdy explanation of why it is funny")

# Klass för llm-agent
class JokeBot:
    # 2. Dependency Injection: Vi skickar in modell och filnamn
    def __init__(self, model_name: str, storage_file: str = "jokes.json"):
        self.storage_file = storage_file
        self.jokes = self._load_jokes()
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
        logger.info(f"JokeBot initialized with model: {model_name}")

    def _load_jokes(self) -> list:
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, "r", encoding="utf-8") as f:
                    content = f.read()
                    if not content: return []
                    return json.loads(content)
            except json.JSONDecodeError:
                logger.error(f"Corrupt JSON in {self.storage_file}. Starting fresh.")
                return []
        return []

    # Async metod i stället för run_sync()
    async def chat(self, prompt: str) -> dict:
        logger.info(f"Processing prompt: {prompt}")
        message_history = self.result.all_messages() if self.result else None
        
        try:
            # Awaita svaret (blockerar inte andra processer)
            self.result = await self.chat_agent.run(prompt, message_history=message_history)
            
            joke_data = self.result.output.model_dump()
            
            # Lägg till metadata (t.ex. timestamp) - bra praxis
            full_entry = {
                "timestamp": datetime.now().isoformat(),
                "user_prompt": prompt,
                "bot_response": joke_data
            }
            
            self.jokes.append(full_entry)
            await self._save_jokes_async() # Spara asynkront om möjligt, eller kör vanlig save
            
            return full_entry
            
        except Exception as e:
            logger.error(f"Error during chat execution: {e}")
            raise # Kasta vidare felet så att anroparen vet att det sket sig

    async def _save_jokes_async(self):
        """Sparar till fil (i verkligheten kanske detta är ett databasanrop)"""
        # För enkelhetens skull kör vi synkron skrivning här, men i en stor app
        # skulle detta vara ett anrop till en databas.
        with open(self.storage_file, "w", encoding="utf-8") as f:
            json.dump(self.jokes, f, indent=4, ensure_ascii=False)

# Entry point för async
async def main():
    # Här kan vi enkelt byta miljö (t.ex. 'test_jokes.json' för tester)
    bot = JokeBot(
        model_name="google-gla:gemini-2.5-flash", 
        storage_file="production_jokes.json"
    )

    result1 = await bot.chat("Tell me a joke about Python loops")
    print(f"Bot: {result1['bot_response']['joke']}\n")
    print(f"Bot: {result1['bot_response']['punchline']}\n")

    print("--- User: SQL ---")
    result2 = await bot.chat("One about SQL injection!")
    print(f"Bot: {result2['bot_response']['joke']}\n")
    print(f"Bot: {result2['bot_response']['punchline']}")

if __name__ == "__main__":
    # Starta event-loopen
    asyncio.run(main())