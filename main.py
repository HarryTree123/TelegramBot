from telegram import Bot, Update, ForceReply, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Application, ContextTypes, CallbackQueryHandler
from credits import bot_token
import requests


class Weather:
    def __init__(self):
        self.key = "c3050c3c2fee1937f5603badb34216c5"
        self.city = "Moscow"
        self.lang = "ru"

    def weather_info(self):
        response = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={self.key}&units=metric&lang={self.lang}")
        return response


async def answer_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    print(query.data, type(query.data))
    if query.data == "старт":
        await context.bot.send_message(update.effective_chat.id, "chose button1")
    if query.data == 2:
        await context.bot.send_message(update.effective_chat.id, "chose button2")
    if query.data == 3:
        await context.bot.send_message(update.effective_chat.id, "chose button3")
    if query.data == 4:
        await context.bot.send_message(update.effective_chat.id, "chose button4")


class MyBot:
    def __init__(self, bot_token):
        self.application = Application.builder().token(bot_token).build()

        # Регистрируем обработчики команд
        self.application.add_handler(CallbackQueryHandler(self.answerButton))
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("button", self.createButton))
        self.application.add_handler(CommandHandler("help", self.help))
        self.application.add_handler(CommandHandler("weather", self.weather))

        self.application.run_polling(allowed_updates=Update.ALL_TYPES)

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send a message when the command /start is issued."""
        print(update)
        user = update.effective_user
        print(user.mention_html())
        await update.message.reply_html(
            f"Hi {user.mention_html()}!",
        )

    async def createButton(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        keyboard = [
            [InlineKeyboardButton("button 1", callback_data="старт"), InlineKeyboardButton("button 2", callback_data=2),
             InlineKeyboardButton("button 3", callback_data=3), ],
            [InlineKeyboardButton("button 4", callback_data=4)]
        ]
        await update.message.reply_text("Quetions", reply_markup=InlineKeyboardMarkup(keyboard))

    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(text="Этот простой бот может отвечать на запросы связанные с погодой.")

    async def weather(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            text=f"Здравствуйте! Это WeatherBot. Чтобы узнать погоду в нужном Вам городе, напишите его название\n")
        obj_Weather = Weather()
        result = obj_Weather.weather_info()
        weather_description = result.json()['weather'][0]['description']
        temp = result.json()['main']['temp']

        await update.message.reply_text(text=f"fyghj {weather_description}\nexample {temp}")


if __name__ == "__main__":
    # Замените 'YOUR_BOT_TOKEN' на токен вашего бота
    bot = MyBot(bot_token=bot_token)
