from database import get_question_from_data, add_questions
from interactor import *
from telegram import Update
from model import UserLevel
from payment import buy


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    initialize_states(update, context)
    update_junior_context(context)
    update_middle_context(context)
    update_senior_context(context)
    await show_start_screen(update, context)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    code = update.callback_query.data

    actions = {
        'Новичок (Junior)': lambda: change_level_and_ask_question(update, context, UserLevel.junior),
        'Средний уровень (Middle) 🔒': lambda: change_level_and_pay(update, context, UserLevel.unpaid_middle),
        'Продвинутый уровень (Senior) 🔒': lambda: change_level_and_pay(update, context, UserLevel.unpaid_senior),
        'Средний уровень (Middle)': lambda: change_level_and_ask_question(update, context, UserLevel.paid_middle),
        'Продвинутый уровень (Senior)': lambda: change_level_and_ask_question(update, context, UserLevel.paid_senior),
        'Вернуться на главную страницу': lambda: return_to_start_screen(update, context),
        'Посмотреть результат': lambda: send_level_completion_message(update, context),
        'Назад ⬅️': lambda: set_level_and_show_start(update, context, UserLevel.junior),
        'Назад ⬅️ 1': lambda: return_to_pay_screen(update, context),
        'Купить 💰': lambda: buy(update, context),
        'Следующий вопрос': lambda: ask_question(update, context)
    }

    try:
        int_code = int(code)
        await handle_training_process(update, context, int_code)
    except ValueError:
        if code in actions:
            await actions[code]()


async def return_to_pay_screen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['global']['invoice_message_id'] = update.callback_query.message.message_id
    await pay_screen(update, context)


async def successful_payment_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await show_start_screen(update, context)


async def change_level_and_ask_question(update: Update, context: ContextTypes.DEFAULT_TYPE, level: UserLevel):
    await change_level(context, level)
    await ask_question(update, context)


async def ask_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    level = get_level(context)
    context.user_data[level]['number_of_question'] += 1
    question_id = get_random_number(context, level)
    context.user_data[level]['selected_id_list'].append(question_id)

    await get_question_from_data(update, context, question_id, level)


async def change_level_and_pay(update: Update, context: ContextTypes.DEFAULT_TYPE, level):
    await change_level(context, level)
    await pay_screen(update, context)


async def return_to_start_screen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    level = get_level(context)
    if level == 'junior':
        update_junior_context(context)
    elif level == 'middle':
        update_middle_context(context)
    elif level == 'senior':
        update_senior_context(context)
    await show_start_screen(update, context)


async def set_level_and_show_start(update: Update, context: ContextTypes.DEFAULT_TYPE, level):
    context.user_data['global']['level'] = level
    await show_start_screen(update, context)


async def handle_pre_checkout(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.pre_checkout_query

    if query.invoice_payload != 'test-middle-payload' and query.invoice_payload != 'test-senior-payload':
        await query.answer(ok=False, error_message="Что-то пошло не так c оплатой")
    else:
        await query.answer(ok=True)

        level = context.user_data['global']['level']
        if level == UserLevel.unpaid_middle:
            await change_level(context, UserLevel.paid_middle)
            await change_access(context, UserLevel.paid_middle)
        elif level == UserLevel.unpaid_senior:
            await change_level(context, UserLevel.paid_senior)
            await change_access(context, UserLevel.paid_senior)

        await show_start_screen(update, context)


async def show_start_screen(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    middle = 'Средний уровень (Middle)' if context.user_data['global']['access'][1] == True else 'Средний уровень (Middle) 🔒'
    senior = 'Продвинутый уровень (Senior)' if context.user_data['global']['access'][2] == True else 'Продвинутый уровень (Senior) 🔒'

    list_of_buttons = ['Новичок (Junior)', middle, senior]
    keyboard_buttons = await create_buttons(list_of_buttons)
    reply_markup = types.InlineKeyboardMarkup(row_width=1)
    reply_markup.add(*keyboard_buttons)

    record_text = ''
    if 'global' in context.user_data and 'level' in context.user_data['global'] and context.user_data['global']['level'] != UserLevel.none:
        results_text = ""
        print(context.user_data['global']['result'])
        if 'result' in context.user_data['global']:
            for i in range(len(context.user_data['global']['result'])):
                if context.user_data['global']['result'][i] > 0:
                    results_text += "🏆 {level}: {result}% верно\n\n".format(
                        level=list_of_buttons[i],
                        result=context.user_data['global']['result'][i]
                    )
        if results_text:
            record_text += "<b>Твои лучшие прошлые результаты:</b>\n" + results_text

    text = ("Привет!\n"
            "Здесь ты можешь тренироваться проходить <b>техническую часть собеседования</b> на позицию Python developer\n\n"
            + record_text +
            "Выбери модуль, по которому будешь тренировать техническую часть\n\n\n").format(record_text=record_text)
    try:
        if update.callback_query:
            await edit_message(
                chat_id=context.user_data['global']['chat_id'],
                message_id=update.callback_query.message.message_id,
                reply_markup=reply_markup,
                text=text)
        else:
            await update.message.reply_text(text, reply_markup=reply_markup.to_json(), parse_mode='HTML')
    except Exception as e:
        print(f"Ошибка: {e}")


async def pay_screen(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    list_of_buttons = ['Купить 💰', 'Назад ⬅️']
    keyboard_buttons = await create_buttons(list_of_buttons)
    reply_markup = types.InlineKeyboardMarkup(row_width=1)
    reply_markup.add(*keyboard_buttons)

    text = "Это платный уровень. Пока он заблокирован 🔒\n\n<b>Ты можешь купить его 💰</b>"

    try:
        await edit_message(
            chat_id=context.user_data['global']['chat_id'],
            message_id=update.callback_query.message.message_id,
            text=text,
            reply_markup=reply_markup)
    except Exception as e:
        invoice_message_id = context.user_data['global']['invoice_message_id']
        if invoice_message_id:
            try:
                await delete_message(
                    chat_id=context.user_data['global']['chat_id'],
                    message_id=invoice_message_id)
            except Exception as e:
                print(f"Не удалось удалить сообщение: {e}")

            await send_message(
                chat_id=context.user_data['global']['chat_id'],
                text=text,
                reply_markup=reply_markup)


def get_level(context: ContextTypes.DEFAULT_TYPE) -> str:
    if context.user_data['global']['level'] == UserLevel.junior:
        return 'junior'
    elif context.user_data['global']['level'] == UserLevel.paid_middle:
        return 'middle'
    elif context.user_data['global']['level'] == UserLevel.paid_senior:
        return 'senior'
    return 'junior'


async def show_question(question, answer_explanation, explanation_photo_url, list_of_answers, update, context):
    level = get_level(context)

    correct_index = next((i for i, answer in enumerate(list_of_answers) if answer[1] == 1), None)
    if correct_index is None:
        raise ValueError("Отсутствует правильный ответ в списке ответов")

    context.user_data[level].update({
        'question': question,
        'list_of_answers': list_of_answers,
        'explanation': answer_explanation,
        'explanation_code': explanation_photo_url,
        'correct_answer_index': correct_index
    })

    keyboard_buttons = [types.InlineKeyboardButton(text=button[0], callback_data=str(i)) for i, button in
                        enumerate(list_of_answers)]
    reply_markup = types.InlineKeyboardMarkup([[button] for button in keyboard_buttons], row_width=1)

    text = 'Подготовка к интервью для {level}\n\n❓Вопрос {number_of_question}/4: \n\n{question}'.format(
        level=context.user_data['global']['level'].value,
        number_of_question=context.user_data[level]['number_of_question'],
        question=question)

    await edit_message(
        chat_id=context.user_data['global']['chat_id'],
        message_id=update.callback_query.message.message_id,
        text=text,
        reply_markup=reply_markup
    )

    context.user_data[level]['correct_answer_index'] = correct_index


async def change_access(context, level):
    if level == UserLevel.paid_middle:
        context.user_data['global']['access'][1] = True
    elif level == UserLevel.paid_senior:
        context.user_data['global']['access'][2] = True


async def change_level(context, level):
    context.user_data['global']['level'] = level


async def send_level_completion_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    level = get_level(context)
    percentage_correct = int((context.user_data[level]['number_of_correct'] * 100) / 4)
    reply_markup = await add_jump_button('Вернуться на главную страницу')

    if level == 'junior' and context.user_data['global']['result'][0] < percentage_correct:
        context.user_data['global']['result'][0] = percentage_correct
    elif level == 'middle' and context.user_data['global']['result'][1] < percentage_correct:
        context.user_data['global']['result'][1] = percentage_correct
    elif level == 'senior' and context.user_data['global']['result'][2] < percentage_correct:
        context.user_data['global']['result'][2] = percentage_correct
    await edit_message(
        chat_id=context.user_data['global']['chat_id'],
        message_id=update.callback_query.message.message_id,
        text="<b>Ты закончил тренировку технической части собеседования!</b>\n\nПравильно выполнено {percent}% ({correct} из 4)".format(
            percent=percentage_correct,
            correct=context.user_data[level]['number_of_correct']),
        reply_markup=reply_markup
    )


async def handle_training_process(update: Update, context: ContextTypes.DEFAULT_TYPE, selected_answer_index):
    level = get_level(context)
    count = len(context.user_data[level]['selected_id_list'])
    if context.user_data[level]['correct_answer_index'] == int(selected_answer_index):
        context.user_data[level]['number_of_correct'] += 1
        await send_answer_feedback(context.user_data['global']['chat_id'], True if count == 4 else False, context, update, selected_answer_index, True)
    else:
        context.user_data[level]['number_of_incorrect'] += 1
        await send_answer_feedback(context.user_data['global']['chat_id'], True if count == 4 else False, context, update, selected_answer_index, False)


async def send_answer_feedback(chat_id, is_last, context, update, selected_answer_index, is_correct):
    if is_correct:
        answer_feedback = '✅ Вы выбрали ответ: <b>{selected_answer}</b>\n\n\n'
    else:
        answer_feedback = (
            '❌ Вы выбрали ответ: <b>{selected_answer}</b>\n\n'
            '✅ Правильный ответ: <b>{correct_answer}</b>\n\n\n'
        )

    level = get_level(context)
    text = (
        'Подготовка к интервью для {level}\n\n'
        '<b>❓Вопрос {number_of_question}/4:</b>\n\n'
        '{question}\n\n\n'
        + answer_feedback +
        '🧠 <b>Объяснение:</b>\n{explanation}'
        '{explanation_code}'
    ).format(
        level=context.user_data['global']['level'].value,
        number_of_question=context.user_data[level]['number_of_question'],
        question=context.user_data[level]['question'],
        selected_answer=context.user_data[level]['list_of_answers'][selected_answer_index][0],
        correct_answer=context.user_data[level]['list_of_answers'][context.user_data[level]['correct_answer_index']][0],
        explanation=context.user_data[level]['explanation'],
        explanation_code=context.user_data[level]['explanation_code']
    )

    reply_markup = await add_jump_button('Посмотреть результат' if is_last else 'Следующий вопрос')
    await edit_message(chat_id, update.callback_query.message.message_id, text, reply_markup)


async def add_jump_button(button_text):
    keyboard_button = types.InlineKeyboardButton(text=button_text, callback_data=button_text)
    reply_markup = types.InlineKeyboardMarkup(row_width=1)
    reply_markup.add(keyboard_button)
    return reply_markup
