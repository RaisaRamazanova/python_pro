from typing import List


class VariableData:
    def __init__(self, number_of_correct: int = 0, number_of_incorrect: int = 0, correct_answer_index: int = 0,
                 selected_id_list: List[int] = None, question: str = '', list_of_answers: List[str] = None,
                 explanation: str = '', number_of_question: int = 1, explanation_code: str = '', question_id: int = 0):
        self.number_of_correct = number_of_correct
        self.number_of_incorrect = number_of_incorrect
        self.correct_answer_index = correct_answer_index
        self.selected_id_list = selected_id_list if selected_id_list is not None else []
        self.question = question
        self.list_of_answers = list_of_answers if list_of_answers is not None else []
        self.explanation = explanation
        self.number_of_question = number_of_question
        self.explanation_code = explanation_code
        self.question_id = question_id

    def reset(self):
        self.number_of_correct = 0
        self.number_of_incorrect = 0
        self.correct_answer_index = 0
        self.selected_id_list = []
        self.question = ''
        self.list_of_answers = []
        self.explanation = ''
        self.number_of_question = 1
        self.explanation_code = ''
        self.question_id = 0

    def update(self,  question: str, list_of_answers: List[str], explanation: str, explanation_code: str, correct_answer_index: int, question_id: int):
        self.correct_answer_index = correct_answer_index
        self.question = question
        self.list_of_answers = list_of_answers
        self.explanation = explanation
        self.explanation_code = explanation_code
        self.question_id = question_id

    def to_dict(self):
        return {
            'number_of_correct': self.number_of_correct,
            'number_of_incorrect': self.number_of_incorrect,
            'correct_answer_index': self.correct_answer_index,
            'selected_id_list': self.selected_id_list,
            'question': self.question,
            'list_of_answers': self.list_of_answers,
            'explanation': self.explanation,
            'number_of_question': self.number_of_question,
            'explanation_code': self.explanation_code,
            'question_id': self.question_id
        }


class Level:
    def __init__(self, name: str, code: int, is_paid: bool, questions_count: int, variable_data: VariableData,
                 price: int = None):
        self.name = name
        self.code = code,
        self.is_paid = is_paid
        self.price = price
        self.questions_count = questions_count
        self.variable_data = variable_data

    def to_dict(self):
        return {
            'name': self.name,
            'code': self.code,
            'is_paid': self.is_paid,
            'price': self.price,
            'questions_count': self.questions_count,
            'variable_data': self.variable_data.to_dict()
        }


class Section:
    def __init__(self, name: str, code: int, levels: List[Level], results: List[int] = None,
                 invoice_message_id: int = 0):
        self.name = name
        self.code = code,
        self.levels = levels
        self.results = results
        self.invoice_message_id = invoice_message_id

    def to_dict(self):
        return {
            'name': self.name,
            'code': self.code,
            'levels': [level.to_dict() for level in self.levels],
            'results': self.results,
            'invoice_message_id': self.invoice_message_id
        }


class Theme:
    def __init__(self, name: str, sections: List[Section]):
        self.name = name
        self.sections = sections

    def to_dict(self):
        return {
            'name': self.name,
            'sections': [section.to_dict() for section in self.sections]
        }


class Interview:
    def __init__(self, topics: [str], questions_count: int, variable_data: VariableData, number_of_questions_by_topic: dict,
                 selected_questions_by_topics: dict, number_of_correct_answers_by_topic: dict, results: List[int] = None,
                 invoice_message_id: int = 0):
        self.topics = topics
        self.results = results
        self.deleting_message_id = invoice_message_id
        self.questions_count = questions_count
        self.variable_data = variable_data
        self.number_of_questions_by_topic = number_of_questions_by_topic
        self.selected_questions_by_topics = selected_questions_by_topics
        self.percent_of_correct_answers_by_topic = number_of_correct_answers_by_topic

    def to_dict(self):
        return {
            'topics': self.topics,
            'results': self.results,
            'deleting_message_id': self.deleting_message_id,
            'questions_count': self.questions_count,
            'variable_data': self.variable_data.to_dict(),
            'number_of_questions_by_topic': self.number_of_questions_by_topic,
            'selected_questions_by_topics': self.selected_questions_by_topics,
            'percent_of_correct_answers_by_topic': self.percent_of_correct_answers_by_topic
        }


class CommonData:
    def __init__(self, chat_id: int, theme: str = '', section: str = '', level: str = '', is_interview: bool = True, user_language: str = 'ru'):
        self.chat_id = chat_id
        self.theme = theme,
        self.section = section
        self.level = level
        self.is_interview = is_interview
        self.user_language = user_language

    def to_dict(self):
        return {
            'chat_id': self.chat_id,
            'theme': self.theme,
            'section': self.section,
            'level': self.level,
            'is_interview': self.is_interview,
            'user_language': self.user_language
        }


class UserData:
    def __init__(self, interview_data: Interview, common_data: CommonData, theme_data: List[Theme] = None):
        self.theme_data = theme_data
        self.interview_data = interview_data
        self.common_data = common_data

    def update(self,  theme_data: List[Theme]):
        self.theme_data = theme_data

    def to_dict(self):
        return {
            'theme_data': [theme.to_dict() for theme in self.theme_data] if self.theme_data else [],
            'interview_data': self.interview_data.to_dict() if self.interview_data else None,
            'common_data': self.common_data.to_dict()
        }
