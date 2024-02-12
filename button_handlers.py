from interactor import _
from screens_bulder import *
from payment import buy
from onboarding import show_onboarding, return_to_previous_onboarding_step, restart_onboarding, create_themes
from test_process import show_question_screen, show_answer_feedback


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    code = query.data

    actions = {
        _(context, "Return to the main page ⬅️"): lambda: show_learn_topics_screen(update, context),
        _(context, "Finish training"): lambda: return_to_section_start_screen(update, context),
        _(context, "Finish the interview"): lambda: return_menu_screen(context, query),
        _(context, "Save progress and exit"): lambda: save_data_and_exit(update, context),
        _(context, "View training result"): lambda: send_level_completion_message(update, context),
        _(context, "View interview result"): lambda: send_interview_completion_message(update, context),
        _(context, "Back ⬅️"): lambda: show_section_start_screen(update, context),
        _(context, "Back ⬅️ 1"): lambda: return_to_pay_screen(update, context),
        'back': lambda: return_to_previous_onboarding_step(update, context),
        translations['en']['start']: lambda: change_language_and_show_onboarding(context, query, 'en'),
        translations['ru']['start']: lambda: change_language_and_show_onboarding(context, query, 'ru'),
        # 'start': lambda: show_menu_screen(context, query),

        _(context, "Learn topics 📚"): lambda: show_theme_screen(update, context),
        _(context, "Start the interview 🤺"): lambda: start_interview(update, context),
        _(context, "Change interview topics 🔁"): lambda: restart_onboarding(context, query),
        _(context, "Buy 💰"): lambda: buy(update, context),
        _(context, "Buy access 💰"): lambda: buy(update, context),
        _(context, 'Next question ➡️'): lambda: show_question_screen(update, context),
        _(context, "To the main menu ⬅️"): lambda: show_main_screen(context, query),
        _(context, "Return to the topics ⬅️"): lambda: show_theme_screen(update, context),
        _(context, "Programming languages"): lambda: change_theme_and_show_learn_topics_screen(update, context, code),
        _(context, "Frameworks"): lambda: change_theme_and_show_learn_topics_screen(update, context, code),
        _(context, "Tools"): lambda: change_theme_and_show_learn_topics_screen(update, context, code),
        _(context, "Theory"): lambda: change_theme_and_show_learn_topics_screen(update, context, code),
    }

    try:
        if code.isdigit():
            await handle_numeric_code(update, context, code)
        elif code in actions:
            await actions[code]()
        else:
            await handle_non_numeric_code(update, context, code, query)
    except Exception as e:
        print(f"Error handling button click: {e}")


async def handle_numeric_code(update: Update, context: ContextTypes.DEFAULT_TYPE, code: str) -> None:
    int_code = int(code)
    if get_data(context).common_data.is_interview:
        data = get_interview_data(context)
    else:
        data = get_level_data(context)

    await handle_training_process(update, context, int_code, data)


async def handle_non_numeric_code(update: Update, context: ContextTypes.DEFAULT_TYPE, code: str,
                                  query: CallbackQuery) -> None:
    if context.user_data['stage'] < 7:
        await show_onboarding(context, query)
    else:
        if not context.user_data['data'].common_data.is_interview:
            theme = get_theme(context)
            for section in theme.sections:
                for level in section.levels:
                    if code == str(section.name):
                        context.user_data['data'].common_data.section = section.name
                        await show_section_start_screen(update, context)
                        break
                    if code == str(section.name) + '_' + str(level.name) and level.is_paid:
                        await change_level_and_ask_question(update, context, level.name)
                        break
                    if code == str(section.name) + '_' + str(level.name) and not level.is_paid:
                        await change_level_and_pay(update, context, level.name)
                        break
        else:
            await start_interview(update, context)


async def change_language_and_show_onboarding(context: ContextTypes.DEFAULT_TYPE, query: CallbackQuery, language: str):
    context.user_data['data'].common_data.user_language = language
    context.user_data['data'].update(create_themes(context))
    await show_onboarding(context, query)


async def save_data_and_exit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if get_data(context).common_data.is_interview:
        await show_main_screen(context, update.callback_query)
    else:
        await show_section_start_screen(update, context)


async def return_to_pay_screen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    section_data = get_section_data(context)
    section_data.invoice_message_id = update.callback_query.message.message_id
    await show_pay_screen(update, context)


async def change_level_and_ask_question(update: Update, context: ContextTypes.DEFAULT_TYPE, level: str):
    change_level(context, level)
    await show_question_screen(update, context)


async def change_theme_and_show_learn_topics_screen(update: Update, context: ContextTypes.DEFAULT_TYPE, theme: str):
    context.user_data['data'].common_data.theme = theme
    await show_learn_topics_screen(update, context)


async def change_level_and_pay(update: Update, context: ContextTypes.DEFAULT_TYPE, level: str):
    change_level(context, level)
    await show_pay_screen(update, context)


async def start_interview(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if get_data(context) is not None:
        get_data(context).common_data.is_interview = True
        await show_question_screen(update, context)


async def return_to_section_start_screen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    get_level_data(context).variable_data.reset()
    await show_section_start_screen(update, context)


async def return_menu_screen(context: ContextTypes.DEFAULT_TYPE, query):
    get_interview_data(context).variable_data.reset()
    for key in get_interview_data(context).selected_questions_by_topics:
        get_interview_data(context).selected_questions_by_topics[key] = 0
    await show_main_screen(context, query)


async def send_level_completion_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    level_data = get_level_data(context)
    section_data = get_section_data(context)
    percentage_correct = int((level_data.variable_data.number_of_correct * 100) / level_data.questions_count)
    reply_markup = await add_jump_button(_(context, "Finish training"))

    for i, level in enumerate(section_data.levels):
        if level.name == level_data.name and section_data.results[i] < percentage_correct:
            section_data.results[i] = percentage_correct
            break
    await edit_message(
        chat_id=get_data(context).common_data.chat_id,
        message_id=update.callback_query.message.message_id,
        text=_(context, "<b>You have finished the training on {theme}!</b>\n\nCorrectly completed {percent}% ({correct} out of {questions_count})").format(
            theme=section_data.name,
            percent=percentage_correct,
            correct=level_data.variable_data.number_of_correct,
            questions_count=level_data.questions_count),
        reply_markup=reply_markup
    )


async def send_interview_completion_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = get_interview_data(context)

    percentage_correct = int((data.variable_data.number_of_correct * 100) / data.questions_count)
    reply_markup = await add_jump_button(_(context, "Finish the interview"))

    if data.results < percentage_correct:
        data.results = percentage_correct

    await edit_message(
        chat_id=get_data(context).common_data.chat_id,
        message_id=update.callback_query.message.message_id,
        text=_(context, "<b>You have finished the interview!</b>\n\nCorrectly completed {percent}% ({correct} out of {questions_count})").format(
            percent=percentage_correct,
            correct=data.variable_data.number_of_correct,
            questions_count=data.questions_count),
        reply_markup=reply_markup
    )


async def handle_training_process(update: Update, context: ContextTypes.DEFAULT_TYPE, selected_answer_index, data):
    if get_data(context).common_data.is_interview:
        next_button_text = _(context, "View interview result")
        text = _(context, "Interview\n\n<b>❓Question {number_of_question}/{questions_count}:</b>\n\n").format(
            number_of_question=data.variable_data.number_of_question,
            questions_count=data.questions_count
        )
    else:
        next_button_text = _(context, "View training result")
        text = _(context, "Preparation for the interview for {name}\n\n<b>❓Question {number_of_question}/{questions_count}:</b>\n\n").format(
            name=data.name,
            number_of_question=data.variable_data.number_of_question,
            questions_count=data.questions_count
        )
    await show_answer_feedback(update, context, selected_answer_index, data, text, next_button_text)
