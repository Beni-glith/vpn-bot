#!/bin/bash

BOT_DIR="/opt/vpn-bot"
BOT_FILE="vpn_bot.py"
DB_FILE="vpn.db"
RAW_URL="https://raw.githubusercontent.com/Beni-glith/vpn-bot/main/vpn_bot.py"  # GANTI jika URL bot kamu berbeda

echo "🚀 Memulai instalasi KACER VPN Bot..."

# Update & install dependencies
apt update -y
apt install -y python3 python3-pip sqlite3 curl sudo

# Install Python module
pip3 install pyTelegramBotAPI

# Buat direktori untuk bot
mkdir -p $BOT_DIR
cd $BOT_DIR

# Download file bot
echo "⬇️ Mengunduh file bot dari GitHub..."
curl -sSL "$RAW_URL" -o "$BOT_FILE"

# Buat database jika belum ada
if [ ! -f "$DB_FILE" ]; then
    echo "📂 Membuat database VPN..."
    cat <<EOF | sqlite3 $DB_FILE
CREATE TABLE IF NOT EXISTS ssh_accounts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  telegram_id INTEGER,
  username TEXT,
  expired DATE,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
EOF
fi

# Buat systemd service
echo "⚙️ Membuat service systemd..."
cat > /etc/systemd/system/vpn-bot.service <<EOF
[Unit]
Description=Bot Telegram Auto Order VPN
After=network.target

[Service]
ExecStart=/usr/bin/python3 $BOT_DIR/$BOT_FILE
WorkingDirectory=$BOT_DIR
Restart=always
User=root

[Install]
WantedBy=multi-user.target
EOF

# Aktifkan & mulai service
systemctl daemon-reexec
systemctl daemon-reload
systemctl enable vpn-bot
systemctl restart vpn-bot

echo ""
echo "✅ Bot berhasil diinstal dan dijalankan!"
echo "📌 Lokasi: $BOT_DIR"
echo "🛠️ Kelola service dengan:"
echo "   systemctl restart vpn-bot"
echo "   systemctl status vpn-bot"
echo "   journalctl -fu vpn-bot"
