from telegram import Update
from globals import PAYMENTS_TOKEN, MIDDLE_PRICE, SENIOR_PRICE
from telegram.ext import ContextTypes
from model import UserLevel
from telebot import types
from interactor import delete_message


async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    level = context.user_data['global']['level']
    title = "Покупка Middle уровня" if level == UserLevel.unpaid_middle else "Покупка Senior уровня"
    description = "Доступ к уровню Middle навсегда" if level == UserLevel.unpaid_middle else "Доступ к уровню Senior навсегда"
    payload = "test-middle-payload" if level == UserLevel.unpaid_middle else "test-senior-payload"
    currency = "RUB"
    prices = [MIDDLE_PRICE.to_dict()] if level == UserLevel.unpaid_middle else [SENIOR_PRICE.to_dict()]

    pay_text = "Заплатить {prices} {currency}".format(prices=prices[0]['amount']/100,currency=currency)
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(pay_text, pay=True))
    keyboard.add(types.InlineKeyboardButton("Назад ⬅️", callback_data="Назад ⬅️ 1"))

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
