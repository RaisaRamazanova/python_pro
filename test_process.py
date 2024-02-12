from database import get_question_from_data
from interactor import *
from telegram import Update

from interactor import _


async def show_question_screen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question_id = 0
    data = get_data(context)
    if data.common_data.is_interview:
        interview_data = get_interview_data(context)
        for key in interview_data.number_of_questions_by_topic:
            if interview_data.selected_questions_by_topics[key] < interview_data.number_of_questions_by_topic[key]:
                selected_id_list = get_interview_data(context).variable_data.selected_id_list
                ls = []
                for element in selected_id_list:
                    if int(str(element)[:5]) == key:
                        ls.append(int(str(element)[5:]))
                if len(ls) > 3:
                    list_of_index = remove_most_frequent_elements(ls)
                else:
                    list_of_index = ls
                id = get_random_number(context, list_of_index, 3)

                question_id = int(str(key) + str(id))
                break
    else:
        section = get_section_data(context)
        level = get_level_data(context)
        selected_id_list = get_level_data(context).variable_data.selected_id_list
        ls = []
        for element in selected_id_list:
            ls.append(int(str(element)[5:]))
        if len(ls) > 3:
            list_of_index = remove_most_frequent_elements(ls)
        else:
            list_of_index = ls
        id = get_random_number(context, list_of_index, 3)
        if section.code[0][0] == '3':
            question_id = int(str(section.code[0]) + str(id))
        else:
            question_id = int(str(section.code[0]) + str(level.code[0]) + str(id))

    await get_question_from_data(update, context, question_id)


async def show_answer_feedback(update: Update, context: ContextTypes.DEFAULT_TYPE, selected_answer_index, data, text, next_button_text):
    common_data = get_data(context)

    current_level_data = data.variable_data
    current_quantity = len(current_level_data.selected_id_list)
    final_quantity = data.questions_count - 1
    if current_level_data.correct_answer_index == int(selected_answer_index):
        current_level_data.number_of_correct += 1
        await send_answer_feedback(context, common_data.common_data.chat_id,
                                   current_quantity == final_quantity, data,
                                   update, selected_answer_index, text, next_button_text, True)
    else:
        current_level_data.number_of_incorrect += 1
        await send_answer_feedback(context, common_data.common_data.chat_id,
                                   current_quantity == final_quantity, data,
                                   update, selected_answer_index, text, next_button_text, False)


async def send_answer_feedback(context, chat_id, is_last, data, update, selected_answer_index, start_text, next_button_text, is_correct):
    selected_answer = data.variable_data.list_of_answers[selected_answer_index][0]
    correct_answer = data.variable_data.list_of_answers[data.variable_data.correct_answer_index][0]

    answer_feedback = _(context, '✅ You have selected an answer: <b>{selected_answer}</b>\n\n\n').format(selected_answer=selected_answer) if is_correct else \
        _(context, '❌ You have selected the answer: <b>{selected_answer}</b>\n\n✅ Correct answer: <b>{correct_answer}</b>\n\n\n').format(
        selected_answer=selected_answer,
        correct_answer=correct_answer
    )

    total_text = start_text + ('{question}\n\n\n{answer_feedback}'+
            _(context, '🧠 <b>Explanation:</b>\n{explanation}')+
            '{explanation_code}').format(
        question=data.variable_data.question,
        answer_feedback=answer_feedback,
        explanation=data.variable_data.explanation,
        explanation_code=data.variable_data.explanation_code)

    button_text = next_button_text if is_last else _(context, 'Next question ➡️')
    next_button = InlineKeyboardButton(text=button_text, callback_data=button_text)
    keyboard_buttons = [next_button]

    if not is_last:
        back_button = InlineKeyboardButton(text=_(context, "Save progress and exit"),
                                           callback_data=_(context, "Save progress and exit"))
        keyboard_buttons.append(back_button)

    reply_markup = InlineKeyboardMarkup([[button] for button in keyboard_buttons], row_width=1)

    await edit_message(chat_id, update.callback_query.message.message_id, total_text, reply_markup)

    data.variable_data.number_of_question += 1
    interview_data = get_interview_data(context)
    for key in interview_data.number_of_questions_by_topic:
        if interview_data.selected_questions_by_topics[key] < interview_data.number_of_questions_by_topic[key]:
            interview_data.selected_questions_by_topics[key] += 1
    data.variable_data.selected_id_list.append(data.variable_data.question_id)


async def send_question_data(question, explanation, explanation_code, list_of_answers, question_id, update, context):
    correct_index = next((i for i, answer in enumerate(list_of_answers) if answer[1] == 1), None)
    if correct_index is None:
        raise ValueError("Отсутствует правильный ответ в списке ответов")

    is_interview = get_data(context).common_data.is_interview
    data = get_interview_data(context) if is_interview else get_level_data(context)
    data.variable_data.update(
        question=question,
        list_of_answers=list_of_answers,
        explanation=explanation,
        explanation_code=explanation_code,
        correct_answer_index=correct_index,
        question_id=question_id)

    if is_interview:
        text = _(context, "Interview\n\n❓Question {number_of_question}/{questions_count}: \n\n{question}").format(
            number_of_question=str(data.variable_data.number_of_question),
            questions_count=data.questions_count,
            question=question)
    else:
        text = _(context, "Preparation for the interview for {level}\n\n❓Question {number_of_question}/{questions_count}: \n\n{question}").format(
            level=data.name,
            number_of_question=str(data.variable_data.number_of_question),
            questions_count=data.questions_count,
            question=question)
    await show_question(text, list_of_answers, update, context)


async def show_question(text, list_of_answers, update, context):
    back_button = InlineKeyboardButton(text=_(context, "Save progress and exit"),
                                       callback_data=_(context, "Save progress and exit"))
    keyboard_buttons = [InlineKeyboardButton(text=button[0], callback_data=str(i)) for i, button in
                        enumerate(list_of_answers)] + [back_button]

    reply_markup = InlineKeyboardMarkup([[button] for button in keyboard_buttons], row_width=1)

    await edit_message(
        chat_id=get_data(context).common_data.chat_id,
        message_id=update.callback_query.message.message_id,
        text=text,
        reply_markup=reply_markup
    )