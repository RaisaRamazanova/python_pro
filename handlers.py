from telegram import Update
from telegram.ext import ContextTypes
from telebot import types
from telebot.types import KeyboardButton, ReplyKeyboardMarkup


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    reply_markup = ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton("Junior"),
        KeyboardButton("Middle"),
        KeyboardButton("Senior"),
        row_width=1).to_json()

    await update.message.reply_text("Привет! Укажи свой уровень", reply_markup=reply_markup)


async def set_event(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.text == 'Junior':
        await update.effective_message.reply_text("Твой уровень Junior")
    elif update.message.text == 'Middle':
        await update.effective_message.reply_text("Твой уровень Middle")
    elif update.message.text == 'Senior':
        await update.effective_message.reply_text("Твой уровень JuSeniornior")