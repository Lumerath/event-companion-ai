import os
from urllib import response
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

print("🤖 AI Service carregado!")

def generate_event_plan(event_name):
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=f"""
        You are Event Companion AI.

        You help people prepare for live events.

        Create a friendly event plan for:

        {event_name}

        Organize the answer using:

        🎟 Arrival
       🚪 Entrance
       👕 Merchandise
       🍔 Food
       🚶 Leaving

       Keep the answer short and practical.
       """
    )
    
    return response.output_text
