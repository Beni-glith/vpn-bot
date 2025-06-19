import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import subprocess
import sqlite3
import random
import string

# === GANTI DENGAN TOKEN BOT KAMU ===
TOKEN = '8075337049:AAH5neurIntnSNBFHIHD535d19CEw22eWOo'
bot = telebot.TeleBot(TOKEN)

# === FUNGSI GENERATE USERNAME ===
def generate_username(length=6):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

# === MENU UTAMA ===
@bot.message_handler(commands=['start'])
def handle_start(message):
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("📦 CREATE ACCOUNT", callback_data="create_menu"),
        InlineKeyboardButton("👤 AKUN SAYA", callback_data="akun_saya")
    )
    bot.send_message(message.chat.id, "Selamat datang di *KACER VPN BOT* 🐦\nSilakan pilih menu di bawah ini:", parse_mode="Markdown", reply_markup=markup)

# === MENU CREATE AKUN ===
@bot.callback_query_handler(func=lambda call: call.data == "create_menu")
def handle_create_menu(call):
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("🌐 SSH", callback_data="create_ssh")
    )
    markup.row(
        InlineKeyboardButton("⬅️ KEMBALI", callback_data="main_menu")
    )
    bot.edit_message_text("Pilih jenis akun yang ingin dibuat:", call.message.chat.id, call.message.message_id, reply_markup=markup)

# === KEMBALI KE MENU UTAMA ===
@bot.callback_query_handler(func=lambda call: call.data == "main_menu")
def handle_back_menu(call):
    handle_start(call.message)

# === HANDLE BUAT AKUN SSH ===
@bot.callback_query_handler(func=lambda call: call.data == "create_ssh")
def handle_create_ssh(call):
    telegram_id = call.from_user.id
    username = generate_username()
    hari_aktif = 3

    try:
        result = subprocess.run(
            ["sudo", "/usr/local/bin/addsshws.sh", username, str(hari_aktif)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode == 0:
            output = result.stdout.strip()

            # Ambil tanggal expired
            for line in output.split('\n'):
                if "Expired:" in line:
                    expired = line.split("Expired:")[1].strip()
                    break
            else:
                expired = None

            # Simpan log ke database
            conn = sqlite3.connect('vpn.db')
            c = conn.cursor()
            c.execute("INSERT INTO ssh_accounts (telegram_id, username, expired) VALUES (?, ?, ?)",
                      (telegram_id, username, expired))
            conn.commit()
            conn.close()

            bot.send_message(call.message.chat.id, f"✅ Akun SSH berhasil dibuat:\n\n{output}")
        else:
            bot.send_message(call.message.chat.id, f"❌ Gagal membuat akun SSH:\n{result.stderr.strip()}")
    except Exception as e:
        bot.send_message(call.message.chat.id, f"⚠️ Terjadi kesalahan:\n{str(e)}")

# === CEK AKUN SAYA ===
@bot.message_handler(commands=['akun_saya'])
def cek_akun_saya(message):
    telegram_id = message.from_user.id
    conn = sqlite3.connect('vpn.db')
    c = conn.cursor()
    c.execute("SELECT username, expired, created_at FROM ssh_accounts WHERE telegram_id = ? ORDER BY created_at DESC", (telegram_id,))
    akun = c.fetchall()
    conn.close()

    if not akun:
        bot.send_message(message.chat.id, "📂 Kamu belum pernah membuat akun SSH.")
        return

    msg = "📋 Berikut akun SSH yang pernah kamu buat:\n"
    for idx, (username, expired, created_at) in enumerate(akun, 1):
        msg += f"\n{idx}. 👤 *{username}*\n   📅 Expired: `{expired}`\n   🕒 Dibuat: `{created_at}`\n"

    bot.send_message(message.chat.id, msg, parse_mode="Markdown")

# === CEK AKUN SAYA VIA CALLBACK ===
@bot.callback_query_handler(func=lambda call: call.data == "akun_saya")
def handle_akun_saya_cb(call):
    cek_akun_saya(call.message)

# === JALANKAN BOT ===
print("🤖 Bot sedang berjalan...")
bot.infinity_polling()
