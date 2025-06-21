from telegram import Update
from telegram.ext import ContextTypes
from services.ssh_ws import create_ssh_account

async def order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    result = create_ssh_account(user_id)
    await update.message.reply_text(f"Akun SSH/WS berhasil dibuat:\n\n{result}")
