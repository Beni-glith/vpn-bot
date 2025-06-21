from telegram import Update
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"Selamat datang, {user.first_name}!\n"
        "Ini adalah bot pemesanan akun VPN otomatis.\n\n"
        "Gunakan /menu untuk mulai."
    )
