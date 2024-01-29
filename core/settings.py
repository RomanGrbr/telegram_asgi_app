import os
from dotenv import load_dotenv


load_dotenv()

DEBUG = os.getenv('DEBUG')
BOT_TOKEN = os.getenv('DEVELOP_CHUSHPAN_TOKEN') if DEBUG else os.getenv('PROD_CHUSHPAN_TOKEN')
APP_TOKEN = os.getenv('APP_TOKEN')
NGROK_TOKEN = os.getenv('NGROK_TOKEN')

HOST = '127.0.0.1' if DEBUG else os.getenv('HOST')
PORT = 8000 if DEBUG else int(os.getenv('PORT'))
TELEGRAM_TO = os.getenv('TELEGRAM_TO')
