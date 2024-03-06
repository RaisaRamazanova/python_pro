from Model.model import UserData, Level, Section, Interview, Theme
from telegram.ext import ContextTypes
from telegram import Update


def change_level(context, level: str):
    context.user_data['data'].common_data.level = level


def change_section(context, section: str):
    context.user_data['data'].common_data.section = section


def change_theme(context, theme: str):
    context.user_data['data'].common_data.theme = theme


def change_is_interview(context, is_interview: bool):
    context.user_data['data'].common_data.is_interview = is_interview


def change_user_language(context, user_language: str):
    context.user_data['data'].common_data.user_language = user_language


def change_stage(context, stage: int):
    context.user_data['stage'] = stage


def get_data(context: ContextTypes.DEFAULT_TYPE) -> UserData | None:
    if 'data' in context.user_data:
        return context.user_data['data']
    else:
        return None


def get_level_name(context: ContextTypes.DEFAULT_TYPE) -> str:
    data = get_data(context)
    if data is not None:
        return data.common_data.level
    return ""


def get_level_data(context: ContextTypes.DEFAULT_TYPE) -> Level | None:
    data = get_data(context)
    section = get_section_data(context)
    if data is not None:
        for level in section.levels:
            if level.name == data.common_data.level:
                return level
    return None


def get_interview_data(context: ContextTypes.DEFAULT_TYPE) -> Interview | None:
    data = get_data(context)
    if data is not None:
        return data.interview_data
    return None


def get_section_data(context: ContextTypes.DEFAULT_TYPE) -> Section | None:
    data = get_data(context)
    theme = get_theme(context)
    if data is not None:
        for s in theme.sections:
            if s.name == data.common_data.section:
                return s
    return None


def get_theme(context: ContextTypes.DEFAULT_TYPE) -> Theme | None:
    data = get_data(context)
    if data is not None:
        for theme in data.theme_data:
            if theme.name == data.common_data.theme:
                return theme
    return None


def get_chat_id(update: Update):
    return update.message.chat_id if update.message else update.callback_query.message.chat_id


def get_message_id(update: Update):
    return update.message.message_id if update.message else update.message.chat.id