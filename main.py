from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
import os

# Стадії тесту
QUESTION1, QUESTION2, QUESTION3, QUESTION4, QUESTION5 = range(5)

# Питання та відповідні клавіатури
questions_text = {
    QUESTION1: "Що тобі більше подобається?",
    QUESTION2: "Який проєкт ти б хотів реалізувати?",
    QUESTION3: "Як тобі зручніше працювати?",
    QUESTION4: "Які дисципліни тобі цікавіше вивчати?",
    QUESTION5: "Яку суперсилу ти б вибрав?"
}

keyboards = {
    QUESTION1: [["Програмування", "Кібербезпека"], ["Аналіз даних", "Комп'ютерні мережі"]],
    QUESTION2: [["Мобільний додаток", "Система захисту даних"], ["Аналітична система", "Інтернет мережа"]],
    QUESTION3: [["Командна робота", "Індивідуальні завдання"]],
    QUESTION4: [["Алгоритми", "Криптографія"], ["Мережі", "Машинне навчання"]],
    QUESTION5: [["Створювати програми", "Захищати дані"], ["Керувати даними", "Будувати мережі"]]
}

# Профілі
profiles = ["Програмування", "Кібербезпека", "Аналіз даних", "Комп'ютерні мережі"]

# Пам'ять відповідей
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
    text = update.message.text

    for profile in profiles:
        if profile.lower() in text.lower():
            user_data[chat_id][profile] += 1

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
            "Кібербезпека": "Фахівець з кібербезпеки",
            "Аналіз даних": "Data Scientist",
            "Комп'ютерні мережі": "Network Engineer"
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

    # Запускаємо через webhook для Render
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get('PORT', 8443)),
        webhook_url=f"https://{os.environ['RENDER_EXTERNAL_HOSTNAME']}/{token}"
    )

if __name__ == '__main__':
    main()
