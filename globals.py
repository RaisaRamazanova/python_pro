import logging
import threading
from telegram.ext import ApplicationBuilder
from model import UserLevel

TOKEN = "6970949745:AAGLijdNA6lfdHzp3dDsdWPKAfn39ZJaKqs"


logger = logging.getLogger(__name__)
application = ApplicationBuilder().token(TOKEN).build()
lock = threading.Lock()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)