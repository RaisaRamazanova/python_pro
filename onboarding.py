from data import translations
from interactor import *
import screens_bulder
from telegram import CallbackQuery
from interactor import _
from repository.database import create_app_config
from data.globals import db_config


app_config = create_app_config(db_config)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print('start')
    app_config['user_repo'].create(
        telegram_id=update.effective_user.id,
        telegram_username=update.effective_user.username,
        first_name=update.effective_user.first_name,
        last_name=update.effective_user.last_name,
        language_id=1,
        telegram_chat_id=update.message.chat.id,
        is_banned=False
    )

    language = app_config['user_repo'].get_user_language_code(get_chat_id(update))
    welcome_text = translations[language]['welcome_message']
    buttons = [
        InlineKeyboardButton(translations['en']['start'], callback_data=translations['en']['start']),
        InlineKeyboardButton(translations['ru']['start'], callback_data=translations['ru']['start'])
    ]

    reply_markup = InlineKeyboardMarkup([[button for button in buttons]]).to_json()

    await context.bot.send_message(chat_id=get_chat_id(update), text=welcome_text, reply_markup=reply_markup,
                                   parse_mode='HTML')


async def start_onboarding(update: Update, context: ContextTypes.DEFAULT_TYPE, query: CallbackQuery):
    user_id = app_config['user_repo'].get_user_id(telegram_id=update.effective_user.id)
    first_stage_id = app_config['stage_repo'].get_stage_by_index(index=1)

    app_config['onboarding_repo'].finish_last_onboarding(
        user_id=user_id,
        chat_id=get_chat_id(update)
    )

    app_config['onboarding_repo'].start_onboarding(user_id=user_id, chat_id=update.callback_query.message.chat.id)
    user_onboarding_id = app_config['onboarding_repo'].get_user_onboarding_id(user_id=user_id)

    app_config['onboarding_stage_repo'].start_onboarding_stage(
        user_id=user_id,
        chat_id=get_chat_id(update),
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
    language_id = app_config['user_repo'].get_language_id(chat_id=update.callback_query.message.chat.id)
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
            chat_id=get_chat_id(update),
            user_onboarding_id=user_onboarding_id
        )

        if next_onboarding_stage:
            current_stage = app_config['onboarding_stage_repo'].get_latest_onboarding_stage_details(user_id=user_id)
            stage_translate = app_config['stage_repo'].get_stage_translate(
                stage_id=current_stage['id'],
                language_id=language_id)
            await show_onboarding_page(update, context, query, user_id, user_onboarding_id, stage_translate, current_stage)
        else:
            app_config['onboarding_repo'].finish_onboarding(
                user_id=user_id,
                chat_id=get_chat_id(update)
            )
            app_config['user_level_repo'].record_user_levels(user_id=user_id)
            await screens_bulder.show_main_screen(update, context, query)
    else:
        stage_option_id = app_config['stage_option_repo'].get_stage_option_id_by_name(
            option_name=query.data
        )
        app_config['onboarding_stage_option_repo'].toggle_stage_option(
            user_id=user_id,
            chat_id=get_chat_id(update),
            user_onboarding_id=user_onboarding_id,
            user_onboarding_stage_id=user_onboarding_stage_id,
            stage_id=current_stage['id'],
            stage_option_id=stage_option_id
        )
        await show_onboarding_page(update, context, query, user_id, user_onboarding_id, stage_translate, current_stage)


async def show_onboarding_page(update: Update, context: ContextTypes.DEFAULT_TYPE, query: CallbackQuery, user_id, user_onboarding_id, stage_description, current_stage):
    stage_options = app_config['stage_option_repo'].get_dependent_stage_options(
        user_id=user_id,
        user_onboarding_id=user_onboarding_id,
        target_stage_id=current_stage['id']
    )

    reply_markup = generate_keyboard(update, context, current_stage, stage_options, 'Дальше')

    await query.edit_message_text(text=stage_description, reply_markup=reply_markup.to_json())


async def return_to_previous_onboarding_step(update: Update, context: ContextTypes.DEFAULT_TYPE, query: CallbackQuery):
    user_id = app_config['user_repo'].get_user_id(telegram_id=update.effective_user.id)
    user_onboarding_id = app_config['onboarding_repo'].get_user_onboarding_id(user_id=user_id)

    app_config['onboarding_stage_repo'].return_to_previous_onboarding_step(
        user_id=user_id,
        user_onboarding_id=user_onboarding_id
    )

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
