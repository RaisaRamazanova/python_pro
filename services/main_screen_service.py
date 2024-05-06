from handlers.interactor import *
from telegram import CallbackQuery, Update
from handlers.interactor import _
from services.onboarding_service import app_config


async def show(update: Update, context: ContextTypes.DEFAULT_TYPE, query: CallbackQuery = None):
    user_id = app_config['user_repo'].get_user_id(telegram_id=update.effective_user.id)
    user_onboarding_id = app_config['onboarding_repo'].get_user_onboarding_id(user_id=user_id)
    categories = app_config['onboarding_stage_option_repo'].get_user_selected_option_names(
        user_id=user_id,
        user_onboarding_id=user_onboarding_id,
        chat_id=get_chat_id(update)
    )

    subcategories_text = "\n".join(["\t\t⛳️ {category}".format(category=category) for category in categories])

    text = _(context, "Your personalized interview on").format(subcategory=subcategories_text)

    button_texts = [_(context, "Start the interview 🤺"), _(context, "Change interview topics 🔁"), _(context, "Buy access 💰")]
    keyboard_buttons = await create_buttons(button_texts)

    reply_markup = InlineKeyboardMarkup(row_width=1).add(*keyboard_buttons)

    try:
        await query.edit_message_text(text=text, reply_markup=reply_markup.to_json(), parse_mode="HTML")
    except Exception as e:
        print(f"Error updating message: {e}")
        await send_message(chat_id=get_chat_id(update), text=text, reply_markup=reply_markup)
