import os
import time
import logging
from pyrogram import Client
from pymongo import MongoClient
from pytgcalls import PyTgCalls, idle

FORMAT = "[INFO]: %(message)s"

logging.basicConfig(
    level=logging.INFO,
    handlers=[logging.FileHandler("logs.txt"), logging.StreamHandler()],
    format=FORMAT,
)

# Set up logging
logger = logging.getLogger(__name__)

# Set up database connection
DB_URL = os.getenv("MONGO_URI")
DB = MongoClient(DB_URL)
DATABASE = DB.MAIN


# Set up bot configurations
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
SESSION = os.getenv("SESSION")
TOKEN = os.getenv("TOKEN")


# PYROGRAM USER CLIENT
music = Client(
    name="music",
    session_string=SESSION,
    api_id=API_ID,
    api_hash=API_HASH,
    plugins=dict(root="Hanime"),
)

# PYROGRAM BOT CLIENT
bot = Client(
    name="bot",
    bot_token=TOKEN,
    api_id=API_ID,
    api_hash=API_HASH,
    plugins=dict(root="Hanime"),
)

app = PyTgCalls(music)
