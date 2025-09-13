import os
from flask import Flask, request, jsonify
import requests

# Initialize Flask app
app = Flask(__name__)

# Your bot token
TOKEN = "8234827256:AAHIMCUanq5uFRLXZMLoBb6TLQ49WVCmEsg"
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

# Set webhook
def set_webhook():
    webhook_url = os.getenv('RENDER_EXTERNAL_URL') + '/webhook'
    response = requests.get(f"{BASE_URL}/setWebhook?url={webhook_url}")
    return response.json()

# Handle webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    
    # Extract message data
    if 'message' in data:
        chat_id = data['message']['chat']['id']
        user_id = data['message']['from']['id']
        first_name = data['message']['from'].get('first_name', '')
        
        # Check if it's a command
        if 'text' in data['message']:
            text = data['message']['text']
            
            if text.startswith('/start'):
                message = f"Hello {first_name}! Your user ID is: `{user_id}`"
                send_message(chat_id, message)
            elif text.startswith('/help'):
                message = "Just send any message and I'll reply with your user ID!"
                send_message(chat_id, message)
            else:
                message = f"Your user ID is: `{user_id}`"
                send_message(chat_id, message)
    
    return jsonify({"status": "ok"})

# Send message function
def send_message(chat_id, text):
    url = f"{BASE_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, json=payload)
    return response.json()

# Set webhook endpoint
@app.route('/set_webhook', methods=['GET'])
def set_webhook_route():
    result = set_webhook()
    return jsonify(result)

# Home page
@app.route('/')
def home():
    return "Telegram User ID Bot is running!"

# Health check endpoint for Render
@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
