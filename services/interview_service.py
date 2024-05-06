from telegram.ext import ContextTypes
from telegram import Update
from handlers.interactor import _, get_chat_id, pick_random_number, edit_message, get_message_id, add_jump_button
from services.onboarding_service import app_config
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


async def start_interview(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = app_config['user_repo'].get_user_id(telegram_id=update.effective_user.id)
    user_onboarding_id = app_config['onboarding_repo'].get_user_onboarding_id(user_id=user_id)

    interview_id = app_config['interview_repo'].start_interview(
        user_id=user_id,
        chat_id=get_chat_id(update)
    )

    app_config['interview_topic_repo'].record_interview_topics(
        interview_id=interview_id,
        user_onboarding_id=user_onboarding_id
    )

    await get_question_id(update, context)


async def get_question_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    question = app_config['question_repo'].get_question_by_question_id(question_id=question_id)
    number_of_question = app_config['interview_question_repo'].get_number_of_question(interview_id=interview_id)
    questions_count = app_config['system_setting_repo'].get_interview_question_count()

    text = _(context, "Interview\n\n❓Question {number_of_question}/{questions_count}: \n\n{question}").format(
        number_of_question=str(number_of_question + 1),
        questions_count=questions_count,
        question=question['content'])

    await show_question(text, interview_id, question_id, update, context)


async def show_question(text, interview_id, question_id, update, context):
    back_button = InlineKeyboardButton(text=_(context, "Save progress and exit"),
                                       callback_data=_(context, "Save progress and exit"))
    know_button = InlineKeyboardButton(text=_(context, 'I know'), callback_data=_(context, 'I know'))
    dont_know_button = InlineKeyboardButton(text=_(context, 'I don\'t know'),
                                            callback_data=_(context, 'I don\'t know'))

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


async def get_answer_from_data(update: Update, context: ContextTypes.DEFAULT_TYPE, is_known, text, end_button_text, interview_id):
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
    await show_feedback_by_answer(context, get_chat_id(update), question, is_known,
                                  number_of_question == questions_count,
                                  update, text, end_button_text)


async def show_feedback_by_answer(context, chat_id, question, is_known, is_last, update, start_text, end_button_text):
    answer_feedback = _(context, 'You know the answer') if is_known else \
        _(context, 'You don\'t know the answer')

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


async def show_interview_results_screen(update, context):
    reply_markup = await add_jump_button(_(context, "To the main menu ⬅️"), callback_data="back to the main menu")

    text = _(context, 'not enough data')
    await edit_message(
        chat_id=get_chat_id(update),
        message_id=update.callback_query.message.message_id,
        text=text,
        reply_markup=reply_markup)