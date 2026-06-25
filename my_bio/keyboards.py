from telebot import types

def main_menu():
    keyboard = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    buttons = [
        "👤 Обо мне", "🎯 Цель", "📖 История",
        "👩‍🏫 Менторы", "📈 Прогресс", "🎨 Хобби",
        "💻 Проекты", "🌸 Вдохновение", "✨ Факт",
        "📚 Книги", "❓ Викторина", "❓ Вопросы"
    ]
    keyboard.add(*buttons)
    return keyboard

def mentor_menu():
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = ["👩‍🏫 Жасмин", "👩‍🏫 Гульнура", "👩‍🏫 Диана", "📝 Другие", "🔙 Назад"]
    keyboard.add(*buttons)
    return keyboard

def hobby_menu():
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = [
        "🎨 Рисование",
        "✍️ Писательство",
        "🌟 Дополнительно",
        "🎨 Баннеры",
        "🔙 Назад"
    ]
    keyboard.add(*buttons)
    return keyboard

def drawing_menu():
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = [
        "🖼️ Арты",
        "🎨 Процесс",
        "🔙 К хобби"
    ]
    keyboard.add(*buttons)
    return keyboard

def arts_navigation_menu():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        types.InlineKeyboardButton("⬅️ Предыдущий", callback_data="art_prev"),
        types.InlineKeyboardButton("Следующий ➡️", callback_data="art_next"),
        types.InlineKeyboardButton("🔙 К рисованию", callback_data="back_to_drawing")
    )
    return keyboard

def process_navigation_menu():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        types.InlineKeyboardButton("⬅️ Предыдущий", callback_data="process_prev"),
        types.InlineKeyboardButton("Следующий ➡️", callback_data="process_next"),
        types.InlineKeyboardButton("🔙 К рисованию", callback_data="back_to_drawing")
    )
    return keyboard

def books_menu():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    buttons = ["📖 Собор Парижской Богоматери", "📖 Человек который смеется", "📖 Королева Марго", "📖 Унесённые ветром", "📖 Три товарища", "🔙 Назад"]
    keyboard.add(*buttons)
    return keyboard

def works_menu():
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = ["💡 FlashCLI", "🦕 Игра Дино", "💬 Проект Чат", "📝 Блог Django", "🔙 Назад"]
    keyboard.add(*buttons)
    return keyboard

def work_detail_menu(work_name):
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    if work_name in ["FlashCLI", "Блог Django"]:
        buttons = ["📖 Описание", "🐙 GitHub", "🔙 К проектам"]
    else:
        buttons = ["📖 Описание", "📸 Скриншоты", "🔙 К проектам"]
    keyboard.add(*buttons)
    return keyboard

def banner_menu():
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = ["📖 Описание", "🖼️ Примеры", "🔙 Назад"]
    keyboard.add(*buttons)
    return keyboard

def quiz_menu():
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = ["🟢 Лёгкий", "🟡 Средний", "🔴 Сложный", "🔙 Назад"]
    keyboard.add(*buttons)
    return keyboard