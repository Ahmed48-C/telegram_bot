import logging
import requests
import os
from typing import Final
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, Application
from bs4 import BeautifulSoup
import uuid

TOKEN: Final = '5711672688:AAET8nIq3k8jh8rFjPWPxNTaMmR_UUyRfAE'

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Define the start command handler
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi! Welcome to MyBot.')

async def download(update, context):
    """Download a video from a social media link and send it back to the user."""
    chat_id = update.message.chat_id
    # Check if a video link was provided
    if len(context.args) == 0:
        await update.message.reply_text('Please provide a video link.')
        return
    video_link = context.args[0]
    # Download the video
    r = requests.get(video_link, allow_redirects=True)
    filename = os.path.basename(video_link)
    with open(filename, 'wb') as f:
        f.write(r.content)
        f.close()
    # Send the video back to the user
    with open(filename, 'rb') as f:
        await context.bot.send_video(chat_id=chat_id, video=f)
    os.remove(filename)


# def main():
#     """Start the bot."""
#     # Create the Updater and pass it your bot's token.
#     updater = Updater("5711672688:AAET8nIq3k8jh8rFjPWPxNTaMmR_UUyRfAE", proxy_url='http://yourproxyurl.com')

#     # Get the dispatcher to register handlers
#     dp = updater.dispatcher

#     # Add command handlers
#     dp.add_handler(CommandHandler("start", start))
#     dp.add_handler(CommandHandler("download", download))

#     # Start the Bot
#     updater.start_polling()
#     updater.idle()

# if __name__ == '__main__':
#     main()

# Run the program
if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('download', download))

    print('Polling...')
    # Run the bot
    app.run_polling(poll_interval=3)
    
    
#5711672688:AAET8nIq3k8jh8rFjPWPxNTaMmR_UUyRfAE