# Event Companion AI

**An AI-powered event companion designed to help people navigate live events with more confidence and less stress.**

Event Companion AI combines trusted event and venue data with Generative AI to create practical, personalized guides for concert and live-event attendees.

## 🎯 The Problem

Event information is often scattered across venue pages, ticket details, emails, FAQs, and other sources.

Event Companion AI explores how Generative AI can organize trusted information into a simple guide while reducing unsupported assumptions and information overload.

## ✨ Key Features

* Personalized guides based on artist/event, venue, date, and ticket type
* Event and venue validation before AI generation
* Recognition of venue aliases and common naming variations
* Ticket-aware guidance for General Admission, Reserved Seating, VIP, Accessible Seating, and uncertain ticket types
* Structured guidance for transportation, arrival, entrance, merchandise, food, and leaving
* Detection of mismatched or unverified event information

## 🛡️ AI Reliability

Event Companion AI uses structured event and venue data as trusted context instead of relying only on the language model's general knowledge.

The AI is instructed to:

* Prioritize trusted event-specific and venue-specific information
* Never invent event, venue, or ticket-specific details
* Avoid assuming VIP benefits or procedures
* Clearly identify information that has not been confirmed
* Prefer **"not yet confirmed"** over guessing

This validation and context layer helps reduce hallucinations and makes the generated guidance more reliable.

## ⚙️ How It Works

```text
User Input
    ↓
Event Validation
    ↓
Trusted Event & Venue Context
    ↓
Prompt Construction
    ↓
OpenAI API
    ↓
Personalized Event Guide
```

## 🛠️ Tech Stack

**Python · Flask · OpenAI API · JSON · Jinja2 · Markdown · HTML · CSS · JavaScript · Git/GitHub**

## 💡 What I Learned

Building Event Companion AI gave me hands-on experience with:

* Integrating Generative AI into a web application
* Prompt design and instruction hierarchy
* Structuring trusted context for LLMs
* Input validation and data normalization
* Reducing unsupported AI-generated information
* Flask application development
* Debugging and iterative testing

One of the biggest lessons from the project was that generating an AI response is only part of the challenge. **Designing when an AI should trust information, reject incorrect input, or acknowledge that something is unknown is just as important.**

## 📌 Project Status

**Functional MVP — currently in refinement.**

The core AI generation, event validation, venue matching, and trusted-context flows are working. Visual identity and additional UX improvements are planned for the next iteration.


Built by Luciana Merath

LinkedIn: www.linkedin.com/in/luciana-merath-5391323aa