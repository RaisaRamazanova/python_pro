from telegram import Update
from data.globals import PAYMENTS_TOKEN
from telegram.ext import ContextTypes
from handlers.interactor import delete_message, _, create_buttons, get_message_id, get_chat_id, edit_message, send_message
from telebot.types import LabeledPrice
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from services.main_screen_service import show


async def show_pay_screen(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    list_of_buttons = {_(context, "Buy 💰"): _(context, "Buy 💰"),
                       'back to the main menu': _(context, "Back ⬅️")}
    keyboard_buttons = await create_buttons(list_of_buttons)
    reply_markup = InlineKeyboardMarkup(row_width=1)
    reply_markup.add(*keyboard_buttons)

    text = _(context, "Unlimited access to Frontend interviews is blocked")

    try:
        await edit_message(
            chat_id=get_chat_id(update),
            message_id=get_message_id(update),
            text=text,
            reply_markup=reply_markup)
    except Exception as e:
        try:
            await delete_message(
                chat_id=get_chat_id(update),
                message_id=get_message_id(update))
        except Exception as e:
            print(f"Не удалось удалить сообщение: {e}")

        await send_message(
            chat_id=get_chat_id(update),
            text=text,
            reply_markup=reply_markup)


async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    title = "Покупка доступа к Frontend собеседованиям"
    description = "Доступ к собеседованиям Frontend навсегда"
    payload = "interview-frontend-payload"
    currency = "RUB"
    # Specify price in kopecks
    prices = [LabeledPrice(label='Frontend', amount=100000).to_dict()]
    pay_text = f"Заплатить {prices[0]['amount']/100} {currency}"
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(pay_text, pay=True))
    keyboard.add(InlineKeyboardButton("Назад ⬅️", callback_data="back to pay screen"))

    # Assuming delete_message is a properly defined function
    if update.callback_query:
        await delete_message(chat_id=update.effective_chat.id, message_id=update.callback_query.message.message_id)

    await context.bot.send_invoice(
        chat_id=update.effective_chat.id,
        title=title,
        description=description,
        provider_token=PAYMENTS_TOKEN,
        currency=currency,
        payload=payload,
        is_flexible=False,
        prices=prices,
        start_parameter='start_parameter',
        reply_markup=keyboard.to_json()
    )


async def handle_pre_checkout(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.pre_checkout_query

    if query.invoice_payload != "interview-frontend-payload":
        await query.answer(ok=False, error_message=_(context, "Something went wrong with the payment"))
    else:
        await query.answer(ok=True)
        await show(update, context)


async def successful_payment_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await show(update, context)