from data import translations
from interactor import *
from screens_bulder import show_main_screen
from user_state import *
from telegram import CallbackQuery
from interactor import _
from repository.database import create_app_config
from data.globals import db_config


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global app_config
    app_config = create_app_config(db_config)

    app_config['user_repo'].create(
        telegram_id=update.effective_user.id,
        telegram_username=update.effective_user.username,
        first_name=update.effective_user.first_name,
        last_name=update.effective_user.last_name,
        language_id=1,
        telegram_chat_id=update.message.chat.id,
        is_banned=False
    )

    language = app_config['user_repo'].get_language(update.message.chat.id)

    if language == 1:
        welcome_text = translations['ru']['welcome_message']
    else:
        welcome_text = translations['en']['welcome_message']
    buttons = [
        InlineKeyboardButton(translations['en']['start'], callback_data=translations['en']['start']),
        InlineKeyboardButton(translations['ru']['start'], callback_data=translations['ru']['start'])
    ]

    reply_markup = InlineKeyboardMarkup([[button for button in buttons]]).to_json()


    await context.bot.send_message(chat_id=update.effective_chat.id, text=welcome_text, reply_markup=reply_markup,
                                   parse_mode='HTML')


async def start_onboarding(update: Update, context: ContextTypes.DEFAULT_TYPE, query: CallbackQuery):
    user_id = app_config['user_repo'].get_user_id(telegram_id=update.effective_user.id)
    first_stage_id = app_config['stage_repo'].get_stage_by_index(index=1)

    app_config['onboarding_repo'].start_onboarding(user_id=user_id, chat_id=update.callback_query.message.chat.id)
    user_onboarding_id = app_config['onboarding_repo'].get_user_onboarding_id(user_id=user_id)

    app_config['onboarding_stage_repo'].start_onboarding_stage(
        user_id=user_id,
        chat_id=update.callback_query.message.chat.id,
        user_onboarding_id=user_onboarding_id,
        stage_id=first_stage_id)

    await show_onboarding(update, context, query)


async def show_onboarding(update: Update, context: ContextTypes.DEFAULT_TYPE, query: CallbackQuery):
    user_id = app_config['user_repo'].get_user_id(telegram_id=update.effective_user.id)
    user_onboarding_id = app_config['onboarding_repo'].get_user_onboarding_id(user_id=user_id)
    user_onboarding_stage_id = app_config['onboarding_stage_repo'].get_latest_onboarding_stage_id(
        user_id=user_id,
        user_onboarding_id=user_onboarding_id
    )
    language_id = app_config['user_repo'].get_language(chat_id=update.callback_query.message.chat.id)
    current_stage = app_config['onboarding_stage_repo'].get_latest_onboarding_stage_details(user_id=user_id)
    stage_translate = app_config['stage_repo'].get_stage_translate(
        stage_id=current_stage['id'],
        language_id=language_id)

    if query.data == 'confirm':
        if current_stage['is_required'] and not app_config['onboarding_stage_option_repo'].has_stage_option(
                user_id=user_id,
                user_onboarding_id=user_onboarding_id,
                user_onboarding_stage_id=user_onboarding_stage_id):
            return

        next_onboarding_stage = app_config['onboarding_stage_repo'].start_next_onboarding_stage(
            user_id=user_id,
            chat_id=update.callback_query.message.chat.id,
            user_onboarding_id=user_onboarding_id
        )

        if next_onboarding_stage:
            current_stage = app_config['onboarding_stage_repo'].get_latest_onboarding_stage_details(user_id=user_id)
            stage_translate = app_config['stage_repo'].get_stage_translate(
                stage_id=current_stage['id'],
                language_id=language_id)
            await show_onboarding_page(update, context, query, stage_translate, current_stage)
        else:
            app_config['onboarding_repo'].finish_onboarding(
                user_id=user_id,
                chat_id=update.callback_query.message.chat.id
            )
            await show_main_screen(context, query)

    elif query.data == "back" or query.data == translations['en']['start'] or query.data == translations['ru'][
        'start'] or query.data == _(context, "Change interview topics 🔁"):
        await show_onboarding_page(update, context, query, stage_translate, current_stage)
    else:
        stage_option_id = app_config['stage_option_repo'].get_stage_option_id_by_name(
            option_name=query.data
        )
        app_config['onboarding_stage_option_repo'].toggle_stage_option(
            user_id=user_id,
            chat_id=update.callback_query.message.chat.id,
            user_onboarding_id=user_onboarding_id,
            user_onboarding_stage_id=user_onboarding_stage_id,
            stage_id=current_stage['id'],
            stage_option_id=stage_option_id
        )
        await show_onboarding_page(update, context, query, stage_translate, current_stage)


async def show_onboarding_page(update: Update, context: ContextTypes.DEFAULT_TYPE, query: CallbackQuery, stage_description, current_stage):
    stage_options = app_config['stage_option_repo'].get_stage_option_by_stage_id(
        stage_id=current_stage['id']
    )

    user_id = app_config['user_repo'].get_user_id(telegram_id=update.effective_user.id)
    user_onboarding_id = app_config['onboarding_repo'].get_user_onboarding_id(user_id=user_id)
    child_stage_options = app_config['stage_option_repo'].get_next_stage_options(
        user_id=user_id,
        user_onboarding_id=user_onboarding_id,
        current_stage_id=current_stage['id']
    )

    print(child_stage_options)

    reply_markup = generate_keyboard(update, context, current_stage, stage_options, 'Дальше')
    await query.edit_message_text(text=stage_description, reply_markup=reply_markup.to_json())


def update_user_selection(context, data):
    selected_stage_key = f'stage_{context.user_data["stage"]}_selection'
    if data in context.user_data[selected_stage_key]:
        context.user_data[selected_stage_key].remove(data)
    else:
        context.user_data[selected_stage_key].append(data)


async def return_to_previous_onboarding_step(update: Update, context: ContextTypes.DEFAULT_TYPE):
    selected_stage_key = f'stage_{context.user_data['stage']}_selection'
    context.user_data[selected_stage_key] = []
    context.user_data['stage'] = context.user_data['stage'] - 1
    query = update.callback_query

    await show_onboarding(update, context, query)


def generate_keyboard(update: Update, context, current_stage, stage_options, confirm_text):
    keyboard = []

    user_id = app_config['user_repo'].get_user_id(telegram_id=update.effective_user.id)
    user_onboarding_id = app_config['onboarding_repo'].get_user_onboarding_id(user_id=user_id)
    for option in stage_options:
        is_selected = app_config['onboarding_stage_option_repo'].check_user_has_stage_option(
            user_id=user_id,
            stage_option_id=option['id'],
            user_onboarding_id=user_onboarding_id
        )
        text = f"{'✅ ' if is_selected else ''}{option['name']}"
        keyboard.append([InlineKeyboardButton(text, callback_data=option['name'])])

    keyboard.append([InlineKeyboardButton(confirm_text, callback_data='confirm')])
    if current_stage['index'] > 1:
        keyboard.append([InlineKeyboardButton(_(context, "Back ⬅️"), callback_data='back')])

    return InlineKeyboardMarkup(keyboard)
