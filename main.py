from telegram import Update
from telegram.ext import filters
from telegram.ext import CommandHandler, MessageHandler, CallbackQueryHandler
from handlers import start, set_event
from globals import application, logger


def main():
    application.add_handler(CommandHandler(["start"], start))
    application.add_handler(MessageHandler(filters.TEXT, set_event))
    application.add_error_handler(error_handler)

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
    main()