from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from data.translations import translations
from data.globals import application
from telegram.ext import ContextTypes
import random
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
from typing import IO
from io import BytesIO


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


async def send_image(chat_id: int, photo: IO[bytes], caption: str, reply_markup: InlineKeyboardMarkup | None = None):
    await application.bot.send_photo(
        chat_id=chat_id,
        photo=photo,
        caption=caption,
        reply_markup=reply_markup.to_json()
    )


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


def get_random_number(selected_id_list: [], end: int = 3) -> int:
    random_number = random.randint(1, end)

    if random_number in selected_id_list:
        print(f"Generated {random_number}")
        return get_random_number(selected_id_list)

    print(f"Generated {random_number}")
    return random_number


def remove_most_frequent_elements(lst) -> []:
    if lst:
        element_counts = Counter(lst)
        max_count = max(element_counts.values())
        filtered_list = [element for element in lst if element_counts[element] != max_count]
        return filtered_list
    return []


async def add_jump_button(button_text, callback_data='') -> InlineKeyboardMarkup:
    keyboard_button = InlineKeyboardButton(text=button_text, callback_data=button_text if callback_data == '' else callback_data)
    reply_markup = InlineKeyboardMarkup(row_width=1)
    reply_markup.add(keyboard_button)
    return reply_markup


def _(context: ContextTypes.DEFAULT_TYPE, message: str):
    return translations['ru'].get(message, "Translation not found")


def choose_color(value):
    if value < 11:
        return '#e53e3e'  # Красный
    elif value < 22:
        return '#f6a377'  # Красно-оранжевый
    elif value < 33:
        return '#f9d87c'  # Оранжевый
    elif value < 44:
        return '#faf089'  # Желто-оранжевый
    elif value < 55:
        return '#ffeeba'  # Желтый
    elif value < 66:
        return '#d4f7be'  # Светло-желтый
    elif value < 77:
        return '#9ae6b4'  # Желто-зеленый
    elif value < 88:
        return '#68d391'  # Светло-зеленый
    else:
        return '#38a169'  # Зеленый


def darken_color(hex_color, darken_percent):
    darken_factor = 1 - darken_percent / 100

    hex_color = hex_color.strip('#')
    rgb = (int(hex_color[:2], 16), int(hex_color[2:4], 16), int(hex_color[4:], 16))

    darker_rgb = tuple(max(min(int(comp * darken_factor), 255), 0) for comp in rgb)

    darker_hex = '#{:02x}{:02x}{:02x}'.format(*darker_rgb)
    return darker_hex


def send_graph(context, count: int, results: list) -> IO[bytes]:
    x_points = [i for i in range(1, count + 1)]
    y_points = results

    colors = [choose_color(value) for value in y_points]

    avg_value = np.mean(y_points)
    plt.axhline(y=avg_value, color=darken_color(choose_color(avg_value), 30), linestyle='--', label=f'Average: {avg_value:.2f}')

    plt.bar(x_points, y_points, color=colors, edgecolor='black')
    plt.xlabel(_(context, 'number of attempts'))
    plt.ylabel(_(context, 'completion percentage')+'%')
    plt.title(_(context, 'average result') + f'- {avg_value:.0f}%')

    plt.ylim(0, 110)
    x_min = min(x_points)
    x_max = max(x_points)
    plt.xticks(np.arange(x_min, x_max + 1, step=1))

    graph_img = BytesIO()
    plt.savefig(graph_img, format='png')
    plt.close()
    graph_img.seek(0)

    return graph_img
