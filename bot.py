import os
import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes,
)

from config import BOT_TOKEN, DOWNLOAD_PATH
from downloader import download_video, download_audio

logging.basicConfig(
    format="%(asctime)s - %(name)s -  %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello could you please send me YouTube video link?"
    )


async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    if "youtube.com" not in url and "youtu.be" not in url:
        await update.message.reply_text("Please send me a valid YouTube video link.")
        return

    context.user_data["url"] = url
    keyboard = [
        [
            InlineKeyboardButton("🎬 video (MP3)", callback_data="video"),
            InlineKeyboardButton("🎵 audio (MP3) ", callback_data="audio"),

        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "What format do you want?",
        reply_markup=reply_markup,
    )


async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    url = context.user_data.get("url")
    if not url:
        await query.edit_message_text("The link wasn't found! please send the link again.")
        return

    choice = query.data
    await query.edit_message_text("Downloading.... please wait.")

    filepath = None
    try:
        if choice == "video":
            filepath = download_video(url)
            with open(filepath, "rb") as f:
                await context.bot.send_video(
                    chat_id=query.message.chat_id,
                    audio=f,
                    read_timeout=120,
                    write_timeout=120,
                )
        elif choice == "audio":
            filepath = download_audio(url)
            with open(filepath, "rb") as f:
                await context.bot.send_audio(
                    chat_id=query.message.chat_id,
                    audio=f,
                    read_timeout=120,
                    write_timeout=120,
                )
        else:
            await query.edit_message_text("The option was invalid.")
            return

        await query.edit_message_text("Finished!")

    except Exception as e:
        logger.exception("Download/send faild")
        await query.edit_message_text(f'Download faild : {e}')

    finally:
        if filepath and os.path.exists(filepath):
            try:
                os.remove(filepath)
            except OSError:
                pass
        context.user_data.pop("url , None")


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, handle_link))
    app.add_handler(CallbackQueryHandler(handle_button))

    logger.info("Bot is starting....")
    app.run_pollig()


if __name__ == "__main__":
    main()
