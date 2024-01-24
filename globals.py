import logging
import threading
from telegram.ext import ApplicationBuilder


TOKEN = "6914866790:AAHQFOHkYzPqRSByECISnNwGRLy1uXFieU8"

path_questions = "/Users/raisatramazanova/development/python_bot/python_pro_bot/sm_questions.sqlite"
path_answers = "/Users/raisatramazanova/development/python_bot/python_pro_bot/sm_answers.sqlite"

logger = logging.getLogger(__name__)
application = ApplicationBuilder().token(TOKEN).build()
lock = threading.Lock()

global_state = {}
junior_state = {}

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)