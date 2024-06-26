import logging
import config
import transcript_service

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Просто отправьте ссылку на видео с Youtube для которого вы хотите получить расшифровку текста")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    url = update.message.text
    result = transcript_service.get_transcript(url)
    await update.message.reply_text(result)


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(config.telegram_bot_token).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", help_command))
    application.add_handler(CommandHandler("help", help_command))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
