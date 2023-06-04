#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import re

from telegram import __version__ as TG_VER
from settings import TOKEN

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 5):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from commands.url_shortner import url_shortner
from commands.fibonacci import fibonacci_generator

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

STEP_1, STEP_2 = range(2)
ALL_COMMANDS = ["url", "fibonacci"]
ESCAPED_COMMANDS = [re.escape(command) for command in ALL_COMMANDS]
COMMANDS_PATTERN = r'^(' + '|'.join(ESCAPED_COMMANDS) + r')'
ALL_COMMANDS_VALUES = {
    "url": "url",
    "fibonacci": "number",
}
SELECTED_COMMAND = None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation ."""
    reply_keyboard = [ALL_COMMANDS]
    print(f"\n\nreply_keyboard : {reply_keyboard}\n\n")

    await update.message.reply_text(
        "Hi!, Please select a command to help you with. ",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Select command"
        ),
    )

    return STEP_1

# asks user for the input
async def step_1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """User selected url command."""
    global SELECTED_COMMAND
    user = update.message.from_user
    logger.info("User selected the url command of %s: %s", user.first_name, update.message.text)
    SELECTED_COMMAND = update.message.text
    await update.message.reply_text(
        f"Please provide {ALL_COMMANDS_VALUES[update.message.text]}",
        reply_markup=ReplyKeyboardRemove(),
    )

    return STEP_2

# gets the input and return its the solution
async def step_2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Receives the value and return the solution."""
    global SELECTED_COMMAND
    user = update.message.from_user
    user_input = update.message.text
    logger.info("User input of %s: %s", user.first_name, user_input)

    if SELECTED_COMMAND == "url":
        if user_input.startswith('http'):
            try:
                new_url = url_shortner(user_input)
                await update.message.reply_text(
                    f"URL : {new_url}"
                )
            except Exception as e:
                logger.info("Error on handling url : %s", str(e))
                await update.message.reply_text(
                    "Sorry, invalid url."
                )
        else:
            await update.message.reply_text(
                "Sorry, invalid url."
            )
    elif SELECTED_COMMAND == "fibonacci":
        try:
            fib_nums = int(user_input)
            await update.message.reply_text(
                f"{user_input} Fibonacci number are : {fibonacci_generator(fib_nums)}"
            )
        except Exception as e:
            logger.info("Error on handling number : %s", str(e))
            await update.message.reply_text(
                "Sorry, invalid input."
            )

    SELECTED_COMMAND = None
    return ConversationHandler.END


async def skip_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Skips the current command and end."""
    user = update.message.from_user
    logger.info("User %s had skupped the current command.", user.first_name)
    await update.message.reply_text(
        "Bye!"
    )

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Bye!", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # Add conversation handler with the states URL, URL_2
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            STEP_1: [MessageHandler(filters.Regex(COMMANDS_PATTERN), step_1)],
            STEP_2: [MessageHandler(filters.TEXT, step_2), CommandHandler("skip", skip_command)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)


    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()