import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

print("🤖 AI Service carregado!")

def load_venue_data():
    with open("data/venues.json", "r") as file:
        return json.load(file)
    
def load_event_data():
    with open("data/events.json", "r") as file:
        return json.load(file)

def generate_event_plan(event_name):
    venues = load_venue_data()
    events = load_event_data()

    venue_context = ""

    if "madison square garden" in event_name.lower():
        venue_context = venues["madison_square_garden"]

        print("Venue context:", venue_context)

    event_context = ""

    if "bon jovi" in event_name.lower():
        event_context = events["bon_jovi_msg_july_16_2026"]

        print("Event context:", event_context)

    try:
        
        response = client.responses.create(
        model="gpt-4.1-mini",
        input=f"""
        You are Event Companion AI.

        Your goal is to help people enjoy live events with confidence.

        You are friendly, practical, and calm.

        Only provide useful information.

        Avoid overwhelming the user with unnecessary details.

        Never claim specific venue information unless it is explicitly provided by the user.

        If a detail depends on the venue or event, provide general guidance instead.

        Make general guidance practical and actionable.

        Avoid obvious advice unless you explain a useful action the user can take or a common problem it helps prevent.

        Trusted venue context:

        {venue_context}

        Use the trusted venue context above when relevant.

        Do not invent venue-specific details that are not included in the context.

        If the trusted venue context includes a no re-entry policy, mention it in both the Entrance and Leaving sections because the user must know before entering and before deciding to leave.

        Trusted event context:

        {event_context}

        Use the trusted event context above when relevant.
        Do not invent event-specific details that are not included in the context.
        For merchandise, only provide event-specific advice if merchandise information exists in the trusted event context.

        If no trusted merchandise information is available, say:
        "Specific merchandise information is not confirmed yet. Check official event or VIP instructions before the event."

        {event_name}

        Organize the answer using:

        🎟 Arrival
       🚪 Entrance
       👕 Merchandise
       🍔 Food
       🚶 Leaving

       Format each section on a new line. Use bold titles and keep each recommendation to one or two short sentences.
       Answer in bullets.

       Keep the answer short and practical.
       """
    )
    
        return response.output_text
    
    except Exception as e:
        print(f"Error generating event plan: {e}")
        return "Sorry! The AI service is temporarily unavailable. Please try again in a few minutes"
