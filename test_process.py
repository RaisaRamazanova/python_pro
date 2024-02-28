from database import get_question_from_data
from interactor import *
from telegram import Update
from data.globals import STAGE_MAPPING_LEVELS
from interactor import _


async def show_question_screen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    themes = [_(context, "Programming languages"), _(context, "Frameworks"), _(context, "Tools"), _(context, "Theory")]
    question_id = '1' if context.user_data['data'].common_data.user_language == 'ru' else '2' if context.user_data[
                                                                                                     'data'].common_data.user_language == 'en' else None

    is_one_answer = True
    data = get_data(context)
    if data.common_data.is_interview:
        interview_data = get_interview_data(context)
        for key in interview_data.number_of_questions_by_topic:
            if interview_data.selected_questions_by_topics[key] < interview_data.number_of_questions_by_topic[key]:
                selected_id_list = get_interview_data(context).variable_data.selected_id_list
                ls = []
                for element in selected_id_list:
                    if int(str(element)[1:6]) == key:
                        ls.append(int(str(element)[7:]))
                if len(ls) > 20:
                    list_of_index = remove_most_frequent_elements(ls)
                else:
                    list_of_index = ls
                id = get_random_number(context, list_of_index, 20)
                for (k, v) in context.user_data['unique_codes'].items():
                    if v == int(str(key)[:4]):
                        with open('/Users/raisatramazanova/development/python_bot/python_pro_bot/data/four_answers.txt', 'r') as file:
                            lines = file.readlines()
                            for line in lines:
                                if k == line.strip():
                                    is_one_answer = False
                        get_data(context).common_data.theme = k
                        get_data(context).common_data.theme = themes[int(str(key)[:1]) - 1]
                        get_data(context).common_data.section = k
                        break
                get_data(context).common_data.level = STAGE_MAPPING_LEVELS[int(str(key)[4:]) - 1]
                question_id += str(key) + ('2' if is_one_answer else '1') + str(id)
                break
    else:
        section = get_section_data(context)
        level = get_level_data(context)
        selected_id_list = get_level_data(context).variable_data.selected_id_list
        ls = []
        for element in selected_id_list:
            ls.append(int(str(element)[7:]))
        if len(ls) > 20:
            list_of_index = remove_most_frequent_elements(ls)
        else:
            list_of_index = ls
        id = get_random_number(context, list_of_index, 20)
        if section.code[0][0] == '3':
            question_id += str(section.code[0]) + ('2' if is_one_answer else '1')+ str(id)
        else:
            question_id += str(section.code[0]) + str(level.code[0]) + ('2' if is_one_answer else '1') + str(id)

    await get_question_from_data(update, context, int(question_id))


async def show_four_answers_feedback(update: Update, context: ContextTypes.DEFAULT_TYPE, selected_answer_index, data,
                                     text, next_button_text):
    common_data = get_data(context)

    current_level_data = data.variable_data
    current_quantity = len(current_level_data.selected_id_list)
    final_quantity = data.questions_count - 1

    if common_data.common_data.is_interview:
        interview = get_interview_data(context)
        section = get_section_data(context)

        if section.code[0][0] in interview.percent_of_correct_answers_by_topic:
            interview.percent_of_correct_answers_by_topic[section.code[0][0]] += 1
        else:
            interview.percent_of_correct_answers_by_topic[section.code[0][0]] = 1

    if current_level_data.correct_answer_index == int(selected_answer_index):
        current_level_data.number_of_correct += 1
        await compose_four_answers_feedback(context, common_data.common_data.chat_id,
                                            current_quantity == final_quantity, data,
                                            update, selected_answer_index, text, next_button_text, True)
    else:
        current_level_data.number_of_incorrect += 1
        await compose_four_answers_feedback(context, common_data.common_data.chat_id,
                                            current_quantity == final_quantity, data,
                                            update, selected_answer_index, text, next_button_text, False)


async def show_one_answer_feedback(update: Update, context: ContextTypes.DEFAULT_TYPE, is_known, data, text,
                                   end_button_text):
    common_data = get_data(context)

    current_level_data = data.variable_data
    current_quantity = len(current_level_data.selected_id_list)
    final_quantity = data.questions_count - 1

    if common_data.common_data.is_interview:
        interview = get_interview_data(context)
        section = get_section_data(context)

        if section.code[0][0] in interview.percent_of_correct_answers_by_topic:
            interview.percent_of_correct_answers_by_topic[section.code[0][0]] += 1
        else:
            interview.percent_of_correct_answers_by_topic[section.code[0][0]] = 1

    if is_known:
        current_level_data.number_of_correct += 1
        await compose_one_answer_feedback(context, common_data.common_data.chat_id,
                                          current_quantity == final_quantity, data,
                                          update, is_known, text, end_button_text)
    else:
        current_level_data.number_of_incorrect += 1
        await compose_one_answer_feedback(context, common_data.common_data.chat_id,
                                          current_quantity == final_quantity, data,
                                          update, is_known, text, end_button_text)


async def compose_four_answers_feedback(context, chat_id, is_last, data, update, selected_answer_index, start_text,
                                        end_button_text, is_correct):
    selected_answer = data.variable_data.list_of_answers[selected_answer_index][0]
    correct_answer = data.variable_data.list_of_answers[data.variable_data.correct_answer_index][0]

    answer_feedback = _(context, '✅ You have selected an answer').format(
        selected_answer=selected_answer) if is_correct else \
        _(context, '❌ You have selected the answer').format(
            selected_answer=selected_answer,
            correct_answer=correct_answer
        )

    await send_feedback(context, chat_id, is_last, data, update, answer_feedback, start_text, end_button_text)


async def compose_one_answer_feedback(context, chat_id, is_last, data, update, is_known, start_text, end_button_text):
    answer_feedback = _(context, 'You know the answer') if is_known else \
        _(context, 'You don\'t know the answer')

    await send_feedback(context, chat_id, is_last, data, update, answer_feedback, start_text, end_button_text)


async def send_feedback(context, chat_id, is_last, data, update, answer_feedback, start_text, end_button_text):
    total_text = start_text + ('{question}\n\n\n{answer_feedback}' +
                               _(context, '🧠 Explanation') +
                               '{explanation_code}').format(
        question=data.variable_data.question,
        answer_feedback=answer_feedback,
        explanation=data.variable_data.explanation,
        explanation_code=data.variable_data.explanation_code)
    print('explanation_code = ', data.variable_data.explanation_code)

    button_text = end_button_text if is_last else _(context, 'Next question ➡️')
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
            break
    data.variable_data.selected_id_list.append(data.variable_data.question_id)


async def four_answers_question(question, explanation, explanation_code, list_of_answers, question_id, update, context):
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
        text = _(context, "Preparation for the interview for {level}").format(
            level=data.name,
            number_of_question=str(data.variable_data.number_of_question),
            questions_count=data.questions_count,
            question=question)
    await show_question_with_four_answers(text, list_of_answers, update, context)


async def one_answers_question(question, explanation, question_id, update, context):
    is_interview = get_data(context).common_data.is_interview
    data = get_interview_data(context) if is_interview else get_level_data(context)
    data.variable_data.update(
        question=question,
        list_of_answers=[],
        explanation=explanation,
        explanation_code='',
        correct_answer_index=0,
        question_id=question_id)

    if is_interview:
        text = _(context, "Interview\n\n❓Question {number_of_question}/{questions_count}: \n\n{question}").format(
            number_of_question=str(data.variable_data.number_of_question),
            questions_count=data.questions_count,
            question=question)
    else:
        text = _(context, "Preparation for the interview for {level}").format(
            level=data.name,
            number_of_question=str(data.variable_data.number_of_question),
            questions_count=data.questions_count,
            question=question)
    await show_question_with_one_answer(text, update, context)


async def show_question_with_four_answers(text, list_of_answers, update, context):
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


async def show_question_with_one_answer(text, update, context):
    back_button = InlineKeyboardButton(text=_(context, "Save progress and exit"),
                                       callback_data=_(context, "Save progress and exit"))
    know_button = InlineKeyboardButton(text=_(context, 'I know'), callback_data=_(context, 'I know'))
    dont_know_button = InlineKeyboardButton(text=_(context, 'I don\'t know'), callback_data=_(context, 'I don\'t know'))

    keyboard_buttons = [[know_button, dont_know_button], [back_button]]

    reply_markup = InlineKeyboardMarkup(keyboard_buttons)

    await edit_message(
        chat_id=get_data(context).common_data.chat_id,
        message_id=update.callback_query.message.message_id,
        text=text,
        reply_markup=reply_markup
    )
