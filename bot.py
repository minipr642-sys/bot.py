import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot token - make sure to set this as an environment variable in production
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '8385389366:AAFYb2oK6LesGbxinUryzfZ4sr_pmVr79Jg')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    user = update.effective_user
    welcome_message = f"""
👋 Hello {user.first_name}!

I'm your User ID Bot! 🤖

Use me to get your Telegram user ID or anyone else's who interacts with me.

Just send me any message and I'll tell you the user ID!

Your current User ID: <code>{user.id}</code>
    """
    await update.message.reply_text(welcome_message, parse_mode='HTML')

async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get the user ID when any message is sent."""
    user = update.effective_user
    chat = update.effective_chat
    
    response = f"""
🆔 User Information:

👤 Username: {user.username or 'Not set'}
📛 First Name: {user.first_name or 'Not set'}
👤 Full Name: {user.full_name}
🆔 User ID: <code>{user.id}</code>

💬 Chat ID: <code>{chat.id}</code>
📢 Chat Type: {chat.type}
    """
    
    await update.message.reply_text(response, parse_mode='HTML')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /help is issued."""
    help_text = """
🆘 Help Menu

Commands:
/start - Welcome message with your User ID
/help - Show this help message

Just send me any message and I'll reply with your User ID information!

📝 Example: Send "hello" and I'll tell you your User ID.
    """
    await update.message.reply_text(help_text)

def main():
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_id))

    # Run the bot until you press Ctrl-C
    print("🤖 Bot is starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
