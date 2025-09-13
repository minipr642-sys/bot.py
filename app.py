import os
from flask import Flask, request, jsonify
import telegram
from telegram import Update, Bot
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters

# Initialize Flask app
app = Flask(__name__)

# Your bot token
TOKEN = "8234827256:AAHIMCUanq5uFRLXZMLoBb6TLQ49WVCmEsg"
bot = Bot(token=TOKEN)

# Start command handler
def start(update, context):
    user = update.effective_user
    update.message.reply_text(f"Hello {user.first_name}! Your user ID is: `{user.id}`", parse_mode='Markdown')

# Help command handler
def help_command(update, context):
    update.message.reply_text("Just send any message and I'll reply with your user ID!")

# Handle all messages
def echo(update, context):
    user = update.effective_user
    update.message.reply_text(f"Your user ID is: `{user.id}`", parse_mode='Markdown')

# Webhook handler
@app.route('/webhook', methods=['POST'])
def webhook():
    # Create dispatcher
    dispatcher = Dispatcher(bot, None, workers=0)
    
    # Add handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    
    # Process the update
    update = Update.de_json(request.get_json(), bot)
    dispatcher.process_update(update)
    
    return jsonify({"status": "ok"})

# Set webhook
@app.route('/set_webhook', methods=['GET'])
def set_webhook():
    # Get the Render URL from environment variable
    webhook_url = os.getenv('RENDER_EXTERNAL_URL') + '/webhook'
    
    # Set the webhook
    success = bot.set_webhook(webhook_url)
    
    if success:
        return jsonify({"message": f"Webhook set successfully: {webhook_url}"})
    else:
        return jsonify({"message": "Webhook setup failed"}), 500

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
