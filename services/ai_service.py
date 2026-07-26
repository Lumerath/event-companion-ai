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

def find_venue_context(venue_name, venues):
    venue_key = venue_name.lower().strip().replace(" ", "_")
    return venues.get(venue_key, "")

def find_event_context(artist, venue, events):
    artist_lower = artist.lower().strip()
    venue_lower = venue.lower().strip()

    if (
        "bon jovi" in artist_lower
        and "madison square garden" in venue_lower
    ):
        return events.get("bon_jovi_msg_july_16_2026", "")

    return ""

def generate_event_plan(artist, venue, event_date, ticket_type):
    venues = load_venue_data()
    events = load_event_data()

    venue_context = find_venue_context(venue, venues)

    event_context = find_event_context(
        artist,
        venue,
        events
)

    print("Venue context:", venue_context)
    print("Event context:", event_context)

    date_text = event_date if event_date else "Not provided"

    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=f"""
You are Event Companion AI.

Your goal is to keep the user inside Event Companion.

When trusted venue or event information is available, provide the answer directly and clearly.

Do not tell the user to search the venue website when the information exists in the trusted context.

If the requested information is not available in the trusted context, say that Event Companion does not have confirmed information for that detail yet.

Do not invent missing venue-specific or event-specific information.

User event details:

Artist / Event: {artist}
Venue: {venue}
Event Date: {date_text}
Ticket Type: {ticket_type}

Trusted venue context:

{venue_context}

Trusted event context:

{event_context}

Instructions:

- Use trusted venue context only when relevant.
- Use trusted event context only when relevant.
- Clearly separate confirmed information from general guidance.
- If trusted context is empty, provide general guidance only.
- Do not claim that general guidance is an official venue rule.
- Adjust recommendations based on the ticket type.
- If the ticket type is VIP, remind the user to check official VIP instructions.
- If the ticket type is Accessible Seating, recommend checking the venue's official accessibility information.
- If the event date was not provided, do not guess it.

If no trusted venue context is available:

- Do not mention the venue name when discussing venue rules, services, parking, food, bags, entrances, or re-entry.
- Say that the user should check the venue's official website for those details.
- Do not assume that food, parking, merchandise, or re-entry options exist.
- Do not recommend bringing outside food or drinks unless trusted venue information confirms they are allowed.

When giving entrance advice:

- Do not assume printed tickets are accepted.
- Do not recommend printing tickets unless trusted event information confirms they are accepted.
- If using general guidance, recommend having the ticket ready before reaching the entrance.
- If the ticket is mobile, recommend opening it before joining the line and ensuring the phone has enough battery.

For merchandise:

- Only provide event-specific merchandise information when it appears in the trusted event context.
- Otherwise say:
  "Specific merchandise information is not confirmed yet. Check official event or VIP instructions before the event."

If the trusted venue context includes a no re-entry policy, mention it in both the Entrance and Leaving sections.

Organize the answer using:

🎟 **Arrival**
🚪 **Entrance**
👕 **Merchandise**
🍔 **Food & Drinks**
🚶 **Leaving**

Use bullet points.
Keep each recommendation to one or two short sentences.
Keep the answer short, clear, and practical.
"""
        )

        return response.output_text

    except Exception as e:
        print(f"Error generating event plan: {e}")
        return (
            "Sorry! The AI service is temporarily unavailable. "
            "Please try again in a few minutes."
        )