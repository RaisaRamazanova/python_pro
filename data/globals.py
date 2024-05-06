import logging
import threading
from telegram.ext import ApplicationBuilder

TOKEN = "6914866790:AAHQFOHkYzPqRSByECISnNwGRLy1uXFieU8"
PAYMENTS_TOKEN = '381764678:TEST:76546'

logger = logging.getLogger(__name__)
application = ApplicationBuilder().token(TOKEN).build()
lock = threading.Lock()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

db_config = {
    'dbname': 'interview_bot',
    'user': 'raisatramazanova',
    'password': 'qwerty',
    'host': '127.0.0.1'
}