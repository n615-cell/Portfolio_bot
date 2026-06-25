import os
from dotenv import load_dotenv
import sys
import datetime
import pytz

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

DEBUG_MODE = "--debug" in sys.argv


def get_theme_by_time():
    """Определяет тему в зависимости от времени суток (Казахстан, GMT+5)"""
    tz = pytz.timezone('Asia/Almaty')
    now = datetime.datetime.now(tz)
    hour = now.hour

    if 6 <= hour < 12:
        return {
            "name": "утро",
            "greeting": "Доброе утро",
            "color": "#D4B8E0",
            "emoji": "🌅"
        }
    elif 12 <= hour < 18:
        return {
            "name": "день",
            "greeting": "Добрый день",
            "color": "#7B3F8C",
            "emoji": "☀️"
        }
    elif 18 <= hour < 23:
        return {
            "name": "вечер",
            "greeting": "Добрый вечер",
            "color": "#4A1A5E",
            "emoji": "🌆"
        }
    else:
        return {
            "name": "ночь",
            "greeting": "Доброй ночи",
            "color": "#2E0A3A",
            "emoji": "🌙"
        }