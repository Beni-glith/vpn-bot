from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["🔐 Produk", "🛒 Beli Akun"],
        ["📊 Cek Akun", "📞 Bantuan"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Pilih menu:", reply_markup=reply_markup)
