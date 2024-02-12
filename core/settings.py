import os

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = os.getenv('DEBUG').lower() == 'true'

# Токен от BotFather
BOT_TOKEN = os.getenv('DEVELOP_CHUSHPAN_TOKEN') if DEBUG else os.getenv('PROD_CHUSHPAN_TOKEN')

# Токен приложения
APP_TOKEN = os.getenv('APP_TOKEN')

# Ngrok токен
NGROK_TOKEN = os.getenv('NGROK_TOKEN')

# Настройки хоста
HOST = '127.0.0.1' if DEBUG else os.getenv('HOST')
PORT = 8000 if DEBUG else int(os.getenv('PORT'))

TELEGRAM_TO = os.getenv('TELEGRAM_TO')

TELEGRAM_API = 'https://api.telegram.org'

# The file upload directory
MEDIA_ROOT = 'media'
