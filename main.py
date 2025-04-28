from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
import os

# Стадії тесту
QUESTION1, QUESTION2, QUESTION3, QUESTION4, QUESTION5 = range(5)

# Оновлені питання
questions_text = {
    QUESTION1: "Що тебе найбільше захоплює у світі ІТ?",
    QUESTION2: "Який проєкт ти мрієш реалізувати?",
    QUESTION3: "Як тобі зручніше працювати в команді?",
    QUESTION4: "Який тип завдань приносить тобі найбільше задоволення?",
    QUESTION5: "Якою суперсилою ти б хотів володіти в ІТ?"
}

# Оновлені варіанти відповідей
keyboards = {
    QUESTION1: [["Писати код", "Захищати дані"], ["Аналізувати інформацію", "Будувати мережі"]],
    QUESTION2: [["Розробити мобільний додаток", "Створити систему захисту"], ["Побудувати аналітичну платформу", "Налаштувати складну мережу"], ["Обробляти зображення", "Розробити вбудовану систему"], ["Підтримувати сервери"]],
    QUESTION3: [["Співпрацювати в команді", "Працювати самостійно"]],
    QUESTION4: [["Структури даних і алгоритми", "Кіберзахист і криптографія"], ["Архітектура комп'ютерних мереж", "Штучний інтелект і машинне навчання"], ["Комп'ютерний зір", "Вбудовані системи"]],
    QUESTION5: [["Створювати інноваційні програми", "Зупиняти кібератаки"], ["Відкривати закономірності в даних", "Створювати мережеву інфраструктуру"], ["Обробляти відео- та фотодані", "Проєктувати електронні пристрої"], ["Адмініструвати сервери"]]
}

# Профілі
profiles = [
    "Програмування",
    "Захист інформації",
    "Аналіз даних",
    "Комп'ютерні мережі",
    "Комп'ютерний зір",
    "Вбудовані системи",
    "Системне адміністрування"
]

# Пам'ять відповідей користувачів
user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_data[chat_id] = {profile: 0 for profile in profiles}
    
    context.user_data['state'] = QUESTION1

    await update.message.reply_text(
        f"Привіт! 👋 Давай визначимо, хто ти в ІТ! 🚀\n\n{questions_text[QUESTION1]}",
        reply_markup=ReplyKeyboardMarkup(keyboards[QUESTION1], one_time_keyboard=True, resize_keyboard=True)
    )
    return QUESTION1

async def handle_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    text = update.message.text.lower()

    # Підрахунок балів
    if any(kw in text for kw in ["код", "мобільний додаток", "структури даних", "інноваційні програми"]):
        user_data[chat_id]["Програмування"] += 1
    if any(kw in text for kw in ["захист", "кібератаки", "кіберзахист", "система захисту"]):
        user_data[chat_id]["Захист інформації"] += 1
    if any(kw in text for kw in ["аналіз", "аналітична платформа", "машинне навчання", "дані"]):
        user_data[chat_id]["Аналіз даних"] += 1
    if any(kw in text for kw in ["мережа", "інтернет", "мережева інфраструктура", "архітектура мереж"]):
        user_data[chat_id]["Комп'ютерні мережі"] += 1
    if any(kw in text for kw in ["зображення", "комп'ютерний зір", "відео", "фото"]):
        user_data[chat_id]["Комп'ютерний зір"] += 1
    if any(kw in text for kw in ["вбудована система", "вбудовані системи", "електронні пристрої"]):
        user_data[chat_id]["Вбудовані системи"] += 1
    if any(kw in text for kw in ["сервери", "адмініструвати", "системний адміністратор"]):
        user_data[chat_id]["Системне адміністрування"] += 1

    current_state = context.user_data.get('state', QUESTION1)
    next_state = current_state + 1

    if next_state <= QUESTION5:
        await update.message.reply_text(
            questions_text[next_state],
            reply_markup=ReplyKeyboardMarkup(keyboards[next_state], one_time_keyboard=True, resize_keyboard=True)
        )
        context.user_data['state'] = next_state
        return next_state
    else:
        top_profile = max(user_data[chat_id], key=user_data[chat_id].get)
        role = {
            "Програмування": "Software Engineer",
            "Захист інформації": "Information Security Specialist",
            "Аналіз даних": "Data Scientist",
            "Комп'ютерні мережі": "Network Engineer",
            "Комп'ютерний зір": "Computer Vision Engineer",
            "Вбудовані системи": "Embedded Systems Engineer",
            "Системне адміністрування": "System Administrator"
        }[top_profile]

        await update.message.reply_text(
            f"Вітаємо! 🎉 Ти — майбутній {role}!\n\nБільше інформації тут 👉 https://fcst.nau.edu.ua/1st-course/",
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Тест скасовано.', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def main():
    token = os.environ.get("TELEGRAM_TOKEN")
    app = ApplicationBuilder().token(token).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            QUESTION1: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_question)],
            QUESTION2: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_question)],
            QUESTION3: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_question)],
            QUESTION4: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_question)],
            QUESTION5: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_question)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    app.add_handler(conv_handler)

    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get('PORT', 8443)),
        webhook_url=f"https://{os.environ['RENDER_EXTERNAL_HOSTNAME']}"
    )

if __name__ == '__main__':
    main()
