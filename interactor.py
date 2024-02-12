from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from data.translations import translations
from data.globals import application
from telegram.ext import ContextTypes
import random
from model import UserData, Level, Section, Interview, Theme
from telegram import Update
from collections import Counter


def get_chat_id(update: Update):
    return update.message.chat_id if update.message else update.callback_query.message.chat_id


def get_message_id(update: Update):
    return update.message.message_id if update.message else update.message.chat.id


async def send_message(chat_id: int, text: str, reply_markup: InlineKeyboardMarkup | None = None,
                       parse_mode: str = 'HTML'):
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
        print(f"Произошла ошибка при отправке сообщения: {e}")


async def edit_message(chat_id: int, message_id: int, text: str, reply_markup: InlineKeyboardMarkup | None = None,
                       parse_mode: str = 'HTML'):
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


async def create_buttons(list_of_buttons):
    if isinstance(list_of_buttons, list):
        return [InlineKeyboardButton(text=button, callback_data=button)
                for i, button in enumerate(list_of_buttons)]

    elif isinstance(list_of_buttons, dict):
        return [InlineKeyboardButton(text=value, callback_data=str(key))
                for key, value in list_of_buttons.items()]

    else:
        raise TypeError("list_of_buttons должен быть типа list или dict")


def get_random_number(context: ContextTypes.DEFAULT_TYPE, selected_id_list: [], end: int = 3) -> int:
    random_number = random.randint(0, end)

    if random_number in selected_id_list:
        print(f"Generated {random_number}")
        return get_random_number(context, selected_id_list)

    print(f"Generated {random_number}, it's not in the list.")
    return random_number


def get_data(context: ContextTypes.DEFAULT_TYPE) -> UserData | None:
    if 'data' in context.user_data:
        return context.user_data['data']
    else:
        return None


def get_level_name(context: ContextTypes.DEFAULT_TYPE) -> str:
    data = get_data(context)
    if data is not None:
        return data.common_data.level
    return ""


def get_level_data(context: ContextTypes.DEFAULT_TYPE) -> Level | None:
    data = get_data(context)
    section = get_section_data(context)
    if data is not None:
        for level in section.levels:
            if level.name == data.common_data.level:
                return level
    return None


def get_interview_data(context: ContextTypes.DEFAULT_TYPE) -> Interview | None:
    data = get_data(context)
    if data is not None:
        return data.interview_data
    return None


def get_section_data(context: ContextTypes.DEFAULT_TYPE) -> Section | None:
    data = get_data(context)
    theme = get_theme(context)
    if data is not None:
        for s in theme.sections:
            if s.name == data.common_data.section:
                return s
    return None


def get_theme(context: ContextTypes.DEFAULT_TYPE) -> Theme | None:
    data = get_data(context)
    if data is not None:
        for theme in data.theme_data:
            if theme.name == data.common_data.theme:
                return theme
    return None


def remove_most_frequent_elements(lst) -> []:
    if lst:
        element_counts = Counter(lst)
        max_count = max(element_counts.values())
        filtered_list = [element for element in lst if element_counts[element] != max_count]
        return filtered_list
    return []


async def add_jump_button(button_text, callback_data='') -> InlineKeyboardMarkup:
    keyboard_button = InlineKeyboardButton(text=button_text,
                                           callback_data=button_text if callback_data == '' else callback_data)
    reply_markup = InlineKeyboardMarkup(row_width=1)
    reply_markup.add(keyboard_button)
    return reply_markup


def change_level(context, level: str):
    context.user_data['data'].common_data.level = level


def _(context: ContextTypes.DEFAULT_TYPE, message: str):
    return translations[context.user_data['data'].common_data.user_language].get(message, "Translation not found")
