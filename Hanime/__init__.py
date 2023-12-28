import os
import time
import logging
from pyrogram import Client
from pymongo import MongoClient
from pytgcalls import PyTgCalls, idle
from config import SESSION, API_ID, API_HASH, TOKEN, DB_URL


FORMAT = "[INFO]: %(message)s"

logging.basicConfig(
    level=logging.INFO,
    handlers=[logging.FileHandler("logs.txt"), logging.StreamHandler()],
    format=FORMAT,
)

# Set up logging
logger = logging.getLogger(__name__)

# Set up database connection
DB = MongoClient(DB_URL)
DATABASE = DB.MAIN

#Vars
SUDO = [5690711835,5015417782,5915335486,6495253163,6390170725]


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
