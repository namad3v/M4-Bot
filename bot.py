"""Simple Telegram bot — commands: /start /help /ping /id"""

import logging
import os

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)

# Your group link
GROUP_LINK = "https://t.me/+bw4LZHxtgdZmZjA1"


def load_token() -> str:
    """Read TELEGRAM_BOT_TOKEN from environment, falling back to .env file."""

    token = os.getenv("TELEGRAM_BOT_TOKEN")

    if not token:
        env_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            ".env",
        )

        if os.path.exists(env_path):
            with open(env_path, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()

                    if line and not line.startswith("#") and "=" in line:
                        key, value = line.split("=", 1)

                        os.environ.setdefault(
                            key.strip(),
                            value.strip().strip('"').strip("'"),
                        )

            token = os.getenv("TELEGRAM_BOT_TOKEN")

    if not token or "paste" in token.lower():
        raise SystemExit(
            "❌ TELEGRAM_BOT_TOKEN not found.\n"
            "Add your bot token to the TELEGRAM_BOT_TOKEN environment variable."
        )

    return token


# =========================
# START
# =========================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:

    user = update.effective_user

    keyboard = [
        [
            InlineKeyboardButton("🆘 Help", callback_data="help"),
            InlineKeyboardButton("🏓 Ping", callback_data="ping"),
        ],
        [
            InlineKeyboardButton("🆔 My ID", callback_data="id"),
            InlineKeyboardButton("👥 Group", url=GROUP_LINK),
        ],
        [
            InlineKeyboardButton("⚙️ Others", callback_data="others"),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"👋 Hi {user.first_name}!\n\n"
        "🤖 I'm online.\n"
        "Choose an option below 👇",
        reply_markup=reply_markup,
    )


# =========================
# HELP
# =========================

async def help_cmd(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:

    await update.message.reply_text(
        "📚 Available Commands:\n\n"
        "▶️ /start — Start the bot\n"
        "🆘 /help — Show help\n"
        "🏓 /ping — Check bot status\n"
        "🆔 /id — Show your Telegram ID"
    )


# =========================
# PING
# =========================

async def ping(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:

    await update.message.reply_text(
        "🏓 Pong!\n"
        "🤖 Bot is online ✅"
    )


# =========================
# ID
# =========================

async def id_cmd(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:

    user = update.effective_user

    await update.message.reply_text(
        f"🆔 Your Telegram ID:\n\n"
        f"`{user.id}`",
        parse_mode="Markdown",
    )


# =========================
# BUTTON HANDLER
# =========================

async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:

    query = update.callback_query

    await query.answer()

    if query.data == "help":

        await query.message.reply_text(
            "📚 Available Commands:\n\n"
            "▶️ /start — Start the bot\n"
            "🆘 /help — Show help\n"
            "🏓 /ping — Check bot status\n"
            "🆔 /id — Show your Telegram ID"
        )

    elif query.data == "ping":

        await query.message.reply_text(
            "🏓 Pong!\n"
            "🤖 Bot is online ✅"
        )

    elif query.data == "id":

        await query.message.reply_text(
            f"🆔 Your Telegram ID:\n\n"
            f"`{query.from_user.id}`",
            parse_mode="Markdown",
        )

    elif query.data == "others":

        await query.message.reply_text(
            "🛠️ This command is under construction."
        )


# =========================
# MAIN
# =========================

def main() -> None:

    token = load_token()

    app = Application.builder().token(token).build()

    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CommandHandler("id", id_cmd))

    # Inline buttons
    app.add_handler(CallbackQueryHandler(button_handler))

    logger.info("🤖 Bot starting...")

    app.run_polling(
        allowed_updates=Update.ALL_TYPES
    )


if __name__ == "__main__":
    main()
