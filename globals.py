import logging
import threading
from telebot.types import LabeledPrice
from telegram.ext import ApplicationBuilder


TOKEN = "6914866790:AAHQFOHkYzPqRSByECISnNwGRLy1uXFieU8"
PAYMENTS_TOKEN = '381764678:TEST:76546'

MIDDLE_PRICE = LabeledPrice(label='Покупка Middle тарифа',amount=49900)
SENIOR_PRICE = LabeledPrice(label='Покупка Senior тарифа',amount=79900)

path_questions = "/Users/raisatramazanova/development/python_bot/python_pro_bot/{level}_sm_questions.sqlite"
path_answers = "/Users/raisatramazanova/development/python_bot/python_pro_bot/{level}_sm_answers.sqlite"

logger = logging.getLogger(__name__)
application = ApplicationBuilder().token(TOKEN).build()
lock = threading.Lock()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)