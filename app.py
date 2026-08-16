from flask import Flask, render_template, request
from services.ai_service import generate_event_plan
import markdown

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    message = ""

    if request.method == "POST":
                
        artist = request.form.get("artist", "").strip()
        venue = request.form.get("venue", "").strip()
        event_date = request.form.get("event_date", "").strip()
        ticket_type = request.form.get("ticket_type", "Not Sure").strip()

        if not artist or not venue:
            message = "Please enter both an artist/event and venue."
        else:
            message = generate_event_plan(
            artist,
            venue,
            event_date,
            ticket_type
        )

        message = markdown.markdown(message)    

    return render_template("index.html", message=message)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)