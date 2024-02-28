from typing import List
from data import translations
from interactor import *
from telegram import CallbackQuery
from data.globals import STAGE_MAPPING_LEVELS, types_of_topics
from interactor import _
from screens_bulder import show_main_screen
from model import CommonData, Interview, VariableData, Theme
import json


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_lang = update.effective_user.language_code

    if user_lang.startswith('ru'):
        welcome_text = translations['ru']['welcome_message']
    else:
        welcome_text = translations['en']['welcome_message']
    buttons = [
        InlineKeyboardButton(translations['en']['start'], callback_data=translations['en']['start']),
        InlineKeyboardButton(translations['ru']['start'], callback_data=translations['ru']['start'])
    ]

    reply_markup = InlineKeyboardMarkup([[button for button in buttons]]).to_json()

    initialize_states(update, context)

    await context.bot.send_message(chat_id=update.effective_chat.id, text=welcome_text, reply_markup=reply_markup,
                                   parse_mode='HTML')


def initialize_states(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global STAGE_MAPPING
    STAGE_MAPPING = get_stage_mapping_data()

    context.user_data['unique_codes'] = {}
    context.user_data['code_value'] = 100
    for key in ['stage_1_selection', 'stage_2_selection', 'stage_3_selection', 'stage_4_selection', 'stage_5_selection',
                'stage_6_selection']:
        context.user_data[key] = []
    context.user_data['stage'] = 1
    context.user_data['data'] = UserData(
        interview_data=Interview(
            topics=[],
            results=[],
            questions_count=10,
            variable_data=VariableData(),
            number_of_questions_by_topic={},
            selected_questions_by_topics={},
            number_of_correct_answers_by_topic={}
        ),
        common_data=CommonData(
            chat_id=get_chat_id(update)
        )
    )

    # assign_codes(context, STAGE_MAPPING)


def create_themes(context: ContextTypes.DEFAULT_TYPE) -> List[Theme]:
    codes_1 = []
    codes_2 = []
    codes_3 = []
    codes_4 = []

    with open('/Users/raisatramazanova/development/python_bot/python_pro_bot/data/unique_codes.txt', 'r') as file:
        for line in file:
            key, value = line.strip().split(' - ')
            if is_key_in_stage_mapping(key, STAGE_MAPPING):
                first_char = str(value)[0]
                if first_char == '1':
                    codes_1.append(Section(
                        name=key,
                        code=value,
                        results=[0, 0, 0],
                        levels=[
                            Level(
                                name='Junior',
                                code=1,
                                is_paid=True,
                                questions_count=10,
                                variable_data=VariableData()
                            ),
                            Level(
                                name='Middle',
                                code=2,
                                is_paid=False,
                                questions_count=10,
                                variable_data=VariableData(),
                                price=29900
                            ),
                            Level(
                                name='Senior',
                                code=3,
                                is_paid=False,
                                questions_count=10,
                                variable_data=VariableData(),
                                price=29900
                            )
                        ]
                    ))
                elif first_char == '2':
                    codes_2.append(Section(
                        name=key,
                        code=value,
                        results=[0, 0, 0],
                        levels=[
                            Level(
                                name='Junior',
                                code=1,
                                is_paid=True,
                                questions_count=10,
                                variable_data=VariableData()
                            ),
                            Level(
                                name='Middle',
                                code=2,
                                is_paid=False,
                                questions_count=10,
                                variable_data=VariableData(),
                                price=29900
                            ),
                            Level(
                                name='Senior',
                                code=3,
                                is_paid=False,
                                questions_count=10,
                                variable_data=VariableData(),
                                price=29900
                            )
                        ]
                    ))
                elif first_char == '4':
                    codes_4.append(Section(
                        name=key,
                        code=value,
                        results=[0, 0, 0],
                        levels=[
                            Level(
                                name='Junior',
                                code=1,
                                is_paid=True,
                                questions_count=10,
                                variable_data=VariableData()
                            ),
                            Level(
                                name='Middle',
                                code=2,
                                is_paid=False,
                                questions_count=10,
                                variable_data=VariableData(),
                                price=29900
                            ),
                            Level(
                                name='Senior',
                                code=3,
                                is_paid=False,
                                questions_count=10,
                                variable_data=VariableData(),
                                price=29900
                            )
                        ]
                    ))
                else:
                    codes_3.append(Section(
                        name=key,
                        code=value,
                        results=[0],
                        levels=[
                            Level(
                                name='Junior',
                                code=1,
                                is_paid=True,
                                questions_count=10,
                                variable_data=VariableData()
                            )
                        ]
                    ))

            context.user_data['unique_codes'][key] = int(value)

            theme_1 = Theme(
                name=_(context, "Programming languages"),
                sections=codes_1
            )
            theme_2 = Theme(
                name=_(context, "Frameworks"),
                sections=codes_2
            )
            theme_3 = Theme(
                name=_(context, "Tools"),
                sections=codes_3
            )
            theme_4 = Theme(
                name=_(context, "Theory"),
                sections=codes_4
            )
        themes = []
        for theme in [theme_1, theme_2, theme_3, theme_4]:
            if theme.sections:
                themes.append(theme)

        return themes


def is_key_in_stage_mapping(key, stage_mapping):
    for section in stage_mapping.values():
        if key in section["options"]:
            return True

        for category in section["next"].values():
            if key in category.get("languages", []) or \
                    key in category.get("frameworks", []) or \
                    key in category.get("tools", []):
                return True
    return False


def assign_codes(context: ContextTypes.DEFAULT_TYPE, data, type=None):
    if isinstance(data, dict):
        for key, value in data.items():
            new_path = str(key)
            if not isinstance(value, (dict, list)):
                context.user_data['unique_codes'][new_path] = context.user_data['code_value']
                context.user_data['code_value'] += 1
            else:
                if new_path in types_of_topics:
                    assign_codes(context, value, types_of_topics[new_path])
                else:
                    assign_codes(context, value)
    elif isinstance(data, list):
        for item in data:
            new_path = str(item)
            if new_path not in context.user_data['unique_codes']:
                if type is not None:
                    if type == 3:
                        context.user_data['unique_codes'][new_path] = type * 10000 + context.user_data[
                            'code_value'] * 10 + 1
                    else:
                        context.user_data['unique_codes'][new_path] = type * 1000 + context.user_data['code_value']
                else:
                    context.user_data['unique_codes'][new_path] = context.user_data['code_value']
                context.user_data['code_value'] += 1

    file_path = '/Users/raisatramazanova/development/python_bot/python_pro_bot/data/unique_codes.txt'

    with open(file_path, 'w') as file:
        for key, value in context.user_data['unique_codes'].items():
            file.write(f'{key} - {value}\n')
        file.close()


def select_uniformly(lst, num_selections):
    count = {element: 0 for element in lst}
    selections = []

    for _ in range(num_selections):
        lst.sort(key=lambda x: count[x])
        choice = random.choice(lst[:len(lst) // 2 + 1])
        selections.append(choice)
        count[choice] += 1

    return selections


async def show_onboarding(context: ContextTypes.DEFAULT_TYPE, query: CallbackQuery):
    data = query.data
    stage_texts = {
        1: (_(context, "Choose the domains"), _(context, "To subcategories ➡️")),
        2: (_(context, "Choose the subcategories"), _(context, "To programming languages ➡️")),
        3: (_(context, "Choose programming languages"), _(context, "To frameworks ➡️")),
        4: (_(context, "Choose frameworks"), _(context, "To tools ➡️")),
        5: (_(context, "Choose tools"), _(context, "To levels ➡️")),
        6: (_(context, "Choose levels"), _(context, "Finish ➡️")),
    }

    if data == 'confirm':
        if (context.user_data['stage'] == 1 and context.user_data['stage_1_selection'] == []) or (
                context.user_data['stage'] == 2 and context.user_data['stage_2_selection'] == []) or (
                context.user_data['stage'] == 6 and context.user_data['stage_6_selection'] == []):
            return
        context.user_data['stage'] += 1
        next_stage = context.user_data['stage']
        context.user_data['stage'] = next_stage

        if next_stage <= 6:
            text, confirm_button_text = stage_texts[next_stage]
            reply_markup = generate_keyboard(context, [], confirm_button_text)
            await query.edit_message_text(text=text, reply_markup=reply_markup.to_json())
        elif next_stage == 7:
            interview_themes = []
            for stage in ['stage_2_selection', 'stage_3_selection', 'stage_4_selection', 'stage_5_selection']:
                for subject in context.user_data[stage]:
                    if context.user_data['stage_6_selection']:
                        for level in context.user_data['stage_6_selection']:
                            if len(str(context.user_data['unique_codes'][subject])) == 4:
                                interview_themes.append(
                                    int(str(context.user_data['unique_codes'][subject]) + (
                                        '1' if level == 'Junior' else '2' if level == 'Middle' else '3'))
                                )
                            else:
                                interview_themes.append(context.user_data['unique_codes'][subject])
                    else:
                        for level in ['Junior', 'Middle', 'Senior']:
                            interview_themes.append(
                                str(context.user_data['unique_codes'][subject]) + (
                                    '1' if level == 'Junior' else '2' if level == 'Middle' else '3')
                            )
            uniform_selections = select_uniformly(interview_themes, get_interview_data(context).questions_count)
            get_interview_data(context).number_of_questions_by_topic = {x: uniform_selections.count(x) for x in
                                                                        interview_themes}
            get_interview_data(context).selected_questions_by_topics = {x: 0 for x in interview_themes}
            get_interview_data(context).percent_of_correct_answers_by_topic = {x: 0 for x in interview_themes}
            for category in context.user_data['stage_2_selection']:
                context.user_data['data'].interview_data.topics.append(category)

            await show_main_screen(context, query)
    elif data == "back" or data == translations['en']['start'] or data == translations['ru'][
        'start'] or data == _(context, "Change interview topics 🔁"):
        await show_onboarding_page(context, query, stage_texts)
    else:
        update_user_selection(context, data)
        await show_onboarding_page(context, query, stage_texts)


async def restart_onboarding(context: ContextTypes.DEFAULT_TYPE, query: CallbackQuery):
    for key in ['stage_1_selection', 'stage_2_selection', 'stage_3_selection', 'stage_4_selection', 'stage_5_selection',
                'stage_6_selection', 'interview']:
        context.user_data[key] = []
    context.user_data['stage'] = 1
    await show_onboarding(context, query)


async def show_onboarding_page(context: ContextTypes.DEFAULT_TYPE, query: CallbackQuery, stage_texts):
    if context.user_data['stage'] in stage_texts:
        text, confirm_button_text = stage_texts[context.user_data['stage']]
        selected_stage_key = f'stage_{context.user_data["stage"]}_selection'
        reply_markup = generate_keyboard(context, context.user_data[selected_stage_key], confirm_button_text)
        await query.edit_message_text(text=text, reply_markup=reply_markup.to_json())


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

    await show_onboarding(context, query)


def generate_keyboard(context, selected_options, confirm_text):
    keyboard = []
    stage = context.user_data['stage']
    options_key = 'options' if stage == 1 or stage == 2 else 'next'
    if stage == 1:
        options = list(STAGE_MAPPING.keys())
    else:
        selected_stage_key = f'stage_{stage - 1}_selection'
        previous_selection = context.user_data[selected_stage_key]
        options = set()
        for selected in previous_selection:
            if stage == 2:
                options.update(STAGE_MAPPING[selected].get(options_key, []))
        for option in context.user_data['stage_1_selection']:
            for category in STAGE_MAPPING[option]['next']:
                if category in context.user_data["stage_2_selection"] and 2 < stage < 6:
                    key = 'languages' if stage == 3 else 'frameworks' if stage == 4 else 'tools'
                    options.update(STAGE_MAPPING[option][options_key][category].get(key, []))
                if stage == 6:
                    options.update(STAGE_MAPPING_LEVELS)

    options = sorted(list(options))

    for option in options:
        text = f"{'✅ ' if option in selected_options else ''}{option}"
        keyboard.append([InlineKeyboardButton(text, callback_data=option)])

    keyboard.append([InlineKeyboardButton(confirm_text, callback_data='confirm')])
    if stage > 1:
        keyboard.append([InlineKeyboardButton(_(context, "Back ⬅️"), callback_data='back')])

    return InlineKeyboardMarkup(keyboard)


def get_stage_mapping_data() -> dict:
    file_path = '/Users/raisatramazanova/development/python_bot/python_pro_bot/data/stage_mapping.json'
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    file.close()
    return data
