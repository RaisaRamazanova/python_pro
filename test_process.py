from interactor import *
from telegram import Update
from interactor import _
from onboarding import app_config


async def show_question_screen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = app_config['user_repo'].get_user_id(telegram_id=update.effective_user.id)
    interview_id = app_config['interview_repo'].get_last_unfinished_interview_id(
        user_id=user_id,
        chat_id=get_chat_id(update)

    )

    language_id = app_config['user_repo'].get_language_id(chat_id=get_chat_id(update))

    topic_id, level = app_config['interview_topic_repo'].get_topic_with_insufficient_questions(
        interview_id=interview_id,
        user_id=user_id
    )
    questions_id = app_config['question_repo'].get_questions_by_parameters(
        topic_id=topic_id,
        level_id=level,
        is_enabled=True,
        language_id=language_id,
        interview_id=interview_id
    )

    question_id = pick_random_number(questions_id)

    await get_question_from_data(update, context, interview_id, question_id)


async def get_question_from_data(update, context, interview_id, question_id):
    question = app_config['question_repo'].get_question_by_question_id(
        question_id=question_id
    )

    answers_list = app_config['answer_repo'].get_answers_by_question_id(
        question_id=question_id
    )
    for answer in answers_list:
        answer_id = app_config['interview_question_answer_repo'].create_answer(
            interview_id=interview_id,
            answer_id=answer['id']
        )

    number_of_question = app_config['interview_question_repo'].get_number_of_question(interview_id=interview_id)

    if not answers_list:
        await one_answer_question(interview_id, number_of_question, question['content'], question_id, update, context)
    else:
        await four_answers_question(interview_id, number_of_question, question['content'], answers_list, update, context)


async def show_four_answers_feedback(update: Update, context: ContextTypes.DEFAULT_TYPE, selected_answer_index,
                                     text, next_button_text, interview_id):
    number_of_question = app_config['interview_question_repo'].get_number_of_question(interview_id=interview_id)
    questions_count = app_config['system_setting_repo'].get_interview_question_count()

    # if interview_id:
    #     interview = get_interview_data(context)
    #     section = get_section_data(context)
    #
    #     if section.code[0][0] in interview.percent_of_correct_answers_by_topic:
    #         interview.percent_of_correct_answers_by_topic[section.code[0][0]] += 1
    #     else:
    #         interview.percent_of_correct_answers_by_topic[section.code[0][0]] = 1
    #
    # if current_level_data.correct_answer_index == int(selected_answer_index):
    #     current_level_data.number_of_correct += 1
    #     await compose_four_answers_feedback(context, common_data.common_data.chat_id,
    #                                         number_of_question == questions_count,
    #                                         update, selected_answer_index, text, next_button_text, True)
    # else:
    #     current_level_data.number_of_incorrect += 1
    #     await compose_four_answers_feedback(context, common_data.common_data.chat_id,
    #                                         number_of_question == questions_count,
    #                                         update, selected_answer_index, text, next_button_text, False)


async def show_one_answer_feedback(update: Update, context: ContextTypes.DEFAULT_TYPE, is_known, text, end_button_text, interview_id):
    number_of_question = app_config['interview_question_repo'].get_number_of_question(interview_id=interview_id)
    questions_count = app_config['system_setting_repo'].get_interview_question_count()
    question_id = app_config['interview_question_repo'].get_last_unanswered_question(
        interview_id=interview_id
    )

    question = app_config['question_repo'].get_question_by_question_id(
        question_id=question_id
    )
    app_config['interview_question_repo'].answer_question(
        interview_id=interview_id,
        question_id=question_id,
        is_correct=is_known
    )
    await compose_one_answer_feedback(context, get_chat_id(update), question,
                                      number_of_question == questions_count,
                                      update, is_known, text, end_button_text)


async def compose_four_answers_feedback(context, chat_id, is_last, update, selected_answer_index, start_text,
                                        end_button_text, is_correct):
    # selected_answer = data.variable_data.list_of_answers[selected_answer_index][0]
    # correct_answer = data.variable_data.list_of_answers[data.variable_data.correct_answer_index][0]

    answer_feedback = _(context, '✅ You have selected an answer').format(
        selected_answer="TEST") if is_correct else \
        _(context, '❌ You have selected the answer').format(
            selected_answer="TEST",
            correct_answer="TEST"
        )

    await send_feedback(context, chat_id, is_last, update, answer_feedback, start_text, end_button_text)


async def compose_one_answer_feedback(context, chat_id, question, is_last, update, is_known, start_text, end_button_text):
    answer_feedback = _(context, 'You know the answer') if is_known else \
        _(context, 'You don\'t know the answer')

    await send_feedback(context, chat_id, question, is_last, update, answer_feedback, start_text, end_button_text)


async def send_feedback(context, chat_id, question, is_last, update, answer_feedback, start_text, end_button_text):
    total_text = start_text + ('{question}\n\n\n{answer_feedback}' +
                               _(context, '🧠 Explanation') +
                               '\n{explanation_code}').format(
        question=question['content'],
        answer_feedback=answer_feedback,
        explanation=question['explanation'],
        explanation_code=question['explanation_code'] if question['explanation_code'] != None else '')

    button_text = end_button_text if is_last else _(context, 'Next question ➡️')
    next_button = InlineKeyboardButton(text=button_text, callback_data=button_text)
    keyboard_buttons = [next_button]

    if not is_last:
        back_button = InlineKeyboardButton(text=_(context, "Save progress and exit"),
                                           callback_data=_(context, "Save progress and exit"))
        keyboard_buttons.append(back_button)

    reply_markup = InlineKeyboardMarkup([[button] for button in keyboard_buttons], row_width=1)

    await edit_message(chat_id, update.callback_query.message.message_id, total_text, reply_markup)


async def four_answers_question(interview_id, number_of_question, question, list_of_answers, update, context):
    if interview_id:
        questions_count = app_config['system_setting_repo'].get_interview_question_count()
        text = _(context, "Interview\n\n❓Question {number_of_question}/{questions_count}: \n\n{question}").format(
            number_of_question=str(number_of_question),
            questions_count=questions_count,
            question=question)
    else:
        questions_count = app_config['system_setting_repo'].get_theme_qustion_count()
        level = app_config['user_level_repo'].get_level()
        text = _(context, "Preparation for the interview for {level}").format(
            level=level,
            number_of_question=str(number_of_question),
            questions_count=questions_count,
            question=question)
    await show_question_with_four_answers(text, list_of_answers, update, context)


async def one_answer_question(interview_id, number_of_question, question, question_id, update, context):
    if interview_id:
        questions_count = app_config['system_setting_repo'].get_interview_question_count()
        text = _(context, "Interview\n\n❓Question {number_of_question}/{questions_count}: \n\n{question}").format(
            number_of_question=str(number_of_question + 1),
            questions_count=questions_count,
            question=question)
    else:
        level = app_config['user_level_repo'].get_level()
        questions_count = app_config['system_setting_repo'].get_theme_question_count()
        text = _(context, "Preparation for the interview for {level}").format(
            level=level,
            number_of_question=str(number_of_question + 1),
            questions_count=questions_count,
            question=question)

    await show_question_with_one_answer(text, interview_id, question_id, update, context)


async def show_question_with_four_answers(text, list_of_answers, update, context):
    back_button = InlineKeyboardButton(text=_(context, "Save progress and exit"),
                                       callback_data=_(context, "Save progress and exit"))
    keyboard_buttons = [InlineKeyboardButton(text=button[0], callback_data=str(i)) for i, button in
                        enumerate(list_of_answers)] + [back_button]

    reply_markup = InlineKeyboardMarkup([[button] for button in keyboard_buttons], row_width=1)

    await edit_message(
        chat_id=get_chat_id(update),
        message_id=get_message_id(update),
        text=text,
        reply_markup=reply_markup
    )


async def show_question_with_one_answer(text, interview_id, question_id, update, context):
    back_button = InlineKeyboardButton(text=_(context, "Save progress and exit"),
                                       callback_data=_(context, "Save progress and exit"))
    know_button = InlineKeyboardButton(text=_(context, 'I know'), callback_data=_(context, 'I know'))
    dont_know_button = InlineKeyboardButton(text=_(context, 'I don\'t know'), callback_data=_(context, 'I don\'t know'))

    keyboard_buttons = [[know_button, dont_know_button], [back_button]]

    reply_markup = InlineKeyboardMarkup(keyboard_buttons)

    app_config['interview_question_repo'].create_question(
        interview_id=interview_id,
        question_id=question_id
    )

    await edit_message(
        chat_id=get_chat_id(update),
        message_id=get_message_id(update),
        text=text,
        reply_markup=reply_markup
    )
