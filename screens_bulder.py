from interactor import *
from telegram import CallbackQuery
from interactor import _


async def show_main_screen(context: ContextTypes.DEFAULT_TYPE, query: CallbackQuery):
    subcategory = ''
    for category in context.user_data['stage_2_selection']:
        subcategory += "\t\t⛳️ {category}\n".format(category=category)
    text = _(context, "Your personalized interview on\n\n {subcategory}\n is ready!\n\nTake it as many times as you want, <u>questions will change</u>\n\n").format(
        subcategory=subcategory
    )

    list_of_buttons = [_(context, "Start the interview 🤺"), _(context, "Change interview topics 🔁"), _(context, "Learn topics 📚"), _(context, "Buy access 💰")]
    keyboard_buttons = await create_buttons(list_of_buttons)
    reply_markup = InlineKeyboardMarkup(row_width=1)
    reply_markup.add(*keyboard_buttons)

    await query.edit_message_text(
        text=text,
        reply_markup=reply_markup.to_json(),
        parse_mode="HTML"
    )


async def show_theme_screen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['data'].common_data.is_interview = False
    data = get_data(context)

    list_of_buttons = []
    for theme in data.theme_data:
        list_of_buttons.append(theme.name)
    list_of_buttons.append(_(context, "To the main menu ⬅️"))
    keyboard_buttons = await create_buttons(list_of_buttons)
    reply_markup = InlineKeyboardMarkup(row_width=1)
    reply_markup.add(*keyboard_buttons)

    text = _(context, "Welcome to the training section 📚!\n\nHere you can learn and practice various topics, answering questions and solving problems.\n\nAfter each training session, we will collect statistics on your progress 📊, to help you become a better programmer.\n\n")

    try:
        if update.callback_query:
            await edit_message(
                chat_id=data.common_data.chat_id,
                message_id=update.callback_query.message.message_id,
                reply_markup=reply_markup,
                text=text)
        else:
            await update.message.reply_text(text, reply_markup=reply_markup.to_json(), parse_mode='HTML')
    except Exception as e:
        print(f"Ошибка: {e}")


async def show_learn_topics_screen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['data'].common_data.is_interview = False
    data = get_data(context)

    short_name_buttons = []
    long_name_buttons = []
    theme = get_theme(context)

    for section in theme.sections:
        button = InlineKeyboardButton(section.name, callback_data=section.name)
        if len(section.name) <= 15:
            short_name_buttons.append(button)
        else:
            long_name_buttons.append([button])

    back_button = InlineKeyboardButton(_(context, "Return to the topics ⬅️"), callback_data=_(context, "Return to the topics ⬅️"))
    long_name_buttons.append([back_button])

    keyboard_buttons = []
    for i in range(0, len(short_name_buttons), 2):
        row = short_name_buttons[i:i+2]
        keyboard_buttons.append(row)
    keyboard_buttons.extend(long_name_buttons)

    reply_markup = InlineKeyboardMarkup(keyboard_buttons)

    text = _(context, "Choose the topic you want to study")

    try:
        if update.callback_query:
            await context.bot.edit_message_text(
                chat_id=data.common_data.chat_id,
                message_id=update.callback_query.message.message_id,
                text=text,
                reply_markup=reply_markup.to_json())
        else:
            await update.message.reply_text(text, reply_markup=reply_markup.to_json())
    except Exception as e:
        print(f"Ошибка: {e}")


async def show_section_start_screen(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    section = get_section_data(context)
    data = get_data(context)

    if section.code[0][0] == '3':
        dict_of_buttons = {f"{section.name}_Junior": _(context, 'start_tool')}
    else:
        dict_of_buttons = {
            f"{section.name}_{level.name}": level.name if level.is_paid else f"{level.name} 🔒"
            for level in section.levels
        }
    dict_of_buttons[_(context, "Return to the main page ⬅️")] = _(context, "Return to the main page ⬅️")
    keyboard_buttons = await create_buttons(dict_of_buttons)
    reply_markup = InlineKeyboardMarkup(row_width=1)
    reply_markup.add(*keyboard_buttons)

    if section.code[0][0] == '3':
        results_texts = [_(context, "🏆 {level}: {result}% correct\n\n").format(level=section.name, result=section.results[0])] if section.results[0] > 0 else []
    else:
        results_texts = [
            _(context, "🏆 {level}: {result}% correct\n\n").format(level=level.name, result=result)
            for level, result in zip(section.levels, section.results) if result > 0
        ]

    if results_texts:
        record_text = _(context, "<b>Your best past results:</b>\n") + "\n\n".join(results_texts)
    else:
        record_text = ""

    if section.code[0][0] == '3':
        text_parts = [_(context, "Here you can train ") + section.name, record_text, '\n\n\n']
    else:
        text_parts = [
            _(context, "Here you can train ") + section.name,
            record_text,
            _(context, "Choose the level you will be studying\n\n\n")
        ]
    text = "\n\n".join(part for part in text_parts if part)

    try:
        if update.callback_query:
            await edit_message(
                chat_id=data.common_data.chat_id,
                message_id=update.callback_query.message.message_id,
                reply_markup=reply_markup,
                text=text)
        else:
            await update.message.reply_text(text, reply_markup=reply_markup.to_json(), parse_mode='HTML')
    except Exception as e:
        print(f"Ошибка: {e}")


async def show_pay_screen(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    list_of_buttons = [_(context, "Buy 💰"), _(context, "Back ⬅️")]
    keyboard_buttons = await create_buttons(list_of_buttons)
    reply_markup = InlineKeyboardMarkup(row_width=1)
    reply_markup.add(*keyboard_buttons)

    text = _(context, "This is a paid level. It is currently locked 🔒\n\n<b>You can buy it 💰</b>")

    try:
        await edit_message(
            chat_id=get_data(context).common_data.chat_id,
            message_id=update.callback_query.message.message_id,
            text=text,
            reply_markup=reply_markup)
    except Exception as e:
        invoice_message_id = get_section_data(context).invoice_message_id
        if invoice_message_id:
            try:
                await delete_message(
                    chat_id=get_data(context).common_data.chat_id,
                    message_id=invoice_message_id)
            except Exception as e:
                print(f"Не удалось удалить сообщение: {e}")

            await send_message(
                chat_id=get_data(context).common_data.chat_id,
                text=text,
                reply_markup=reply_markup)
