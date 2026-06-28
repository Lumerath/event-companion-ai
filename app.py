from flask import Flask, render_template, request
from services.ai_service import generate_event_plan

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    message = ""

    if request.method == "POST":
        event_name = request.form["event"]
        message = generate_event_plan(event_name)

    return render_template("index.html", message=message)

if __name__ == "__main__":
    app.run(debug=True)