from typing import Any
from database import get_question, good_stickers_id_list
from interactor import *


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    initialize_states(update, context)
    await show_start_screen(update, context)

    global global_state
    global_state = context.user_data['global']

    global junior_state
    junior_state = context.user_data['junior']


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    code = update.callback_query.data

    try:
        int_code = int(code)
        await handle_training_process(int_code, context)
    except ValueError:
        if code == 'Новичок (Junior)':
            await handle_level_change(update, context, code)
            await start_junior(context)
        elif code in ['Средний уровень (Middle) 🔒', 'Продвинутый уровень (Senior) 🔒']:
            await pay_screen(update, context)
        elif code == 'Вернуться на главную страницу':
            update_junior_context(context)
            global junior_state
            junior_state = context.user_data['junior']
            await show_start_screen(update, context)
        elif code == 'Назад ⬅️':
            await show_start_screen(update, context)
        elif code == 'Купить 💰':
            context.user_data['global']['access'] = True
            await show_start_screen(update, context)
        elif code == 'Следующий вопрос' and context.user_data['global']['level'] == 'Новичок (Junior)':
            await start_junior(context)


async def show_start_screen(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    access = context.user_data['global']['access']
    levels = [('Новичок (Junior)', 'Средний уровень (Middle)', 'Продвинутый уровень (Senior)'),
              ('Новичок (Junior)', 'Средний уровень (Middle) 🔒', 'Продвинутый уровень (Senior) 🔒')]
    list_of_buttons = levels[0] if access else levels[1]
    keyboard_buttons = await create_buttons(list_of_buttons)
    reply_markup = types.InlineKeyboardMarkup(row_width=1)
    reply_markup.add(*keyboard_buttons)
    text = ("Привет!\nЗдесь ты можешь тренироваться проходить техническую часть собеседования на позицию Python "
            "developer\n\nВыбери модуль, по которому будешь проходить собеседование\n")

    try:
        await update.message.reply_text(text, reply_markup=reply_markup.to_json())
    except Exception as e:
        await edit_message(
            chat_id=context.user_data['global']['chat_id'],
            message_id=update.callback_query.message.message_id,
            text=text,
            reply_markup=reply_markup)


async def pay_screen(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    list_of_buttons = ['Купить 💰', 'Назад ⬅️']
    keyboard_buttons = await create_buttons(list_of_buttons)
    reply_markup = types.InlineKeyboardMarkup(row_width=1)
    reply_markup.add(*keyboard_buttons)

    text = "Это платный уровень. Пока он заблокирован 🔒\nТы можешь купить его 💰"
    await edit_message(
        chat_id=context.user_data['global']['chat_id'],
        message_id=update.callback_query.message.message_id,
        text=text,
        reply_markup=reply_markup)


async def show_question(question, answer_explanation, explanation_photo_url, list_of_answers: list[tuple[Any, Any]]):
    correct_index = None

    junior_state['explanation'] = answer_explanation
    junior_state['explanation_code'] = explanation_photo_url

    for i, answer in enumerate(list_of_answers):
        if answer[1] == 1:
            correct_index = i
            break

    keyboard_buttons = list(map(lambda button, i: types.InlineKeyboardButton(text=button[0], callback_data=str(i)), list_of_answers,
            range(0, len(list_of_answers))))
    reply_markup = types.InlineKeyboardMarkup(row_width=1)
    reply_markup.add(*keyboard_buttons)

    text = f'*_❓Вопрос {junior_state['number_of_question']}/4:_*\n\n{question}'
    await send_message(
        chat_id=global_state['chat_id'],
        text=text,
        reply_markup=reply_markup
    )

    junior_state['correct_answer_index'] = correct_index


async def handle_level_change(update, context, level):
    context.user_data['global']['level'] = level
    await edit_message(
        chat_id=context.user_data['global']['chat_id'],
        message_id=update.callback_query.message.message_id,
        text=f"Подготовка к интервью для {context.user_data['global']['level']}"
    )


async def start_junior(context):
    context.user_data['junior']['number_of_question'] += 1
    question_id = get_random_number(context)
    junior_state['selected_id_list'].append(question_id)
    await get_question(question_id)


# TODO: использовать в коде
async def send_level_completion_message(context: ContextTypes.DEFAULT_TYPE):
    percentage_correct = int((context.user_data['junior']['number_of_correct'] * 100) / 4)
    await send_sticker(
        chat_id=context.user_data['global']['chat_id'],
        sticker=random.choice(good_stickers_id_list)
    )

    reply_markup = await add_jump_button('Вернуться на главную страницу')
    await send_message(
        chat_id=global_state['chat_id'],
        text=f"*Вы закончили 1\-ый уровень\!*\n\nПравильно выполнено {percentage_correct}\% \({junior_state['number_of_correct']} из 4\)",
        reply_markup=reply_markup
    )


async def handle_training_process(code, context):
    count = len(context.user_data['junior']['selected_id_list'])
    if junior_state['correct_answer_index'] == int(code):
        junior_state['number_of_correct'] += 1
        await send_correct_answer_feedback(global_state['chat_id'], True if count == 4 else False)
    else:
        junior_state['number_of_incorrect'] += 1
        await send_incorrect_answer_feedback(global_state['chat_id'], True if count == 4 else False)


async def send_correct_answer_feedback(chat_id, is_last: bool):
    await send_message(chat_id, f"*✅ Верно\!\n\n\n🧠 Объяснение\:*\n\n{junior_state['explanation']}")
    reply_markup = await add_jump_button('Вернуться на главную страницу' if is_last else 'Следующий вопрос')
    await send_message(chat_id, junior_state['explanation_code'], reply_markup, parse_mode='HTML')


async def send_incorrect_answer_feedback(chat_id, is_last: bool):
    await send_message(chat_id,f"*❌ Не верно \:\(\n\n\n🧠 Объяснение\:*\n{junior_state['explanation']}")
    reply_markup = await add_jump_button('Вернуться на главную страницу' if is_last else 'Следующий вопрос')
    await send_message(chat_id, junior_state['explanation_code'], reply_markup, parse_mode='HTML')


async def add_jump_button(button_text):
    keyboard_button = types.InlineKeyboardButton(text=button_text, callback_data=button_text)
    reply_markup = types.InlineKeyboardMarkup(row_width=1)
    reply_markup.add(keyboard_button)
    return reply_markup
