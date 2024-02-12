from telegram import Update
from data.globals import PAYMENTS_TOKEN
from telegram.ext import ContextTypes
from interactor import get_section_data, get_level_data, delete_message, _
from telebot.types import LabeledPrice
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from screens_bulder import show_section_start_screen


async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    section_data = get_section_data(context)
    level_data = get_level_data(context)

    title = "Покупка {section} {level} уровня".format(
        section=section_data.name,
        level=level_data.name
    )
    description = "Доступ к уровню {level} навсегда".format(
        level=level_data.name
    )
    payload = "{section}-{level}-payload".format(
        section=section_data.name,
        level=level_data.name
    )
    currency = "RUB"
    prices = [LabeledPrice(label='Покупка {level} тарифа'.format(level=level_data.name), amount=level_data.price).to_dict()]
    pay_text = "Заплатить {prices} {currency}".format(prices=prices[0]['amount']/100, currency=currency)
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(pay_text, pay=True))
    keyboard.add(InlineKeyboardButton("Назад ⬅️", callback_data="Назад ⬅️ 1"))

    await delete_message(chat_id=update.effective_chat.id, message_id=update.callback_query.message.message_id)

    await context.bot.send_invoice(chat_id=update.effective_chat.id,
                                   title=title,
                                   description=description,
                                   provider_token=PAYMENTS_TOKEN,
                                   currency='RUB',
                                   payload=payload,
                                   is_flexible=False,
                                   prices=prices,
                                   start_parameter='start_parameter',
                                   reply_markup=keyboard.to_json())


async def handle_pre_checkout(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.pre_checkout_query

    section_data = get_section_data(context)
    level_data = get_level_data(context)

    if query.invoice_payload != '{section}-{level}-payload'.format(section=section_data.name, level=level_data.name):
        await query.answer(ok=False, error_message=_(context, "Something went wrong with the payment"))
    else:
        await query.answer(ok=True)
        level_data.is_paid = True
        await show_section_start_screen(update, context)


async def successful_payment_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await show_section_start_screen(update, context)