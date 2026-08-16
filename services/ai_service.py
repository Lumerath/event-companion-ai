import os
import json

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def load_venue_data():
    with open("data/venues.json", "r", encoding="utf-8") as file:
        return json.load(file)


def load_event_data():
    with open("data/events.json", "r", encoding="utf-8") as file:
        return json.load(file)


def find_venue_context(venue_name, venues):
    venue_lower = venue_name.lower().strip()

    for venue_data in venues.values():
        if not isinstance(venue_data, dict):
            continue

        official_name = venue_data.get("name", "").lower().strip()

        aliases = venue_data.get("aliases",[])

        aliases_lower = [
            alias.lower().strip()
            for alias in aliases
        ]

        if (
            venue_lower == official_name
            or venue_lower in aliases_lower
        ):
            return venue_data

    return ""

    
def find_event_context(artist, venue, events, venues):
    artist_lower = artist.lower().strip()
    venue_lower = venue.lower().strip()

    for event_data in events.values():
        if not isinstance(event_data, dict):
            continue

        saved_artist = event_data.get("artist", "").lower().strip()
        saved_venue = event_data.get("venue", "").lower().strip()
        
        venue_key = saved_venue.replace(" ", "_")
        venue_data = venues.get(venue_key, {})

        aliases = venue_data.get("aliases", [])

        aliases_lower = [
            alias.lower().strip()
            for alias in aliases
        ]

        if (
            saved_artist == artist_lower

        and (

             saved_venue == venue_lower

        or venue_lower in aliases_lower
         )

    ):
     
         return event_data
        
    return ""    

def validate_event(artist, venue, event_date, events, venues):
    artist_lower = artist.lower().strip()
    venue_lower = venue.lower().strip()
    event_date = event_date.strip()

    artist_found = False

    for event_data in events.values():
        if not isinstance(event_data, dict):
            continue

        saved_artist = event_data.get("artist", "").lower().strip()

        if saved_artist != artist_lower:
            continue

        artist_found = True

        expected_venue = event_data.get("venue", "").lower().strip()

        expected_venue_key = (
            event_data.get("venue", "")
            .lower()
            .strip()
            .replace(" ", "_")
        )

        venue_key = expected_venue.replace(" ", "_")
        venue_data = venues.get(venue_key, {})

        aliases = venue_data.get("aliases", [])

        aliases_lower = [
            alias.lower().strip()
            for alias in aliases
        ]
            
        expected_date = event_data.get("date", "").strip()

        if (
            expected_venue
            and venue_lower != expected_venue
            and venue_lower not in aliases_lower
        ):       
            return {
                "valid": False,
                "reason": "venue",
                "expected_venue": event_data.get("venue", ""),
                "expected_date": expected_date
            }

        if event_date and expected_date and event_date != expected_date:
            return {
                "valid": False,
                "reason": "date",
                "expected_venue": event_data.get("venue", ""),
                "expected_date": expected_date
            }

        return {
            "valid": True,
            "reason": None,
            "expected_venue": None,
            "expected_date": None
        }

    if not artist_found:
        return {
            "valid": False,
            "reason": "unverified",
            "expected_venue": None,
            "expected_date": None
        }


def build_venue_context(venue_data):
    context = []

    labels = {
        "getting_there": "Getting There",
        "arrival": "Arrival",
        "entrance": "Entrance",
        "bag_policy": "Bag Policy",
        "merchandise_information": "Merchandise",
        "food_options": "Food",
        "accessibility": "Accessibility",
        "reentry_policy": "Re-entry",
        "leaving": "Leaving"
    }

    for key, value in venue_data.items():
        if key in ("name", "aliases"):
            continue

        if value:
            label = labels.get(key, key)
            context.append(f"{label}: {value}")

    return "\n".join(context)


def generate_event_plan(
    artist,
    venue,
    event_date,
    ticket_type
):
    venues = load_venue_data()
    events = load_event_data()

    validation = validate_event(
        artist,
        venue,
        event_date,
        events,
        venues
    )

    if not validation["valid"]:

        if validation["reason"] == "venue":
            expected_venue = validation["expected_venue"]
            return f"""
### ⚠️ Event mismatch

The artist and venue don't appear to match.

Based on the available event information, {artist} is associated with {expected_venue}, not {venue}.

Please review your event details and try again.
"""
        elif validation["reason"] == "unverified":
            return f"""
### ⚠️ Event not verified

I couldn't verify this event using the available event information.

Please review the artist, venue, and date before generating the guide.
"""
        elif validation["reason"] == "date":
            expected_date = validation["expected_date"]
            return f"""
### ⚠️ Event date mismatch

The date entered doesn't appear to match the available event information.

Based on the available event information, the expected date is:

{expected_date}

Please review your event details and try again.
"""
        else:
            return f"""
### ⚠️ Event mismatch

The artist and venue don't appear to match.

Please review your event details and try again.
"""

    venue_context = find_venue_context(
        venue,
        venues
    )

    if venue_context:
        venue_context = build_venue_context(
            venue_context
        )

    event_context = find_event_context(
        artist,
        venue,
        events,
        venues
    )

    date_text = (
        event_date
        if event_date
        else "Not provided"
    )

    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=f"""
You are an AI assistant that helps people prepare for live events.

Your tone is friendly, calm, practical, and concise.

Your goal is to centralize trusted event information and provide useful guidance without overwhelming the user.

User event details:

Artist / Event: {artist}
Venue: {venue}
Event Date: {date_text}
Ticket Type: {ticket_type}

Trusted venue context:

{venue_context}

Trusted event context:

{event_context}

## Source Priority

- Use trusted event context when available.
- Use trusted venue context when relevant.
- Event-specific information takes priority over general venue information.
- Never invent venue-specific, event-specific, or ticket-specific details.
- If the event date was not provided, do not guess it.

## Missing Information Policy

If trusted information is unavailable:

- Clearly say that the detail has not yet been confirmed.
- Do not guess.
- Do not tell the user to search another website, contact the venue, check social media, or review external communications.
- Provide only safe general guidance when appropriate.

When in doubt, prefer saying "not yet confirmed" instead of making an assumption.

## Ticket Type Guidance

General Admission:
- Focus on arriving early, lines, and general admission procedures.
- Do not assume that all General Admission events are first-come, first-served unless trusted context confirms it.

Reserved Seating:
- Focus on locating the correct section, row, and seat.
- Do not suggest arriving extremely early solely to secure a place.

VIP:
- Use confirmed VIP information only when it exists in the trusted event context.
- If no confirmed VIP information exists, say:
  "VIP instructions have not yet been confirmed for this event."
- Do not assume early entry, soundcheck, lounge access, merchandise, check-in, or other VIP benefits.
- Do not include General Admission advice unless it also applies to VIP guests.

Accessible Seating:
- Prioritize confirmed accessibility information.
- If none is available, say that accessibility details have not yet been confirmed.

Not Sure:
- Explain that some procedures may vary by ticket type.
- Do not assume VIP benefits, reserved seating, or General Admission procedures.

## Entrance Guidance

- Do not assume printed tickets are accepted.
- Do not recommend printing tickets unless trusted information confirms it.
- Recommend having the ticket ready before reaching the entrance.
- For mobile tickets, recommend opening the ticket before joining the line and ensuring the device has enough battery.

## Merchandise Guidance

- Use confirmed merchandise information only when it exists in the trusted event context.
- Otherwise say:
  "Merchandise information has not yet been confirmed for this event."

## Section Mapping

Use venue information only in its matching section:

- getting_there → 🚆 Getting There
- arrival → 🎟 Arrival
- entrance + bag_policy → 🚪 Entrance
- merchandise_information → 👕 Merchandise
- food_options → 🍔 Food & Drinks
- reentry_policy + leaving → 🚶 Leaving

Do not move confirmed information between sections.

If the trusted venue context includes a no re-entry policy, mention it in both Entrance and Leaving.

## Output Format

Organize the answer in this exact order:

🚆 **Getting There**
Provide transportation and access guidance.

🎟 **Arrival**
Explain what the attendee should know upon arriving.

🚪 **Entrance**
Include ticket access, security screening, entrance procedures, and bag policy.

👕 **Merchandise**
Use confirmed merchandise information or clearly state that it has not yet been confirmed.

🍔 **Food & Drinks**
Use confirmed food information or clearly state that it has not yet been confirmed.

🚶 **Leaving**
Include re-entry policy and practical exit guidance.

Use bullet points.
Keep each recommendation to one or two short sentences.
Keep the answer short, clear, and practical.
"""
        )

        return response.output_text

    except Exception as error:
        print(
            f"Error generating event plan: {error}"
        )

        return """
### ⚠️ I couldn't plan your event right now.

Something went wrong while I was preparing your guide.

Please try again in a few moments.
"""