#!/bin/bash

echo "🔧 Memulai instalasi bot Telegram Auto Order VPN..."

# Update & install dependencies
sudo apt update && sudo apt install -y python3 python3-pip git curl

# Buat direktori kerja
BOT_DIR="vpn_bot"
if [ ! -d "$BOT_DIR" ]; then
    git clone https://github.com/Beni-glith/vpn-bot.git "$BOT_DIR" || mkdir "$BOT_DIR"
fi
cd "$BOT_DIR" || exit

# Buat struktur folder jika belum ada
mkdir -p handlers services scripts data

# Install python-telegram-bot
pip3 install -r requirements.txt || pip3 install python-telegram-bot==20.7

# Izin eksekusi untuk bash script SSH/WS
chmod +x scripts/create_ssh_ws.sh

# Buat file logs & users jika belum ada
touch data/users.json data/logs.txt

# Info selesai
echo "✅ Instalasi selesai!"
echo "📁 Direktori bot: $BOT_DIR"
echo "🚀 Jalankan bot dengan: python3 bot.py"
