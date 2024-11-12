import pyautogui
import time
import datetime
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Function to simulate typing the message and track the time it was sent
async def type_and_log(update: Update, message: str, interval: float) -> None:
    # Get the current timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Log the time when the message is sent
    print(f"[{timestamp}] Sending message: {message}")
    
    # Simulate typing the message using pyautogui
    pyautogui.typewrite(message)
    
    # Add a delay between each message
    time.sleep(interval)

# Function to send spam messages with typewrite
async def spam(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Check if all arguments are provided
    if len(context.args) < 3:
        await update.message.reply_text("Usage: /spam <message> <count> <interval>")
        return

    # Parse the arguments
    message = context.args[0]  # Message to spam
    try:
        count = int(context.args[1])  # Number of times to send
        interval = float(context.args[2])  # Delay between each message in seconds
    except ValueError:
        await update.message.reply_text("Please provide a valid number for count and interval.")
        return

    # Send the message the specified number of times
    for i in range(count):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Log and send the message
        await update.message.reply_text(f"{message} (Message {i + 1} of {count})")
        await type_and_log(update, f"{message} (Message {i + 1} of {count})", interval)
        print(f"[{timestamp}] Message {i + 1} sent.")
        
        # Wait for the interval before sending the next message
        await asyncio.sleep(interval)

    await update.message.reply_text("Spamming completed!")

# Command to start the bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Welcome to the Spam Bot!\n\n"
        "I can send spam messages for you.\n"
        "Use the /spam command to send multiple messages.\n\n"
        "Commands:\n"
        "/spam <message> <count> <interval> - Send a spam message\n"
        "/help - Show this help message\n"
    )

# Command to show help instructions
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Usage of the Spam Bot:\n\n"
        "/spam <message> <count> <interval> - Spam a message multiple times.\n"
        "  - <message>: The message you want to spam.\n"
        "  - <count>: How many times you want to send the message.\n"
        "  - <interval>: The time interval (in seconds) between each message.\n\n"
        "Example: /spam Hello 5 2\n"
        "This will send 'Hello' 5 times with a 2-second interval between each.\n\n"
        "You can also type /start to get this message again."
    )

# Function to start the bot
def main():
    # Initialize the bot with your token
    app = Application.builder().token("YOUR_BOT_TOKEN").build()

    # Command to start the bot
    app.add_handler(CommandHandler("start", start))

    # Command to show help
    app.add_handler(CommandHandler("help", help_command))

    # Command to start spamming
    app.add_handler(CommandHandler("spam", spam))

    # Start polling for updates
    app.run_polling()

if __name__ == '__main__':
    main()
