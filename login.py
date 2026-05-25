from pyrogram import Client
from dotenv import load_dotenv
import os

load_dotenv()

app = Client(
    "session/userbot",
    api_id=int(os.getenv("API_ID")),
    api_hash=os.getenv("API_HASH")
)

app.run()