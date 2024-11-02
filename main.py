import telebot
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)

API_TOKEN = '8047776117:AAHbhIHrp_qY1egwP1_LZrMG4oTILDsRF9I'  # Замените на ваш токен
bot = telebot.TeleBot(API_TOKEN)

# Список для хранения проектов
projects = []


@bot.message_handler(commands=['start'])
def start_command_handler(message: telebot.types.Message):
    """
    Обработчик команды /start.
    Отправляет приветственное сообщение пользователю с одноразовой клавиатурой.
    """
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button = telebot.types.KeyboardButton("👉 Нажми меня!")
    markup.add(button)

    bot.send_message(message.chat.id, "👋 Привет! Добро пожаловать в Бот-портфолио! 🌟\n"
                                      "Нажми на кнопку ниже, чтобы продолжить:", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "👉 Нажми меня!")
def button_handler(message: telebot.types.Message):
    """
    Обработчик нажатия на кнопку.
    Отправляет сообщение с дальнейшими инструкциями и скрывает клавиатуру.
    """
    bot.send_message(message.chat.id, "✨ Спасибо за нажатие! Что бы ты хотел сделать дальше?\n"
                                      "🔍 /info - Узнать о командах\n"
                                      "🆕 /add_project - Добавить новый проект\n"
                                      "📜 /projects - Посмотреть сохраненные проекты\n"
                                      "📚 /help - Получить помощь\n"
                                      "🤔 /about - Узнать больше о боте\n"
                                      "✉️ /contact - Связаться с поддержкой",
                     reply_markup=telebot.types.ReplyKeyboardRemove())


@bot.message_handler(commands=['info'])
def info_command_handler(message: telebot.types.Message):
    """
    Обработчик команды /info.
    Выводит описание доступных команд.
    """
    info_text = (
        "🤖 Доступные команды:\n"
        "/start - Запустить бота и получить приветственное сообщение. 👋\n"
        "/add_project - Добавить новый проект в портфолио. 📝\n"
        "/projects - Посмотреть сохраненные проекты. 📜\n"
        "/help - Получить помощь по использованию бота. ❓\n"
        "/about - Узнать больше о возможностях бота. 📖\n"
        "/contact - Связаться с поддержкой. 📞\n"
        "💡 Нажмите на команду, чтобы узнать больше!"
    )
    bot.send_message(message.chat.id, info_text)


@bot.message_handler(commands=['add_project'])
def add_project_handler(message: telebot.types.Message):
    """
    Обработчик команды /add_project.
    Запрашивает у пользователя описание проекта.
    """
    bot.send_message(message.chat.id, "📝 Пожалуйста, введите описание вашего проекта:\n"
                                      "🌐 Поделитесь, чем он уникален и какие технологии использованы!")
    bot.register_next_step_handler(message, save_project)


def save_project(message: telebot.types.Message):
    """
    Сохраняет введенное описание проекта в список проектов.
    """
    project_description = message.text
    projects.append(project_description)
    bot.send_message(message.chat.id, f"✅ Ваш проект был добавлен: {project_description}\n"
                                      "Теперь вы можете увидеть все свои проекты с помощью команды /projects.")


@bot.message_handler(commands=['projects'])
def projects_command_handler(message: telebot.types.Message):
    """
    Обработчик команды /projects.
    Отправляет пользователю список всех сохраненных проектов.
    """
    if projects:
        project_list = "📜 Вот ваши проекты:\n" + "\n".join(f"• {project}" for project in projects)
    else:
        project_list = "🔍 У вас пока нет сохраненных проектов. Добавьте их с помощью команды /add_project."

    bot.send_message(message.chat.id, project_list)


@bot.message_handler(commands=['help'])
def help_command_handler(message: telebot.types.Message):
    """
    Обработчик команды /help.
    Предоставляет информацию о помощи.
    """
    bot.send_message(message.chat.id, "❓ Если у вас возникли вопросы, пожалуйста, свяжитесь с поддержкой.\n"
                                      "💬 Мы всегда рады помочь!\n"
                                      "📧 Напишите на нашу почту: support@example.com")


@bot.message_handler(commands=['about'])
def about_command_handler(message: telebot.types.Message):
    """
    Обработчик команды /about.
    Информация о боте.
    """
    bot.send_message(message.chat.id, "🤖 Этот бот создан для управления проектами.\n"
                                      "🌟 Он поможет вам отслеживать ваши работы и делиться ими с другими!\n"
                                      "🚀 Разработан с любовью для пользователей!")


@bot.message_handler(commands=['contact'])
def contact_command_handler(message: telebot.types.Message):
    """
    Обработчик команды /contact.
    Предоставляет информацию для связи.
    """
    bot.send_message(message.chat.id, "📞 Свяжитесь с нами через:\n"
                                      "✉️ Email: support@example.com\n"
                                      "💬 Telegram: @support_bot\n"
                                      "📱 Или просто напишите в чат!")


@bot.message_handler(func=lambda message: True)
def echo_message(message: telebot.types.Message):
    """
    Обработчик для всех остальных сообщений.
    Отправляет обратно то, что пользователь написал.
    """
    bot.send_message(message.chat.id, "🗨️ Вы написали: " + message.text + "\n"
                                                                          "🤔 Если у вас есть вопросы, напишите /help!")


if __name__ == '__main__':
    bot.polling(none_stop=True)
