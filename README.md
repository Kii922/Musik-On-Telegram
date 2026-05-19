🎵 Telegram VC Music Userbot

Bot Telegram Music Player menggunakan Pyrogram + PyTgCalls untuk memutar musik di Voice Chat Telegram Group.

Support:

▶️ Play Musik dari YouTube
📜 Queue System
🎵 Now Playing
📊 Progress Bar Auto Update
⏭ Auto Next Song
🚪 Auto Leave VC saat queue kosong
🐳 Docker Support
⚡ 24/7 Ready
🚀 Features
.join → Join Voice Chat
.play <judul lagu> → Putar musik
.queue → Lihat daftar queue
.nowplaying → Lihat lagu yang sedang diputar
Auto next song
Auto update progress bar tiap 5 detik
Auto keluar VC saat queue habis
📦 Requirements
Python 3.10+
FFmpeg
Telegram API ID & API HASH
🔧 Installation
1. Clone Repository
git clone https://github.com/USERNAME/REPO.git
cd REPO
2. Install FFmpeg
Ubuntu / Linux Mint
sudo apt update
sudo apt install ffmpeg -y
3. Buat Virtual Environment
python3 -m venv venv

Aktifkan venv:

source venv/bin/activate
4. Install Dependencies
pip install -r requirements.txt
📝 Setup .env

Buat file .env

API_ID=123456
API_HASH=xxxxxxxxxxxxxxxx

Ambil API:
👉 https://my.telegram.org

▶️ Run Bot
python main.py
🎮 Commands
Join VC
.join

Bot akan join ke Voice Chat group.

Play Music
.play faded alan walker
Queue List
.queue
Now Playing
.nowplaying
🐳 Docker Installation
Build Docker
sudo docker compose up -d --build
Cek Logs
sudo docker compose logs -f
📁 Project Structure
.
├── main.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env
├── temp/
└── session/
📄 requirements.txt
pyrogram
tgcrypto
python-dotenv
yt-dlp
py-tgcalls==1.2.9
ntgcalls==1.1.2
🐳 docker-compose.yml
services:
  userbot:
    build: .
    container_name: telegram_userbot
    restart: unless-stopped

    env_file:
      - .env

    volumes:
      - ./temp:/app/temp
      - ./session:/app/session
🐋 Dockerfile
FROM python:3.10

WORKDIR /app

RUN apt update && apt install -y ffmpeg

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
⚠️ Notes
Pastikan Voice Chat group aktif
Akun Telegram harus bisa join VC
Jangan spam command .play
Folder temp/ digunakan untuk menyimpan audio sementara
