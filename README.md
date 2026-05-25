# 🎵 TELEGRAM UBOT MUSIK

Bot Telegram Music Player menggunakan Pyrogram + PyTgCalls untuk memutar musik di Voice Chat Telegram Group.

## ✨ Features

* ▶️ Play Musik dari YouTube
* 📜 Queue System
* 🎵 Now Playing
* 📊 Progress Bar Auto Update
* ⏭ Auto Next Song
* 🚪 Auto Leave VC saat queue kosong
* 🐳 Docker Support
* ⚡ 24/7 Ready

---

# 📦 Requirements

* Python 3.10+
* FFmpeg
* Telegram API ID & API HASH

---

# 🚀 Installation

## 1. Clone Repository

```bash
git clone https://github.com/Kii922/Musik-On-Telegram.git
cd REPO
```

---

## 2. Install FFmpeg

### Ubuntu

```bash
sudo apt update
sudo apt install ffmpeg -y
```

---

## 3. Buat Virtual Environment

```bash
python3 -m venv venv
```

Aktifkan venv:

```bash
source venv/bin/activate
```

---

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 📝 Setup .env

Buat file `.env`

```env
API_ID=123456
API_HASH=xxxxxxxxxxxxxxxx
```

Ambil API:
https://my.telegram.org

---

# ▶️ Run Bot

```bash
python main.py
```

---

# 🎮 Commands

## Join Voice Chat

```bash
.join
```

Bot akan join ke Voice Chat group.

---

## Play Music

```bash
.play
```

---

## Queue List

```bash
.queue
```

---

## Now Playing

```bash
.nowplaying
```

---

# 🐳 Docker Installation

## Build Docker

```bash
sudo docker compose up -d --build
```

---

## Cek Logs

```bash
sudo docker compose logs -f
```

---

# 📁 Project Structure

```bash
.
├── main.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env
├── temp/
└── session/
```

---

# 📄 requirements.txt

```txt
pyrogram
tgcrypto
python-dotenv
yt-dlp
py-tgcalls==1.2.9
ntgcalls==1.1.2
```

---

# 🐋 Dockerfile

```Dockerfile
FROM python:3.10

WORKDIR /app

RUN apt update && apt install -y ffmpeg

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

---

# 🐳 docker-compose.yml

```yml
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
```

---

# ⚠️ Notes

* Pastikan Voice Chat group aktif
* Akun Telegram harus bisa join VC
* Jangan spam command `.play`
* Folder `temp/` digunakan untuk menyimpan audio sementara

---

# ❤️ Credits

* Pyrogram
* PyTgCalls
* yt-dlp

Developed by **KII**

Thanks for my team @chatgpt

# PROJEK INI MASIH DALAM TAHAP PENGEMBANGAN 
