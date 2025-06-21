from telegram.ext import ApplicationBuilder, CommandHandler
from handlers.start import start
from handlers.menu import show_menu
from handlers.order import order
from handlers.check_account import check_account
from handlers.help import help_command
from config import BOT_TOKEN

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("menu", show_menu))
app.add_handler(CommandHandler("order", order))
app.add_handler(CommandHandler("cek", check_account))
app.add_handler(CommandHandler("help", help_command))

if __name__ == "__main__":
    print("Bot is running...")
    app.run_polling()
