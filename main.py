from telegram.ext import CallbackQueryHandler, PreCheckoutQueryHandler, filters, \
    MessageHandler
from button_handlers import button
from payment import successful_payment_callback, handle_pre_checkout
from data.globals import application, logger
from onboarding import start
from telegram import Update
from telegram.ext import CommandHandler


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
    main()
