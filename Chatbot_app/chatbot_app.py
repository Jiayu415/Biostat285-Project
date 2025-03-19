from flask import Flask, request, jsonify, render_template
from openai import OpenAI
import os

app = Flask(__name__)


OPENAI_API_KEY = "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"

client = OpenAI(api_key=OPENAI_API_KEY)
# Disclaimer: This system is for reference only and does not replace professional medical diagnosis.
DISCLAIMER = (
    "[Disclaimer] This system is for informational purposes only and does not replace a professional doctor's diagnosis. "
    "In case of an emergency, please call your local emergency service immediately."
)


def check_emergency(user_message):
    """
    Checks if the user input contains any emergency keywords.
    """
    emergency_keywords = ['emergency', 'urgent', 'unconscious', 'difficulty breathing', 'heart attack']
    for keyword in emergency_keywords:
        if keyword.lower() in user_message.lower():
            return True
    return False


def generate_response(user_message):
    """
    Generates a response based on user input:
    1. If an emergency keyword is detected, return an emergency prompt.
    2. Otherwise, use the Chat Completions API to generate a response.
       The disclaimer is passed as a system message.
    """
    if check_emergency(user_message):
        return "We detected a potential emergency. Please call your local emergency service or visit the nearest medical facility immediately."

    # The new interface uses a list of messages with defined roles.
    messages = [
        {"role": "system", "content": DISCLAIMER},
        {"role": "user", "content": f"Patient: {user_message}\nDoctor:"}
    ]

    try:
        completion = client.chat.completions.create(
            model="gpt-4o",  # Replace with "gpt-4" if needed, and ensure your account has access.
            messages=messages,
            temperature=0.7,
            max_tokens=100,
        )
        reply = completion.choices[0].message.content.strip()
    except Exception as e:
        print(e)  # Print error details for debugging
        reply = "Sorry, the system encountered an error. Please try again later."
    return reply


@app.route("/")
def index():
    greeting = "Hello! Welcome to the Medical Consultation Chatbot. How can I assist you today?"
    return render_template("index.html", greeting=greeting)


@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.form.get("message")
    reply = generate_response(user_message)
    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(debug=True)