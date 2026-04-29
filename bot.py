import random
import logging
import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# 1. SETUP WEB SERVER (For Render)
app = Flask(__name__)

@app.route('/')
def health_check():
    return "Bot is running!"

def run_flask():
    # Render provides a PORT environment variable automatically
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# 2. BOT LOGIC
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

TOKEN = "8514235567:AAFAvNQbIdZlF9V79Qm6AfHK80IbB2o0nSg"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Bot is Live on Render! Send any message to roll.')

async def generate_random(update: Update, context: ContextTypes.DEFAULT_TYPE):
    number = random.randint(0, 9)
    size = "BIG" if number >= 5 else "SMALL"
    response = f"🎲 Result: {number}\n📊 Size: {size}"
    await update.message.reply_text(response)

def main():
    # Start the Flask web server in a separate thread
    threading.Thread(target=run_flask, daemon=True).start()

    # Start the Telegram Bot
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_random))

    print("Bot is starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
    
