from flask import Flask, request
import requests

app = Flask(__name__)

# Your bot token (⚠️ Not safe to keep here in production!)
TELEGRAM_TOKEN = "8385389366:AAFYb2oK6LesGbxinUryzfZ4sr_pmVr79Jg"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/"

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = f"✅ Your Chat ID is: {chat_id}"
        send_message(chat_id, text)

    return {"ok": True}

def send_message(chat_id, text):
    url = TELEGRAM_API_URL + "sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

@app.route("/", methods=["GET"])
def home():
    return "🚀 Bot is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
