from telegram.ext import CallbackQueryHandler, PreCheckoutQueryHandler, filters, \
    MessageHandler
from button_handlers import button
from payment import successful_payment_callback, handle_pre_checkout
from data.globals import application, logger
from onboarding import start
from telegram import Update
from telegram.ext import CommandHandler
import os
import sys


def main():
    application.add_handler(CommandHandler("start", start))
    application.add_handler(PreCheckoutQueryHandler(handle_pre_checkout))
    application.add_error_handler(error_handler)
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment_callback))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


def error_handler(update, context):
    logger.error(f"An error occurred: {context.error}")
    if update and hasattr(update, 'effective_message'):
        try:
            update.effective_message.reply_text("Произошла ошибка. Пожалуйста, попробуйте еще раз позже.")
        except Exception as e:
            logger.error(f"Error while sending error message: {e}")
    else:
        logger.info("Update or effective_message not available for this error.")


if __name__ == '__main__':
    lock_file_path = "/tmp/my_bot.lock"

    # Check if the lock file already exists
    if os.path.exists(lock_file_path):
        print("Another instance of the bot is already running.")
        sys.exit()

    # Create a lock file to signify that the bot is running
    with open(lock_file_path, 'w') as lock_file:
        lock_file.write("Running")

    try:
        main()
    finally:
        # Remove the lock file when the bot is done, to allow future instances to run
        os.remove(lock_file_path)
