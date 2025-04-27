from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
import os

QUESTION1, QUESTION2, QUESTION3, QUESTION4, QUESTION5 = range(5)

reply_keyboard = [
    ["Програмувати", "Захищати дані", "Аналізувати дані", "Будувати мережі"],
    ["Писати код", "Боротись з хакерами", "Будувати мережі"],
    ["Алгоритми", "Криптографія", "Мережі"],
    ["Програми", "Захист даних", "Мережеві рішення"],
    ["Створювати програми", "Захищати дані", "Керувати мережами"]
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)

user_answers = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привіт на Дні відкритих дверей ФКНТ!\nПройди короткий тест і дізнайся, ким ти можеш стати у світі ІТ!",
        reply_markup=markup
    )
    user_answers[update.effective_chat.id] = {"Програмувати": 0, "Захищати дані": 0, "Аналізувати дані": 0, "Будувати мережі": 0}
    return QUESTION1

async def question1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_choice = update.message.text
    user_answers[update.effective_chat.id][user_choice] += 1
    await update.message.reply_text("Що тобі цікавіше робити на проєкті?", reply_markup=markup)
    return QUESTION2

async def question2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_choice = update.message.text
    user_answers[update.effective_chat.id][user_choice] += 1
    await update.message.reply_text("Який предмет тобі цікавіше вивчати?", reply_markup=markup)
    return QUESTION3

async def question3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_choice = update.message.text
    user_answers[update.effective_chat.id][user_choice] += 1
    await update.message.reply_text("Яка діяльність тебе драйвить найбільше?", reply_markup=markup)
    return QUESTION4

async def question4(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_choice = update.message.text
    user_answers[update.effective_chat.id][user_choice] += 1
    await update.message.reply_text("Яку суперсилу ти б хотів мати?", reply_markup=markup)
    return QUESTION5

async def question5(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_choice = update.message.text
    user_answers[update.effective_chat.id][user_choice] += 1
    results = user_answers[update.effective_chat.id]
    top_category = max(results, key=results.get)

    if top_category in ["Програмувати", "Писати код", "Програми", "Створювати програми"]:
        role = "Software Engineer"
    elif top_category in ["Захищати дані", "Боротись з хакерами", "Криптографія", "Захист даних"]:
        role = "Фахівець з кібербезпеки або захисту інформації"
    elif top_category in ["Аналізувати дані", "Алгоритми"]:
        role = "Data Scientist"
    elif top_category in ["Будувати мережі", "Мережі", "Мережеві рішення", "Керувати мережами"]:
        role = "Інженер з комп'ютерних мереж"
    else:
        role = "Універсальний спеціаліст в ІТ!"

    await update.message.reply_text(
        f"Вітаємо! Ти — майбутній {role}!\n\nДізнатись більше можна на нашому сайті: https://fcst.nau.edu.ua/1st-course/"
    )
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Тест скасовано.')
    return ConversationHandler.END

def main():
    token = os.environ.get("TELEGRAM_TOKEN")
    app = ApplicationBuilder().token(token).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            QUESTION1: [MessageHandler(filters.TEXT & ~filters.COMMAND, question1)],
            QUESTION2: [MessageHandler(filters.TEXT & ~filters.COMMAND, question2)],
            QUESTION3: [MessageHandler(filters.TEXT & ~filters.COMMAND, question3)],
            QUESTION4: [MessageHandler(filters.TEXT & ~filters.COMMAND, question4)],
            QUESTION5: [MessageHandler(filters.TEXT & ~filters.COMMAND, question5)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == '__main__':
    main()