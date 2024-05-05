from interactor import _
from screens_bulder import *
from payment import buy
from onboarding import return_to_previous_onboarding_step, start_onboarding, show_onboarding
from test_process import show_question_screen, show_four_answers_feedback, show_one_answer_feedback


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
        _(context, "Return to the main page ⬅️"): lambda: show_learn_topics_screen(update, context),
        _(context, "Finish training"): lambda: return_to_section_start_screen(update, context),
        _(context, "Finish the interview"): lambda: return_menu_screen(update, context, query),
        _(context, "Save progress and exit"): lambda: save_data_and_exit(update, context, interview_id),
        _(context, "View training result"): lambda: send_level_completion_message(update, context),
        _(context, "View interview result"): lambda: send_interview_completion_message(update, context, interview_id),
        'back to section screen': lambda: show_section_start_screen(update, context),
        'back to pay screen': lambda: return_to_pay_screen(update, context),
        'back': lambda: return_to_previous_onboarding_step(update, context, query),
        translations['en']['start']: lambda: start_onboarding(update, context, query),
        translations['ru']['start']: lambda: start_onboarding(update, context, query),
        _(context, "Learn topics 📚"): lambda: show_theme_screen(update, context),
        _(context, "Start the interview 🤺"): lambda: start_interview(update, context),
        _(context, "interview results"): lambda: show_interview_results_screen(update, context, interview_id),
        _(context, "Change interview topics 🔁"): lambda: start_onboarding(update, context, query),
        _(context, "Buy 💰"): lambda: buy(update, context),
        _(context, "Buy access 💰"): lambda: buy(update, context),
        _(context, 'Next question ➡️'): lambda: show_question_screen(update, context),
        "back to the main menu": lambda: show_main_screen(update, context, query),
        "back to the main menu and delete image": lambda: return_to_main_screen(update, context),
        _(context, "Return to the topics ⬅️"): lambda: show_theme_screen(update, context),
        _(context, "Programming languages"): lambda: change_theme_and_show_learn_topics_screen(update, context, code),
        _(context, "Frameworks"): lambda: change_theme_and_show_learn_topics_screen(update, context, code),
        _(context, "Tools"): lambda: change_theme_and_show_learn_topics_screen(update, context, code),
        _(context, "Theory"): lambda: change_theme_and_show_learn_topics_screen(update, context, code),
        _(context, 'I don\'t know'):lambda: handle_one_answer_question(update, context, code, interview_id),
        _(context, 'I know'): lambda: handle_one_answer_question(update, context, code, interview_id),
    }

    try:
        # if code.isdigit():
        #     await handle_training_process(update, context, int(code), interview_id)
        if code in actions:
            await actions[code]()
        else:
            await show_onboarding(update, context, query)
    except Exception as e:
        print(f"Error handling button click: {e}")


async def handle_one_answer_question(update: Update, context: ContextTypes.DEFAULT_TYPE, code: str, interview_id) -> None:
    number_of_question = app_config['interview_question_repo'].get_number_of_question(interview_id=interview_id)
    questions_count = app_config['system_setting_repo'].get_interview_question_count()

    if interview_id:
        end_button_text = _(context, "View interview result")
        text = _(context, "Interview\n\n<b>❓Question {number_of_question}/{questions_count}:</b>\n\n").format(
            number_of_question=number_of_question,
            questions_count=questions_count
        )
    else:
        end_button_text = _(context, "View training result")
        text = _(context, "Preparation for the interview for {name}").format(
            name="TEST",
            number_of_question=number_of_question,
            questions_count=questions_count
        )

    await show_one_answer_feedback(update, context, True if code == _(context, 'I know') else False, text, end_button_text, interview_id)


async def save_data_and_exit(update: Update, context: ContextTypes.DEFAULT_TYPE, interview_id):
    if interview_id:
        await show_main_screen(update, context, update.callback_query)
    else:
        await show_section_start_screen(update, context)


async def return_to_pay_screen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # section_data = get_section_data(context)
    # section_data.invoice_message_id = update.callback_query.message.message_id
    await show_pay_screen(update, context)


async def return_to_main_screen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # interview = get_interview_data(context)
    # interview.deleting_message_id = update.callback_query.message.message_id
    # await delete_message(
    #     chat_id=get_chat_id(update),
    #     message_id=interview.deleting_message_id
    # )
    await show_main_screen(update, context, update.callback_query)


async def change_level_and_ask_question(update: Update, context: ContextTypes.DEFAULT_TYPE, level: str):
    # change_level(context, level)
    await show_question_screen(update, context)


async def change_theme_and_show_learn_topics_screen(update: Update, context: ContextTypes.DEFAULT_TYPE, theme: str):
    # change_theme(context, theme)
    await show_learn_topics_screen(update, context)


async def change_level_and_pay(update: Update, context: ContextTypes.DEFAULT_TYPE, level: str):
    # change_level(context, level)
    await show_pay_screen(update, context)


async def return_to_section_start_screen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # get_level_data(context).variable_data.reset()
    await show_section_start_screen(update, context)


async def return_menu_screen(update: Update, context: ContextTypes.DEFAULT_TYPE, query):
    # get_interview_data(context).variable_data.reset()
    # for key in get_interview_data(context).selected_questions_by_topics:
    #     get_interview_data(context).selected_questions_by_topics[key] = 0
    #     get_interview_data(context).percent_of_correct_answers_by_topic[key] = 0
    await show_main_screen(update, context, query)


async def send_level_completion_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # level_data = get_level_data(context)
    # section_data = get_section_data(context)
    # percentage_correct = int((level_data.variable_data.number_of_correct * 100) / level_data.questions_count)
    reply_markup = await add_jump_button(_(context, "Finish training"))
    #
    # for i, level in enumerate(section_data.levels):
    #     if level.name == level_data.name and section_data.results[i] < percentage_correct:
    #         section_data.results[i] = percentage_correct
    #         break
    questions_count = app_config['system_setting_repo'].get_interview_question_count()

    await edit_message(
        chat_id=get_chat_id(update),
        message_id=update.callback_query.message.message_id,
        text=_(context, "You have finished the training on {theme}").format(
            theme="TEST",
            percent="TEST%",
            correct="TEST%",
            questions_count=questions_count),
        reply_markup=reply_markup
    )


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


# async def handle_training_process(update: Update, context: ContextTypes.DEFAULT_TYPE, selected_answer_index, interview_id):
#     number_of_question = app_config['interview_question_repo'].get_number_of_question(interview_id=interview_id)
#     questions_count = app_config['system_setting_repo'].get_interview_question_count()
#
#     if interview_id:
#         next_button_text = _(context, "View interview result")
#         text = _(context, "Interview\n\n<b>❓Question {number_of_question}/{questions_count}:</b>\n\n").format(
#             number_of_question=number_of_question,
#             questions_count=questions_count
#         )
#     else:
#         next_button_text = _(context, "View training result")
#         text = _(context, "Preparation for the interview for {name}").format(
#             name='TEST',
#             number_of_question=number_of_question,
#             questions_count=questions_count
#         )
#     await show_four_answers_feedback(update, context, selected_answer_index, text, next_button_text)
