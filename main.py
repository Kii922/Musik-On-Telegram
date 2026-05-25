from pyrogram import Client, filters, idle
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped, HighQualityAudio
from yt_dlp import YoutubeDL
from dotenv import load_dotenv
import os
import time
import asyncio

def format_time(sec):
    m = sec // 60
    s = sec % 60
    return f"{m}:{s:02d}"

load_dotenv()

# =====================
# INIT
# =====================
app = Client(
    "session/userbot",
    api_id=int(os.getenv("API_ID")),
    api_hash=os.getenv("API_HASH")
)

call_py = PyTgCalls(app)

queue = {}
playing = {}
current = {}
start_time = {}
duration = {}
lock = {}
search_cache = {}
nowplaying_msg = {}

# =====================
# PLAY NEXT
# =====================
async def play_next(chat_id):

    if lock.get(chat_id):
        return

    lock[chat_id] = True

    try:

        if chat_id in queue and len(queue[chat_id]) > 0:

            next_song = queue[chat_id].pop(0)

            current[chat_id] = next_song["title"]
            start_time[chat_id] = time.time()
            duration[chat_id] = next_song["duration"]

            await call_py.change_stream(
                chat_id,
                AudioPiped(
                    next_song["file"],
                    HighQualityAudio()
                )
            )

        else:

            playing[chat_id] = False
            current.pop(chat_id, None)

            try:
                await call_py.leave_group_call(chat_id)
            except:
                pass

    except Exception as e:
        print(f"play_next error: {e}")

    finally:
        lock[chat_id] = False

# =====================
# STREAM END
# =====================
@call_py.on_stream_end()
async def on_end(_, update):
    chat_id = getattr(update, "chat_id", None)
    if chat_id:
        await play_next(chat_id)


# =====================
# PING
# =====================
@app.on_message(filters.group & filters.command("ping", prefixes="."))
def ping(client, message):
    message.reply("Pong!")

# =====================
# JOIN
# =====================
@app.on_message(filters.group & filters.command("join", prefixes="."))
async def join_vc(client, message):

    chat_id = message.chat.id

    try:
        await call_py.join_group_call(
            chat_id,
            AudioPiped("temp/sample.mp3", HighQualityAudio())
        )

        await message.reply("✅ Berhasil join VC")

    except Exception as e:
        await message.reply(f"❌ Error join VC:\n{e}")

# =====================
# PLAY
# =====================
@app.on_message(filters.group & filters.command("play", prefixes="."))
async def play(client, message):

    if len(message.command) < 2:
        await message.reply("Contoh: .play faded")
        return

    chat_id = message.chat.id
    arg = " ".join(message.command[1:])

    msg = await message.reply("🔍 Memproses...")

    # =====================
    # PLAY DARI HASIL SEARCH
    # =====================
    if arg.isdigit():

        index = int(arg) - 1

        if chat_id not in search_cache:
            await msg.edit("❌ Belum ada hasil pencarian")
            return

        results = search_cache[chat_id]

        if index < 0 or index >= len(results):
            await msg.edit("❌ Nomor tidak valid")
            return

        query = results[index]["webpage_url"]

    else:
        query = f"ytsearch1:{arg}"

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "temp/%(title)s.%(ext)s",
        "quiet": True,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192"
        }]
    }

    with YoutubeDL(ydl_opts) as ydl:

        info = ydl.extract_info(
            query,
            download=True
        )

        if "entries" in info:
            video = info["entries"][0]
        else:
            video = info

        title = video["title"]
        duration_sec = video.get("duration", 0)

        filename = ydl.prepare_filename(video)
        mp3_file = os.path.splitext(filename)[0] + ".mp3"

    song_data = {
        "title": title,
        "file": mp3_file,
        "duration": duration_sec
    }

    if chat_id not in queue:
        queue[chat_id] = []

    # Belum ada lagu yang diputar
    if not playing.get(chat_id, False):

        playing[chat_id] = True

        current[chat_id] = title
        start_time[chat_id] = time.time()
        duration[chat_id] = duration_sec

        await call_py.change_stream(
            chat_id,
            AudioPiped(
                mp3_file,
                HighQualityAudio()
            )
        )

        await msg.edit(f"🎵 Now Playing\n\n{title}")

        nowplaying_msg[chat_id] = msg

        asyncio.create_task(
            auto_update_progress(chat_id, client)
        )

    # Masuk queue
    else:

        queue[chat_id].append(song_data)

        await msg.edit(
            f"➕ Masuk Queue\n\n"
            f"{title}\n"
            f"Posisi: {len(queue[chat_id])}"
        )

# =====================
# SEARCH
# =====================
@app.on_message(filters.group & filters.command("search", prefixes="."))
async def search_music(client, message):

    if len(message.command) < 2:
        return await message.reply(
            "Contoh:\n.search alan walker"
        )

    query = " ".join(message.command[1:])

    msg = await message.reply("🔍 Searching...")

    with YoutubeDL({"quiet": True}) as ydl:

        result = ydl.extract_info(
            f"ytsearch5:{query}",
            download=False
        )

    videos = result["entries"]

    search_cache[message.chat.id] = videos

    text = "🎵 Hasil Pencarian\n\n"

    for i, video in enumerate(videos, start=1):

        dur = video.get("duration", 0)

        m = dur // 60
        s = dur % 60

        text += (
            f"{i}. {video['title']}\n"
            f"⏱ {m}:{s:02d}\n\n"
        )

    text += "Gunakan:\n.play 1-5"

    await msg.edit(text)

# =====================
# QUEUE
# =====================
@app.on_message(filters.group & filters.command("queue", prefixes="."))
async def show_queue(client, message):

    chat_id = message.chat.id

    if chat_id not in queue or len(queue[chat_id]) == 0:
        await message.reply("📭 Queue kosong")
        return

    text = "📜 Queue:\n\n"

    for i, song in enumerate(queue[chat_id], start=1):
        text += f"{i}. {song['title']}\n"

    await message.reply(text)


# =====================
# NOW PLAYING (basic)
# =====================
@app.on_message(filters.group & filters.command("nowplaying", prefixes="."))
async def now_playing(client, message):

    chat_id = message.chat.id

    if chat_id not in current:
        await message.reply("❌ Tidak ada lagu yang sedang diputar")
        return

    elapsed = int(time.time() - start_time.get(chat_id, 0))
    total = duration.get(chat_id, 0)

    bar_len = 12
    if total > 0:
        filled = int((elapsed / total) * bar_len)
    else:
        filled = 0

    bar = "█" * filled + "░" * (bar_len - filled)

    text = f"""🎵 Now Playing:
{current[chat_id]}

[{bar}] {format_time(elapsed)} / {format_time(total)}
"""

    await message.reply(text)

# =====================
# STOP
# =====================
@app.on_message(filters.group & filters.command("stop", prefixes="."))
async def stop_music(client, message):

    chat_id = message.chat.id

    # hapus semua file queue
    for song in queue.get(chat_id, []):
        try:
            os.remove(song["file"])
        except:
            pass

    queue[chat_id] = []
    playing[chat_id] = False

current.pop(chat_id, None)

    try:
        await call_py.leave_group_call(chat_id)
    except:
        pass

    await message.reply("⏹ Music stopped")

# =====================
# AUTO UPDATE NOW PLAYING
# =====================
async def auto_update_progress(chat_id, client):
    while chat_id in current:

        if chat_id not in start_time or chat_id not in duration:
            await asyncio.sleep(5)
            continue

        elapsed = int(time.time() - start_time[chat_id])
        total = duration.get(chat_id, 0)

        bar_len = 12
        filled = int((elapsed / total) * bar_len) if total > 0 else 0

        bar = "█" * filled + "░" * (bar_len - filled)

        text = f"""🎵 Now Playing:
{current.get(chat_id, '-')}

[{bar}] {format_time(elapsed)} / {format_time(total)}
"""

        try:
            if chat_id in nowplaying_msg:
                await nowplaying_msg[chat_id].edit(text)
        except:
            pass

        await asyncio.sleep(5)
# =====================
# SKIP
# =====================
@app.on_message(filters.group & filters.command("skip", prefixes="."))
async def skip(client, message):

    chat_id = message.chat.id

    if queue.get(chat_id):
        await play_next(chat_id)
        await message.reply("⏭ Lagu dilewati")
    else:
        await message.reply("📭 Queue kosong")
# =====================
# HELP/BANTUAN DAN DAFTAR PERINTAH
# =====================
@app.on_message(filters.group & filters.command("help", prefixes="."))
async def help_cmd(client, message):

    text = """
🎵   DAFTAR PERINTAH

.join
.search <judul>
.play <judul>
.play 1-5
.queue
.nowplaying
.skip
.stop
.ping
"""

    await message.reply(text)

# =====================
# START
# =====================
print("Userbot starting...")

app.start()
call_py.start()

print("BOT RUNNING ✔")

idle()

app.stop()