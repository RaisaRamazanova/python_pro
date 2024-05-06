from handlers.interactor import _
from services.main_screen_service import *
from services.payment_service import buy, show_pay_screen
from services.onboarding_service import return_to_previous_onboarding_step, start_onboarding, show_onboarding
from services.interview_service import get_question_id, get_answer_from_data, start_interview, \
    show_interview_results_screen


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    code = query.data

    user_id = app_config['user_repo'].get_user_id(telegram_id=update.effective_user.id)
    interview_id = app_config['interview_repo'].get_last_unfinished_interview_id(
        user_id=user_id,
        chat_id=get_chat_id(update)
    )

    actions = {
        _(context, "Finish the interview"): lambda: show(update, context, query),
        _(context, "Save progress and exit"): lambda: show(update, context, query),
        _(context, "View interview result"): lambda: send_interview_completion_message(update, context, interview_id),
        'back to pay screen': lambda: show_pay_screen(update, context),
        "back to the main menu": lambda: show(update, context, query),
        'back': lambda: return_to_previous_onboarding_step(update, context, query),
        translations['en']['start']: lambda: start_onboarding(update, context, query),
        translations['ru']['start']: lambda: start_onboarding(update, context, query),
        _(context, "Start the interview 🤺"): lambda: start_interview(update, context),
        _(context, "interview results"): lambda: show_interview_results_screen(update, context),
        _(context, "Change interview topics 🔁"): lambda: start_onboarding(update, context, query),
        _(context, "Buy 💰"): lambda: buy(update, context),
        _(context, "Buy access 💰"): lambda: show_pay_screen(update, context),
        _(context, 'Next question ➡️'): lambda: get_question_id(update, context),
        _(context, 'I don\'t know'):lambda: handle_answer_question(update, context, code, interview_id),
        _(context, 'I know'): lambda: handle_answer_question(update, context, code, interview_id),
    }

    try:
        if code in actions:
            await actions[code]()
        else:
            await show_onboarding(update, context, query)
    except Exception as e:
        print(f"Error handling button click: {e}")


async def handle_answer_question(update: Update, context: ContextTypes.DEFAULT_TYPE, code: str, interview_id) -> None:
    number_of_question = app_config['interview_question_repo'].get_number_of_question(interview_id=interview_id)
    questions_count = app_config['system_setting_repo'].get_interview_question_count()

    end_button_text = _(context, "View interview result")
    text = _(context, "Interview\n\n<b>❓Question {number_of_question}/{questions_count}:</b>\n\n").format(
        number_of_question=number_of_question,
        questions_count=questions_count
    )

    await get_answer_from_data(update, context, True if code == _(context, 'I know') else False, text, end_button_text, interview_id)


async def send_interview_completion_message(update: Update, context: ContextTypes.DEFAULT_TYPE, interview_id):
    reply_markup = await add_jump_button(_(context, "Finish the interview"))

    questions_count = app_config['system_setting_repo'].get_interview_question_count()
    count_of_correct_answers = app_config['interview_question_repo'].get_count_of_correct_answers(interview_id=interview_id)
    correct_answer_percentage = app_config['interview_question_repo'].get_correct_answer_percentage(
        interview_id=interview_id
    )

    app_config['interview_repo'].finish_interview(
        interview_id=interview_id
    )

    app_config['interview_statistics_repo'].save_statistics(
        interview_id=interview_id
    )

    await edit_message(
        chat_id=get_chat_id(update),
        message_id=update.callback_query.message.message_id,
        text=_(context, "You have finished the interview").format(
            percent=correct_answer_percentage,
            correct=count_of_correct_answers,
            questions_count=questions_count),
        reply_markup=reply_markup
    )
