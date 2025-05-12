from loguru import logger

def setup_logger():
    logger.add("bot.log", rotation="500 MB", level="INFO")
    return logger

def handle_error(update, context, error_message):
    logger.error(error_message)
    update.message.reply_text("Terjadi kesalahan. Silakan coba lagi nanti.")