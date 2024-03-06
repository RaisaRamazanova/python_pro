from repository.database_connection import DatabaseConnection
from repository.interview_topic_repo import InterviewTopicRepository
from repository.interview_question_repo import InterviewQuestionRepository
from repository.interview_repo import InterviewRepository
from repository.language_repo import LanguageRepository
from repository.onboarding_repo import OnboardingRepository
from repository.onboarding_stage_option_repo import OnboardingStageOptionRepository
from repository.onboarding_stage_repo import OnboardingStageRepository
from repository.stage_repo import StageRepository
from repository.stage_option_repo import StageOptionRepository
from repository.user_repo import UserRepository


def create_app_config(db_config):
    db_connection = DatabaseConnection(db_config)

    language_repo = LanguageRepository(db_connection)
    stage_repo = StageRepository(db_connection)
    stage_option_repo = StageOptionRepository(db_connection)
    user_repo = UserRepository(db_connection)
    onboarding_repo = OnboardingRepository(db_connection)
    onboarding_stage_repo = OnboardingStageRepository(db_connection)
    onboarding_stage_option_repo = OnboardingStageOptionRepository(db_connection)
    interview_repo = InterviewRepository(db_connection)
    interview_question_repo = InterviewQuestionRepository(db_connection)
    interview_topic_repo = InterviewTopicRepository(db_connection)

    return {
        "db_connection": db_connection,
        "language_repo": language_repo,
        "stage_repo": stage_repo,
        "stage_option_repo": stage_option_repo,
        "user_repo": user_repo,
        "onboarding_repo": onboarding_repo,
        "onboarding_stage_repo": onboarding_stage_repo,
        "onboarding_stage_option_repo": onboarding_stage_option_repo,
        "interview_repo": interview_repo,
        "interview_question_repo": interview_question_repo,
        "interview_topic_repo": interview_topic_repo
    }