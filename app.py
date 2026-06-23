from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    message = ""

    if request.method == "POST":
        event_name = request.form["event"]
        message =  f"""
        Evento registrado: {event_name}

        Seu assistente de eventos está sendo preparado.
        """

    return render_template("index.html", message=message)

if __name__ == "__main__":
    app.run(debug=True)