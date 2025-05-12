import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext
from config import TELEGRAM_BOT_TOKEN, DOWNLOADS_FOLDER
from utils.downloader import download_youtube, download_tiktok, download_instagram, download_facebook
from utils.helpers import setup_logger, handle_error

logger = setup_logger()

# Handler untuk perintah /start
def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("YouTube", callback_data='youtube')],
        [InlineKeyboardButton("TikTok", callback_data='tiktok')],
        [InlineKeyboardButton("Instagram", callback_data='instagram')],
        [InlineKeyboardButton("Facebook", callback_data='facebook')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Pilih platform untuk mendownload:', reply_markup=reply_markup)

# Handler untuk tombol menu
def button_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    platform = query.data
    context.user_data['platform'] = platform
    query.edit_message_text(text=f"Silakan kirim link {platform.capitalize()} untuk didownload.")

# Handler untuk mendownload media
def download_media(update: Update, context: CallbackContext) -> None:
    url = update.message.text
    platform = context.user_data.get('platform')

    if not platform:
        update.message.reply_text("Silakan pilih platform terlebih dahulu menggunakan /start.")
        return

    try:
        if platform == 'youtube':
            file_path = download_youtube(url, DOWNLOADS_FOLDER)
            with open(file_path, 'rb') as audio:
                update.message.reply_audio(audio)
        elif platform == 'tiktok':
            file_path = download_tiktok(url, DOWNLOADS_FOLDER)
            with open(file_path, 'rb') as video:
                update.message.reply_video(video)
        elif platform == 'instagram':
            download_instagram(url, DOWNLOADS_FOLDER)
            update.message.reply_text("Download berhasil!")
        elif platform == 'facebook':
            file_path = download_facebook(url, DOWNLOADS_FOLDER)
            with open(file_path, 'rb') as video:
                update.message.reply_video(video)
    except Exception as e:
        handle_error(update, context, str(e))
    finally:
        cleanup_files(DOWNLOADS_FOLDER)

# Membersihkan file sementara
def cleanup_files(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            logger.error(f"Error cleaning up files: {str(e)}")

# Main Function
def main() -> None:
    updater = Updater(TELEGRAM_BOT_TOKEN)
    dispatcher = updater.dispatcher

    # Handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(button_handler))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, download_media))

    # Mulai bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
