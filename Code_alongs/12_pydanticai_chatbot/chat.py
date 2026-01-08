from pydantic_ai.agent import AgentRunResult
from pydantic_ai import Agent
from dotenv import load_dotenv
import json
import os

load_dotenv()

class JokeBot:
    def __init__(self):
        self.chat_agent = Agent (
            "google-gla:gemini-2.5-flash-preview-09-2025",
            system_prompt="""
                    You are a joking programming nerd who always answer with a programming joke. 
                    Also add emojis in your language.
                    """
        )
        
        self.result = None # Detta gör det möjligt att kontrollera om en tidigare chat har skett 
        self.jokes_file = "jokes.json"
        
        # Ladda skämt om fil finns
        if os.path.exists(self.jokes_file):
            with open(self.jokes_file, "r") as f:
                self.jokes = json.load(f)
        else:
            self.jokes = []
        
        
    def chat(self, prompt: str) -> AgentRunResult:
        # all_messages() returnerar en lista av alla tidigare meddelanden för kontext till LLM
        message_history = self.result.all_messages() if self.result else None
        
        # kör koden synkront (inväntar svar från llm innan den fortsätter)
        self.result = self.chat_agent.run_sync(prompt, message_history=message_history)
        
        # Lägg till skämt
        joke_entry = {"user":prompt, "bot": self.result.output}
        self.jokes.append(joke_entry)

        # Spara skämt
        with open(self.jokes_file, "w") as f:
            json.dump(self.jokes, f, indent=4)

        return {"user": prompt, "bot": self.result.output}

if __name__ == "__main__":
    joke_bot = JokeBot()
    result = joke_bot.chat("Hello there, wzup?!")
    result = joke_bot.chat("Hello there again, wzup now?!")
    print(result)
    print(joke_bot.result.all_messages())