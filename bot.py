import hashlib
import time
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = 'YOUR_BOT_TOKEN_HERE'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me any number for a Signal!")

async def calculate_signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    
    if user_input.isdigit():
        # Step 1: Create a unique 'seed' using the number + current time
        # This ensures the bot 'calculates' a new result each time.
        seed = f"{user_input}{time.time()}"
        
        # Step 2: Use a Hash (SHA256) to turn that seed into a long unique string
        hash_result = hashlib.sha256(seed.encode()).hexdigest()
        
        # Step 3: Convert a piece of that hash into a number and get the last digit (0-9)
        final_digit = int(hash_result[-1], 16) % 10
        
        # Step 4: Determine Buy/Sell
        signal = "BUY 🟢" if final_digit in [0, 2, 4, 6, 8] else "SELL 🔴"
        
        await update.message.reply_text(f"🔢 Result: {final_digit}\n📈 Signal: {signal}")
    else:
        await update.message.reply_text("Please enter a number only.")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, calculate_signal))
    app.run_polling()

if __name__ == '__main__':
    main()
    