from repository.answer_repo import AnswerRepository
from repository.database_connection import DatabaseConnection
from repository.interview_question_answer_repo import InterviewQuestionAnswerRepository
from repository.interview_statistics_repo import InterviewStatisticsRepository
from repository.question_repo import QuestionRepository
from repository.interview_topic_repo import InterviewTopicRepository
from repository.interview_question_repo import InterviewQuestionRepository
from repository.interview_repo import InterviewRepository
from repository.language_repo import LanguageRepository
from repository.onboarding_repo import OnboardingRepository
from repository.onboarding_stage_option_repo import OnboardingStageOptionRepository
from repository.onboarding_stage_repo import OnboardingStageRepository
from repository.stage_repo import StageRepository
from repository.stage_option_repo import StageOptionRepository
from repository.system_setting_repo import SystemSettingRepository
from repository.user_level_repo import UserLevelRepository
from repository.user_repo import UserRepository


def create_app_config(db_config):
    db_connection = DatabaseConnection(db_config)

    language_repo = LanguageRepository(db_connection)
    stage_repo = StageRepository(db_connection)
    stage_option_repo = StageOptionRepository(db_connection)
    user_repo = UserRepository(db_connection)
    user_level_repo = UserLevelRepository(db_connection)
    onboarding_repo = OnboardingRepository(db_connection)
    onboarding_stage_repo = OnboardingStageRepository(db_connection)
    onboarding_stage_option_repo = OnboardingStageOptionRepository(db_connection)
    interview_repo = InterviewRepository(db_connection)
    interview_topic_repo = InterviewTopicRepository(db_connection)
    interview_question_repo = InterviewQuestionRepository(db_connection)
    question_repo = QuestionRepository(db_connection)
    interview_question_answer_repo = InterviewQuestionAnswerRepository(db_connection)
    answer_repo = AnswerRepository(db_connection)
    system_setting_repo = SystemSettingRepository(db_connection)
    interview_statistics_repo = InterviewStatisticsRepository(db_connection)

    return {
        "db_connection": db_connection,
        "language_repo": language_repo,
        "stage_repo": stage_repo,
        "stage_option_repo": stage_option_repo,
        "user_repo": user_repo,
        "user_level_repo": user_level_repo,
        "onboarding_repo": onboarding_repo,
        "onboarding_stage_repo": onboarding_stage_repo,
        "onboarding_stage_option_repo": onboarding_stage_option_repo,
        "interview_repo": interview_repo,
        "interview_topic_repo": interview_topic_repo,
        "interview_question_repo": interview_question_repo,
        "question_repo": question_repo,
        "interview_question_answer_repo": interview_question_answer_repo,
        "answer_repo": answer_repo,
        "system_setting_repo": system_setting_repo,
        "interview_statistics_repo": interview_statistics_repo
    }
