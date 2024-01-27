from telebot.types import InlineKeyboardMarkup
from globals import application
from telegram import Update
from telegram.ext import ContextTypes
from telebot import types
import random
from model import UserLevel


def initialize_states(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if 'global' not in context.user_data:
        context.user_data['global'] = {
            'chat_id': update.message.chat.id,
            'level': UserLevel.junior,
            'result': [0, 0, 0],
            'access': [True, False, False],
            'invoice_message_id': 0,

        }
    if 'junior'not in context.user_data:
        update_junior_context(context)
    if 'middle'not in context.user_data:
        update_middle_context(context)
    if 'senior'not in context.user_data:
        update_senior_context(context)


def update_junior_context(context: ContextTypes.DEFAULT_TYPE):
    context.user_data['junior'] = {
        'number_of_correct': 0,
        'number_of_incorrect': 0,
        'correct_answer_index': 0,
        'selected_id_list': [],
        'question': '',
        'list_of_answers': [],
        'explanation': '',
        'number_of_question': 0,
        'explanation_code': ''
    }


def update_middle_context(context: ContextTypes.DEFAULT_TYPE):
    context.user_data['middle'] = {
        'number_of_correct': 0,
        'number_of_incorrect': 0,
        'correct_answer_index': 0,
        'selected_id_list': [],
        'question': '',
        'list_of_answers': [],
        'explanation': '',
        'number_of_question': 0,
        'explanation_code': ''
    }


def update_senior_context(context: ContextTypes.DEFAULT_TYPE):
    context.user_data['senior'] = {
        'number_of_correct': 0,
        'number_of_incorrect': 0,
        'correct_answer_index': 0,
        'selected_id_list': [],
        'question': '',
        'list_of_answers': [],
        'explanation': '',
        'number_of_question': 0,
        'explanation_code': ''
    }


async def send_message(chat_id: int, text: str, reply_markup: InlineKeyboardMarkup | None = None, parse_mode: str = 'HTML'):
    try:
        await application.bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=reply_markup.to_json(),
            parse_mode=parse_mode)
    except Exception as e:
        await application.bot.send_message(
            chat_id=chat_id,
            text=text,
            parse_mode=parse_mode
        )
        print(f"Произошла ошибка при изменении сообщения: {e}")


async def edit_message(chat_id: int, message_id: int, text: str, reply_markup: InlineKeyboardMarkup | None = None, parse_mode: str = 'HTML'):
    try:
        await application.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            reply_markup=reply_markup.to_json(),
            parse_mode=parse_mode
        )
    except Exception as e:
        await application.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            parse_mode=parse_mode
        )
        print(f"Произошла ошибка при изменении сообщения: {e}")


async def send_sticker(chat_id: int, sticker: str):
    await application.bot.send_sticker(
        chat_id=chat_id,
        sticker=sticker)


async def delete_message(chat_id: int, message_id: int):
    try:
        await application.bot.deleteMessage(
            chat_id=chat_id,
            message_id=message_id)
    except Exception as e:
        print(e)


async def create_buttons(list_of_buttons) -> []:
    return list(
        map(lambda button, i: types.InlineKeyboardButton(text=button, callback_data=str(list_of_buttons[i])),
            list_of_buttons,
            range(0, len(list_of_buttons))))


def get_random_number(context: ContextTypes.DEFAULT_TYPE, level: str) -> int:
    random_number = random.randint(0, 3)

    if random_number in context.user_data[level]['selected_id_list']:
        print(f"Generated {random_number}")
        return get_random_number(context, level)

    print(f"Generated {random_number}, it's not in the list.")
    return random_number
