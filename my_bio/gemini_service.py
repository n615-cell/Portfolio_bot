import os
import re
import google.generativeai as genai
from content import *
from config import get_theme_by_time

# Настройка API
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

user_history = {}
user_style = {}


def get_style_prompt(style_name):
    styles = {
        "Классический": "Отвечай нейтрально, чётко, по делу.",
        "Поэтический": "Отвечай красиво, образно, используй метафоры.",
        "Тёплый": "Отвечай заботливо, мягко, как близкий друг.",
        "Технический": "Отвечай сухо, коротко, как документация.",
        "Юмористический": "Отвечай с лёгкостью, шутками, но не перебарщивай."
    }
    return styles.get(style_name, styles["Классический"])


def build_prompt(user_name, style_name, history):
    style_desc = get_style_prompt(style_name)
    theme = get_theme_by_time()

    history_text = ""
    if history:
        history_text = "Предыдущий диалог:\n" + "\n".join(history[-5:]) + "\n"

    return f"""
Ты — бот-портфолио Наз. Отвечай от первого лица, как будто ты Наз. Отвечай на русском языке, НЕ используй эмодзи. Обращайся к пользователю на "Вы" или по имени {user_name}.

Сейчас {theme['name']}, {theme['greeting']}.

Вот информация о Наз:

О СЕБЕ:
{ABOUT}

МОЯ ЦЕЛЬ:
{GOAL}

КАК ПРИШЛА В IT:
{HISTORY}

МОЙ МЕНТОР:
{MENTORS}

ПРОГРЕСС:
{PROGRESS}

ХОББИ:
Рисование: {HOBBIES["Рисование"]}
Писательство: {HOBBIES["Писательство"]}
Дополнительно: {HOBBIES["Дополнительно"]}
Баннеры: {HOBBIES["Баннеры"]}

МОИ РАБОТЫ:
1. FlashCLI - {WORKS[0]["description"]}
2. Игра Дино - {WORKS[1]["description"]}
3. Проект Чат - {WORKS[2]["description"]}
4. Блог Django - {WORKS[3]["description"]}

GITHUB:
{GITHUB}

ВДОХНОВЕНИЕ:
{INSPIRATION}

КНИГИ (мои любимые):
{BOOKS}

СТИЛЬ ОБЩЕНИЯ:
{style_desc}

ПРАВИЛА ОТВЕТОВ:
1. Отвечай кратко (2-4 предложения), но по делу.
2. НЕ используй эмодзи.
3. Отвечай от первого лица (я, мне, меня).
4. Обращайся к пользователю по имени {user_name} в начале ответа.
5. Учитывай историю диалога, если она есть.
6. Если вопрос не касается тебя напрямую — пошути или предложи спросить о своём опыте.

{history_text}
"""


def ask_gemini(user_question, user_name="Вы", chat_id=None):
    try:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            return "Ой, кажется, я потеряла свой API-ключ. Напишите Наз, чтобы она его проверила."

        style_name = user_style.get(chat_id, "Классический")
        history = user_history.get(chat_id, [])

        # Используем модель, которая точно работает с новой библиотекой
        model = genai.GenerativeModel("gemini-pro")

        prompt = build_prompt(user_name, style_name, history)
        full_prompt = f"{prompt}\n\nВопрос пользователя: {user_question}"

        # НОВЫЙ СИНТАКСИС ДЛЯ 0.8.6
        response = model.generate_content(
            contents=full_prompt,
            generation_config={
                "temperature": 0.7,
                "max_output_tokens": 250,
            }
        )

        answer = response.text

        # Убираем эмодзи
        answer = re.sub(r'[\U00010000-\U0010ffff]', '', answer)

        # Сохраняем историю
        if chat_id:
            if chat_id not in user_history:
                user_history[chat_id] = []
            user_history[chat_id].append(f"Пользователь: {user_question}")
            user_history[chat_id].append(f"Наз: {answer}")
            if len(user_history[chat_id]) > 10:
                user_history[chat_id] = user_history[chat_id][-10:]

        return answer

    except Exception as e:
        return f"Извините, произошла ошибка: {str(e)}"


def set_user_style(chat_id, style_name):
    user_style[chat_id] = style_name


def get_user_style(chat_id):
    return user_style.get(chat_id, "Классический")