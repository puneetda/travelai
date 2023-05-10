my_api_key = "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"

import openai
from flask import Flask, render_template, request

app = Flask(__name__)

def format_itinerary(itinerary_text):
    days = itinerary_text.split("Day ")
    formatted_itinerary = ""
    for day in days:
        if not day.strip():
            continue
        day_number, activities = day.split(":", 1)
        activities = activities.strip().replace("\n", "<br>")
        formatted_day = f"<p class='day'><strong>Day {day_number.strip()}:</strong><br>{activities}</p>"
        formatted_itinerary += formatted_day
    return formatted_itinerary


def get_itinerary(api_key, chat_history, destination, num_days, date):
    openai.api_key = api_key

    message = f"Create an itinerary for {destination} for {num_days} days starting on {date}."
    data = {
        "messages": chat_history + [{"role": "user", "content": message}]
    }

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=data["messages"],
    )

    itinerary_text = response['choices'][0]['message']['content']
    formatted_itinerary = format_itinerary(itinerary_text)
    return formatted_itinerary.replace(destination, f'<span class="highlight">{destination}</span>')

@app.route("/", methods=["GET", "POST"])
def index():
    api_key = my_api_key
    chat_history = []

    if request.method == "POST":
        destination = request.form["destination"]
        num_days = request.form["num_days"]
        date = request.form["date"]
        itinerary = get_itinerary(api_key, chat_history, destination, num_days, date)
        return render_template("index.html", itinerary=itinerary)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
