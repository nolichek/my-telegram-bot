import json
import os
import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Токен вашего бота
TOKEN = "7836181923:AAHjGUphNj9m-yX2OmRlI1uOFSEkSFZyISo"

# Путь к файлу для хранения ссылок
LINKS_FILE = "links.json"

# Инициализация файла JSON, если он не существует
if not os.path.exists(LINKS_FILE):
    with open(LINKS_FILE, "w") as f:
        json.dump({}, f)
    logger.info("Создан новый файл links.json")

# Создаем основную клавиатуру
def get_main_keyboard():
    keyboard = [
        ["😁 ПОДДЕРЖКА"],
        ["👨‍💻 ДАЛЬШЕ"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# Создаем клавиатуру для подменю "ДАЛЬШЕ"
def get_cheats_keyboard():
    keyboard = [
        ["ансофт", "софт"],
        ["назад"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# Создаем клавиатуру для подменю "софт"
def get_software_keyboard():
    keyboard = [
        ["Minecraft java", "Minecraft bedrock"],
        ["назад"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# Создаем клавиатуру для подменю "ансофт"
def get_unsoft_keyboard():
    keyboard = [
        ["ресурс паки"],
        ["назад"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# Создаем клавиатуру для подменю "ресурс паки"
def get_resource_packs_keyboard():
    keyboard = [
        ["Imba RP"],
        ["назад"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# Создаем клавиатуру для подменю "Minecraft java"
def get_minecraft_java_keyboard():
    keyboard = [
        ["чит"],
        ["назад"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# Создаем клавиатуру для подменю "чит"
def get_cheat_version_keyboard():
    keyboard = [
        ["1.16.5"],
        ["назад"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# Создаем клавиатуру для подменю "1.16.5"
def get_cheat_selection_keyboard():
    keyboard = [
        ["Wexside", "britvafarm", "Nursultan crack"],
        ["dimasikclient", "Delta Crack", "Haruka(loader)"],
        ["rocstar free", "назад"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# Команда /start
async def start(update: Update, context):
    logger.info("Команда /start от пользователя %s", update.message.from_user.username)
    context.user_data['menu_state'] = 'main'  # Устанавливаем начальное состояние меню
    await update.message.reply_text(
        "Привет! я бот у которого ты можешь найти разные читы, рп,кфг, и все что надо для тебя\n"
        "Выбери действие из меню ниже:",
        reply_markup=get_main_keyboard()
    )

# Команда /addlink
async def add_link(update: Update, context):
    args = context.args
    if len(args) < 2:
        await update.message.reply_text("Пожалуйста, укажите ссылку и описание: /addlink <URL> <описание>")
        return

    url = args[0]
    description = " ".join(args[1:])

    if not (url.startswith("http://") or url.startswith("https://")):
        await update.message.reply_text("Пожалуйста, укажите корректную ссылку (начинается с http:// или https://)")
        return

    try:
        with open(LINKS_FILE, "r") as f:
            data = json.load(f)
    except Exception as e:
        logger.error("Ошибка чтения файла links.json: %s", e)
        data = {}

    if "Без категории" not in data:
        data["Без категории"] = []
    data["Без категории"].append({"url": url, "description": description})

    with open(LINKS_FILE, "w") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    logger.info("Добавлена ссылка: %s - %s", description, url)

    context.user_data['menu_state'] = 'main'  # Возвращаем в главное меню после команды
    await update.message.reply_text(f"Ссылка добавлена: {description} ({url})", reply_markup=get_main_keyboard())

# Команда /addlinkcategory
async def add_link_category(update: Update, context):
    args = context.args
    if len(args) < 3:
        await update.message.reply_text("Пожалуйста, укажите категорию, ссылку и описание: /addlinkcategory <категория> <URL> <описание>")
        return

    category = args[0]
    url = args[1]
    description = " ".join(args[2:])

    if not (url.startswith("http://") or url.startswith("https://")):
        await update.message.reply_text("Пожалуйста, укажите корректную ссылку (начинается с http:// или https://)")
        return

    try:
        with open(LINKS_FILE, "r") as f:
            data = json.load(f)
    except Exception as e:
        logger.error("Ошибка чтения файла links.json: %s", e)
        data = {}

    if category not in data:
        data[category] = []
    data[category].append({"url": url, "description": description})

    with open(LINKS_FILE, "w") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    logger.info("Добавлена ссылка в категорию %s: %s - %s", category, description, url)

    context.user_data['menu_state'] = 'main'  # Возвращаем в главное меню после команды
    await update.message.reply_text(
        f"Ссылка добавлена в категорию {category}: {description} ({url})",
        reply_markup=get_main_keyboard()
    )

# Команда /getlinks
async def get_links(update: Update, context):
    try:
        with open(LINKS_FILE, "r") as f:
            data = json.load(f)
        
        if not data:
            await update.message.reply_text("Ссылок пока нет. Добавьте с помощью /addlink или /addlinkcategory.")
            return

        response = "Список ссылок по категориям:\n"
        for category, links in data.items():
            response += f"\n{category}:\n"
            for i, link in enumerate(links, 1):
                response += f"  {i}. {link['description']}: {link['url']}\n"
        
        context.user_data['menu_state'] = 'main'  # Возвращаем в главное меню после команды
        await update.message.reply_text(response, reply_markup=get_main_keyboard())
    except Exception as e:
        logger.error("Ошибка при получении ссылок: %s", e)
        await update.message.reply_text("Ошибка при получении ссылок. Попробуйте позже.")

# Обработчик нажатий на кнопки
async def handle_buttons(update: Update, context):
    text = update.message.text
    try:
        with open(LINKS_FILE, "r") as f:
            data = json.load(f)
    except Exception as e:
        logger.error("Ошибка чтения файла links.json: %s", e)
        data = {}

    if text == "😁 ПОДДЕРЖКА":
        context.user_data['menu_state'] = 'main'
        await update.message.reply_text("Свяжитесь с поддержкой: @Kapriz002")
    elif text == "👨‍💻 ДАЛЬШЕ":
        context.user_data['menu_state'] = 'cheats'
        await update.message.reply_text("Выберите раздел", reply_markup=get_cheats_keyboard())
    elif text == "ансофт":
        context.user_data['menu_state'] = 'unsoft'
        await update.message.reply_text("Выберите ресурс пак", reply_markup=get_unsoft_keyboard())
    elif text == "софт":
        context.user_data['menu_state'] = 'software'
        await update.message.reply_text("Выберите раздел", reply_markup=get_software_keyboard())
    elif text == "ресурс паки":
        context.user_data['menu_state'] = 'resource_packs'
        await update.message.reply_text("Выберите ресурс пак", reply_markup=get_resource_packs_keyboard())
    elif text == "Imba RP":
        context.user_data['menu_state'] = 'resource_packs'
        await update.message.reply_text(
            "Imba RP: https://drive.google.com/uc?export=download&id=10JS9wnawD0A2ZUxd78x1VqukQqZUCtE2\n"
            "Пароль от архива: 123",
            reply_markup=get_resource_packs_keyboard()
        )
    elif text == "Minecraft java":
        context.user_data['menu_state'] = 'minecraft_java'
        await update.message.reply_text("Выберите", reply_markup=get_minecraft_java_keyboard())
    elif text == "Minecraft bedrock":
        context.user_data['menu_state'] = 'software'
        await update.message.reply_text(
            "Minecraft Bedrock: https://tooldroid-poggers.neocities.org/",
            reply_markup=get_software_keyboard()
        )
    elif text == "чит":
        context.user_data['menu_state'] = 'cheat_version'
        await update.message.reply_text("Выберите версию", reply_markup=get_cheat_version_keyboard())
    elif text == "1.16.5":
        context.user_data['menu_state'] = 'cheat_selection'
        await update.message.reply_text("Выберите чит", reply_markup=get_cheat_selection_keyboard())
    elif text == "Wexside":
        context.user_data['menu_state'] = 'cheat_selection'
        await update.message.reply_text(
            "Wexside: https://workupload.com/file/9St57j4Jqn6\nПароль от архива: 123",
            reply_markup=get_cheat_selection_keyboard()
        )
    elif text == "britvafarm":
        context.user_data['menu_state'] = 'cheat_selection'
        await update.message.reply_text(
            "britvafarm: https://workupload.com/file/E9dZkBkNHJL",
            reply_markup=get_cheat_selection_keyboard()
        )
    elif text == "dimasikclient":
        context.user_data['menu_state'] = 'cheat_selection'
        await update.message.reply_text(
            "dimasikclient: https://workupload.com/file/VtTKTYQgzLR",
            reply_markup=get_cheat_selection_keyboard()
        )
    elif text == "Delta Crack":
        context.user_data['menu_state'] = 'cheat_selection'
        await update.message.reply_text(
            "Delta Crack: https://drive.google.com/uc?export=download&id=1zCVaGxIOht9vEt3QbVNLPOMygVMWIdOE\nПароль от архива: 123",
            reply_markup=get_cheat_selection_keyboard()
        )
    elif text == "Nursultan crack":
        context.user_data['menu_state'] = 'cheat_selection'
        await update.message.reply_text(
            "Nursultan crack: https://drive.google.com/open?id=1Zo7ozkhhpCRUFtFek4sVFj1YV_is2C_q&usp=drive_copy",
            reply_markup=get_cheat_selection_keyboard()
        )
    elif text == "Haruka(loader)":
        context.user_data['menu_state'] = 'cheat_selection'
        await update.message.reply_text(
            "Haruka(loader): https://drive.google.com/open?id=1laKZlzuGsfdTKuEFJ-D1lq2iaGJ8xByi&usp=drive_copy",
            reply_markup=get_cheat_selection_keyboard()
        )
    elif text == "rocstar free":
        context.user_data['menu_state'] = 'cheat_selection'
        await update.message.reply_text(
            "rocstar free: https://drive.google.com/open?id=16PRyvkjfIUB_5SEA1ffH5gM1hYSKW5Jp&usp=drive_copy",
            reply_markup=get_cheat_selection_keyboard()
        )
    elif text == "назад":
        current_state = context.user_data.get('menu_state', 'main')
        if current_state == 'cheats':
            context.user_data['menu_state'] = 'main'
            await update.message.reply_text("Вернулись в главное меню.", reply_markup=get_main_keyboard())
        elif current_state == 'software':
            context.user_data['menu_state'] = 'cheats'
            await update.message.reply_text("Вернулись назад.", reply_markup=get_cheats_keyboard())
        elif current_state == 'unsoft':
            context.user_data['menu_state'] = 'cheats'
            await update.message.reply_text("Вернулись назад.", reply_markup=get_cheats_keyboard())
        elif current_state == 'resource_packs':
            context.user_data['menu_state'] = 'unsoft'
            await update.message.reply_text("Вернулись назад.", reply_markup=get_unsoft_keyboard())
        elif current_state == 'minecraft_java':
            context.user_data['menu_state'] = 'software'
            await update.message.reply_text("Вернулись назад.", reply_markup=get_software_keyboard())
        elif current_state == 'cheat_version':
            context.user_data['menu_state'] = 'minecraft_java'
            await update.message.reply_text("Вернулись назад.", reply_markup=get_minecraft_java_keyboard())
        elif current_state == 'cheat_selection':
            context.user_data['menu_state'] = 'cheat_version'
            await update.message.reply_text("Вернулись назад.", reply_markup=get_cheat_version_keyboard())
        else:
            context.user_data['menu_state'] = 'main'
            await update.message.reply_text("Вернулись в главное меню.", reply_markup=get_main_keyboard())
    else:
        context.user_data['menu_state'] = 'main'
        await update.message.reply_text("Неизвестная команда. Выберите действие из меню.", reply_markup=get_main_keyboard())

# Обработка неизвестных команд
async def unknown(update: Update, context):
    context.user_data['menu_state'] = 'main'
    await update.message.reply_text("Извините, такая команда не найдена. Выберите действие из меню.", reply_markup=get_main_keyboard())

def main():
    # Создаем приложение
    try:
        application = Application.builder().token(TOKEN).build()
        logger.info("Бот успешно инициализирован")
    except Exception as e:
        logger.error("Ошибка инициализации бота: %s", e)
        return

    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("addlink", add_link))
    application.add_handler(CommandHandler("addlinkcategory", add_link_category))
    application.add_handler(CommandHandler("getlinks", get_links))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons))
    application.add_handler(MessageHandler(filters.COMMAND, unknown))

    # Запускаем бота
    try:
        application.run_polling()
    except Exception as e:
        logger.error("Ошибка при запуске бота: %s", e)

if __name__ == "__main__":
    main()