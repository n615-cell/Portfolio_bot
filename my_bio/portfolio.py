import sys
import re
import random
import time
import telebot
from telebot import types
import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import io

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DEBUG_MODE = "--debug" in sys.argv

from config import get_theme_by_time
from content import *
from keyboards import *

bot = telebot.TeleBot(BOT_TOKEN)

user_names = {}
user_states = {}
user_quiz = {}
user_art_index = {}
user_process_index = {}

FACTS = [
    "Я люлблю французскую литературу",
    "Моя любимая книга — «Человек который смеется» Гюго",
    "Способна усвоить информацию за считанные дни",
    "Мой любимый мультфильм — «Мулан»",
    "Я прочитала свыше 300 книг",
    "Мой любимый цвет — фиолетовый",
    "Я рисую в диджитал-формате с 10 лет",
    "Мои арты вдохновляли людей на создание книг",
    "Я заняла 1 место на олимпиаде по географии",
    "Мой первый проект был игрой камень-ножницы-бумага",
    "Я могу написать стихотворение за 25 минут",
    "Мне нравится изучать языки: английский, французский и турецкий",
    "Я мечтаю создать продукт, который поможет миллионам людей",
    "Мои менторы и куратор стали главной опорой в начинаниях",
    "В свободное время я смотрю старые мультфильмы Disney"
]

def generate_progress_chart():
    skills = {"Python": 80, "Django": 60, "Pygame": 50, "Telegram боты": 75}
    categories = list(skills.keys())
    values = list(skills.values())
    N = len(categories)
    angles = [n / float(N) * 2 * 3.14159 for n in range(N)]
    angles += angles[:1]
    values += values[:1]
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    ax.plot(angles, values, 'o-', linewidth=2, color='#7B3F8C')
    ax.fill(angles, values, alpha=0.25, color='#7B3F8C')
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, size=12)
    ax.set_ylim(0, 100)
    ax.set_yticks([20, 40, 60, 80, 100])
    ax.set_yticklabels(['20%', '40%', '60%', '80%', '100%'], size=10)
    ax.set_title('Мои навыки в программировании', size=16, pad=20)
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', facecolor='#F5F0FF')
    buf.seek(0)
    plt.close()
    return buf

def generate_horizontal_chart():
    skills = HORIZONTAL_SKILLS
    categories = list(skills.keys())
    values = list(skills.values())
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(categories, values, color='#7B3F8C')
    ax.set_xlim(0, 100)
    ax.set_xlabel('Уровень (%)', size=12)
    ax.set_title('Мои творческие навыки', size=16)
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 1, bar.get_y() + bar.get_height()/2, f'{width}%', va='center', fontsize=10)
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', facecolor='#F5F0FF')
    buf.seek(0)
    plt.close()
    return buf

def extract_name(text):
    patterns = [
        r"меня зовут\s+([А-Яа-яЁёA-Za-z]+)",
        r"я\s+([А-Яа-яЁёA-Za-z]+)",
        r"зовут\s+([А-Яа-яЁёA-Za-z]+)",
        r"называйте\s+([А-Яа-яЁёA-Za-z]+)"
    ]
    for pattern in patterns:
        match = re.search(pattern, text.lower())
        if match:
            return match.group(1).capitalize()
    words = text.strip().split()
    if words:
        return words[0].capitalize()
    return None

def normalize_text(text):
    return re.sub(r'[^a-zA-Zа-яА-Я0-9\s]', '', text.lower().strip())

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "🌟 Здравствуйте! Меня зовут Наз. А как мне к вам обращаться?", reply_markup=types.ReplyKeyboardRemove())

@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = """📖 Доступные команды:
/start - Начать заново (спросит имя)
/help - Помощь"""
    bot.send_message(message.chat.id, help_text)

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    chat_id = message.chat.id
    text = message.text
    theme = get_theme_by_time()

    if chat_id not in user_names:
        name = extract_name(text)
        if name:
            user_names[chat_id] = name
            bot.send_message(chat_id, f"{theme['greeting']}, {name}! ✨\nЯ — Наз, и я рада познакомиться с вами.\nВыберите раздел в меню ниже:", reply_markup=main_menu())
        else:
            bot.send_message(chat_id, "Пожалуйста, скажите, как вас зовут.\nНапишите, например: «Меня зовут Алия».", reply_markup=types.ReplyKeyboardRemove())
        return

    if text == "❓ Викторина":
        bot.send_message(chat_id, "🎯 Выберите уровень сложности:", reply_markup=quiz_menu())
        return

    if text in ["🟢 Лёгкий", "🟡 Средний", "🔴 Сложный"]:
        level_map = {"🟢 Лёгкий": "easy", "🟡 Средний": "medium", "🔴 Сложный": "hard"}
        level = level_map[text]
        questions = QUIZ_QUESTIONS[level]
        random.shuffle(questions)
        user_quiz[chat_id] = {"level": level, "questions": questions, "index": 0, "correct": 0, "total": len(questions)}
        send_quiz_question(chat_id)
        return

    if text == "🔙 Назад" and chat_id in user_quiz:
        del user_quiz[chat_id]
        bot.send_message(chat_id, "🏠 Вы вернулись в главное меню.", reply_markup=main_menu())
        return

    if chat_id in user_quiz:
        check_quiz_answer(chat_id, text)
        return

    if text == "❓ Вопросы":
        questions_list = "\n".join([f"• {data['question']}" for key, data in QUESTIONS_BLOCK.items()])
        bot.send_message(chat_id, f"❓ Вот список вопросов, на которые я могу ответить:\n\n{questions_list}\n\n✏️ Просто напиши мне вопрос!", reply_markup=main_menu())
        return

    for key, data in QUESTIONS_BLOCK.items():
        if normalize_text(text) == normalize_text(data["question"]) or text.lower() in data["question"]:
            if key == "q4":
                answer = random.choice(data["answers"])
            elif isinstance(data["answers"], list):
                answer = random.choice(data["answers"])
            else:
                answer = data["answers"]
            bot.send_message(chat_id, f"💬 {answer}", reply_markup=main_menu())
            return

    # главное меню
    if text == "👤 Обо мне":
        bot.send_message(chat_id, f"👤 О себе:\n\n{ABOUT}", reply_markup=main_menu())
        return

    if text == "🎯 Цель":
        bot.send_message(chat_id, f"🎯 Моя цель:\n\n{GOAL}", reply_markup=main_menu())
        return

    if text == "📖 История":
        bot.send_message(chat_id, f"📖 Моя история:\n\n{HISTORY}", reply_markup=main_menu())
        return

    if text == "📈 Прогресс":
        bot.send_message(chat_id, "📊 Генерирую графики...")
        try:
            img1 = generate_progress_chart()
            bot.send_photo(chat_id, img1, caption="📊 Мой прогресс в программировании")
            img2 = generate_horizontal_chart()
            bot.send_photo(chat_id, img2, caption="📊 Мои творческие навыки")
        except Exception as e:
            bot.send_message(chat_id, f"Ошибка при генерации графиков: {e}")
        bot.send_message(chat_id, f"📈 А ещё вот что я рассказываю о своём прогрессе:\n\n{PROGRESS}", reply_markup=main_menu())
        return

    if text == "🌸 Вдохновение":
        bot.send_message(chat_id, f"🌸 Вдохновение:\n\n{INSPIRATION}", reply_markup=main_menu())
        return

    if text == "✨ Факт":
        bot.send_message(chat_id, f"✨ {random.choice(FACTS)}", reply_markup=main_menu())
        return

    if text == "🖼️ Мои арты":
        bot.send_message(chat_id, "🎨 Выберите, что хотите посмотреть:", reply_markup=my_arts_menu())
        return

    if text == "🖼️ Арты":
        user_art_index[chat_id] = 0
        send_art(chat_id, from_main_menu=True)
        return

    if text == "🎨 Процесс":
        user_process_index[chat_id] = 0
        send_process(chat_id, from_main_menu=True)
        return

    if text == "🔙 Назад" and chat_id in user_art_index:
        if chat_id in user_art_index:
            del user_art_index[chat_id]
        if chat_id in user_process_index:
            del user_process_index[chat_id]
        bot.send_message(chat_id, "🏠 Главное меню:", reply_markup=main_menu())
        return

    if text == "👩‍🏫 Менторы":
        bot.send_message(chat_id, "👩‍🏫 Какой ментор интересует?", reply_markup=mentor_menu())
        return

    if text == "👩‍🏫 Жасмин":
        bot.send_message(chat_id, f"👩‍🏫 Жасмин тичер:\n\n{MENTORS['Жасмин тичер']}", reply_markup=mentor_menu())
        return

    if text == "👩‍🏫 Гульнура":
        bot.send_message(chat_id, f"👩‍🏫 Гульнура тичер:\n\n{MENTORS['Гульнура тичер']}", reply_markup=mentor_menu())
        return

    if text == "👩‍🏫 Диана":
        bot.send_message(chat_id, f"👩‍🏫 Диана Е. тичер:\n\n{MENTORS['Диана Е. тичер']}", reply_markup=mentor_menu())
        return

    if text == "📝 Другие":
        bot.send_message(chat_id, f"📝 Другие менторы:\n\n{MENTORS_EXTRA}", reply_markup=mentor_menu())
        return

    if text == "🎨 Хобби":
        bot.send_message(chat_id, "🎨 Какой раздел вас интересует?", reply_markup=hobby_menu())
        return

    if text in ["🎨 Рисование", "✍️ Писательство", "🌟 Дополнительно"]:
        hobby_name = text.replace("🎨 ", "").replace("✍️ ", "").replace("🌟 ", "")
        full_text = HOBBIES.get(hobby_name, "Описание не найдено")
        bot.send_message(chat_id, f"🎨 {hobby_name}:\n\n{full_text}", reply_markup=hobby_menu())
        return

    if text == "🎨 Рисование":
        bot.send_message(chat_id, f"🎨 Рисование:\n\n{HOBBIES['Рисование']}", reply_markup=drawing_menu())
        return

    if text == "🖼️ Арты":
        user_art_index[chat_id] = 0
        send_art(chat_id)
        return

    if text == "🎨 Процесс":
        user_process_index[chat_id] = 0
        send_process(chat_id)
        return

    if text == "🔙 К хобби":
        bot.send_message(chat_id, "🎨 Возвращаемся в раздел хобби.", reply_markup=hobby_menu())
        return

    if text == "🎨 Баннеры":
        user_states[chat_id] = "banner"
        bot.send_message(chat_id, "🎨 Мои баннеры. Что хотите сделать?", reply_markup=banner_menu())
        return

    if text == "📖 Описание" and chat_id in user_states and user_states[chat_id] == "banner":
        bot.send_message(chat_id, f"🎨 Баннеры:\n\n{HOBBIES['Баннеры']}", reply_markup=banner_menu())
        return

    if text == "🖼️ Примеры" and chat_id in user_states and user_states[chat_id] == "banner":
        for banner_url in BANNERS:
            try:
                bot.send_photo(chat_id, banner_url)
            except Exception:
                bot.send_message(chat_id, f"Не удалось загрузить баннер. Ссылка: {banner_url}")
        bot.send_message(chat_id, "Вот мои баннеры! 🎨", reply_markup=banner_menu())
        return

    if text == "📚 Книги":
        bot.send_message(chat_id, "📚 Здесь мои любимые книги! О какой хотите узнать больше?", reply_markup=books_menu())
        return

    if text in ["📖 Собор Парижской Богоматери", "📖 Человек который смеется", "📖 Королева Марго", "📖 Унесённые ветром", "📖 Три товарища"]:
        book_name = text.replace("📖 ", "")
        description = BOOKS.get(book_name, "Описание не найдено")
        bot.send_message(chat_id, f"📖 {book_name}:\n\n{description}", reply_markup=books_menu())
        return

    if text == "💻 Проекты":
        bot.send_message(chat_id, "💻 Какой проект вас интересует?", reply_markup=works_menu())
        return

    if text in ["💡 FlashCLI", "🦕 Игра Дино", "💬 Проект Чат", "📝 Блог Django"]:
        work_name = text.replace("💡 ", "").replace("🦕 ", "").replace("💬 ", "").replace("📝 ", "")
        user_names[f"{chat_id}_work"] = work_name
        bot.send_message(chat_id, f"💻 Что вы хотите узнать о проекте «{work_name}»?", reply_markup=work_detail_menu(work_name))
        return

    if text == "📖 Описание":
        work_name = user_names.get(f"{chat_id}_work", "")
        for work in WORKS:
            if work["name"] == work_name:
                bot.send_message(chat_id, f"💻 {work['name']}:\n\n{work['description']}", reply_markup=work_detail_menu(work_name))
                break
        return

    if text == "🐙 GitHub":
        work_name = user_names.get(f"{chat_id}_work", "")
        for work in WORKS:
            if work["name"] == work_name and work.get("repo"):
                bot.send_message(chat_id, f"🐙 Репозиторий:\n{work['repo']}", reply_markup=work_detail_menu(work_name))
                break
            elif work["name"] == work_name:
                bot.send_message(chat_id, "У этого проекта нет отдельного репозитория.", reply_markup=work_detail_menu(work_name))
                break
        return

    if text == "📸 Скриншоты":
        work_name = user_names.get(f"{chat_id}_work", "")
        for work in WORKS:
            if work["name"] == work_name:
                screenshots = work.get("screenshots", [])
                if screenshots:
                    for url in screenshots:
                        try:
                            bot.send_photo(chat_id, url)
                        except Exception:
                            bot.send_message(chat_id, f"Не удалось загрузить скриншот. Ссылка: {url}")
                    bot.send_message(chat_id, "Вот скриншоты проекта! 📸", reply_markup=work_detail_menu(work_name))
                else:
                    bot.send_message(chat_id, "У этого проекта нет скриншотов.", reply_markup=work_detail_menu(work_name))
                break
        return

    if text == "🔙 К проектам":
        bot.send_message(chat_id, "💻 Какой проект вас интересует?", reply_markup=works_menu())
        if f"{chat_id}_work" in user_names:
            del user_names[f"{chat_id}_work"]
        return

    if text == "🔙 Назад" or text == "🔙 Главное меню":
        if chat_id in user_quiz:
            del user_quiz[chat_id]
        if chat_id in user_states:
            del user_states[chat_id]
        bot.send_message(chat_id, "🏠 Главное меню:", reply_markup=main_menu())
        return

    bot.send_message(chat_id, "Пожалуйста, используйте кнопки меню для навигации.", reply_markup=main_menu())

@bot.callback_query_handler(func=lambda call: True)
def handle_inline(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    if call.data == "art_next":
        user_art_index[chat_id] = (user_art_index.get(chat_id, 0) + 1) % len(ARTS)
        send_art(chat_id, message_id)
        bot.answer_callback_query(call.id)
        return

    if call.data == "art_prev":
        user_art_index[chat_id] = (user_art_index.get(chat_id, 0) - 1) % len(ARTS)
        send_art(chat_id, message_id)
        bot.answer_callback_query(call.id)
        return

    if call.data == "back_to_drawing":
        bot.edit_message_text("🎨 Рисование:\n\n" + HOBBIES["Рисование"], chat_id, message_id, reply_markup=drawing_menu())
        bot.answer_callback_query(call.id)
        return

    if call.data == "process_next":
        user_process_index[chat_id] = (user_process_index.get(chat_id, 0) + 1) % len(PROCESS_IMAGES)
        send_process(chat_id, message_id)
        bot.answer_callback_query(call.id)
        return

    if call.data == "process_prev":
        user_process_index[chat_id] = (user_process_index.get(chat_id, 0) - 1) % len(PROCESS_IMAGES)
        send_process(chat_id, message_id)
        bot.answer_callback_query(call.id)
        return

def send_quiz_question(chat_id):
    data = user_quiz[chat_id]
    index = data["index"]
    total = data["total"]
    question_data = data["questions"][index]
    question_text = question_data["question"]
    bot.send_message(chat_id, f"❓ Вопрос {index+1}/{total}:\n\n{question_text}\n\n✏️ Напишите свой ответ!")

def check_quiz_answer(chat_id, user_answer):
    data = user_quiz[chat_id]
    index = data["index"]
    question_data = data["questions"][index]
    correct_answers = [normalize_text(ans) for ans in question_data["answers"]]
    user_norm = normalize_text(user_answer)

    if user_norm in correct_answers:
        data["correct"] += 1
        feedbacks = ["✅ Правильно!", "🎉 Отлично!", "⭐ Верно!"]
        bot.send_message(chat_id, random.choice(feedbacks))
    else:
        feedbacks = ["❌ Неверно.", "😅 Почти!", "🤔 Попробуй ещё раз в следующий раз."]
        bot.send_message(chat_id, f"{random.choice(feedbacks)} Правильный ответ: {question_data['answers'][0]}")

    data["index"] += 1
    if data["index"] >= data["total"]:
        correct = data["correct"]
        total = data["total"]
        percentage = int(correct / total * 100)
        bot.send_message(chat_id, f"🏆 Викторина завершена!\nВы ответили правильно на {correct} из {total} вопросов ({percentage}%).", reply_markup=quiz_menu())
        del user_quiz[chat_id]
    else:
        send_quiz_question(chat_id)

def send_art(chat_id, message_id=None, from_main_menu=False):
    index = user_art_index.get(chat_id, 0)
    art_url = ARTS[index]
    caption = f"🖼️ Арт {index+1} из {len(ARTS)}"
    if message_id:
        bot.edit_message_media(types.InputMediaPhoto(art_url, caption=caption), chat_id, message_id, reply_markup=arts_navigation_menu())
    else:
        bot.send_photo(chat_id, art_url, caption=caption, reply_markup=arts_navigation_menu())

def send_process(chat_id, message_id=None, from_main_menu=False):
    index = user_process_index.get(chat_id, 0)
    process_url = PROCESS_IMAGES[index]
    caption = f"🎨 Этап {index+1} из {len(PROCESS_IMAGES)}"
    if message_id:
        bot.edit_message_media(types.InputMediaPhoto(process_url, caption=caption), chat_id, message_id, reply_markup=process_navigation_menu())
    else:
        bot.send_photo(chat_id, process_url, caption=caption, reply_markup=process_navigation_menu())

if __name__ == "__main__":
    if "--debug" in sys.argv:
        print("🔍 Режим отладки включён")
    while True:
        try:
            print("🚀 Бот запущен в режиме поллинга...")
            bot.infinity_polling()
        except Exception as e:
            print(f"❌ Бот упал: {e}. Перезапуск через 5 секунд...")
            time.sleep(5)