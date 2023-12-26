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
DB_URL = os.getenv("mongodb+srv://tofu:tofu@cluster2.gz7lfjd.mongodb.net/?retryWrites=true&w=majority")
DB = MongoClient(DB_URL)
DATABASE = DB.MAIN


# Set up bot configurations
API_ID = 9949701
API_HASH = "47013db2802464f3d2c09593fb0dc880"
SESSION = "BQCX0gUAtu0zGjq2j2SSFs-dC43uk0n11oqLQp44PbXtYdy2J3V603oDLT8TD3bP2rJ_iP0mj9kfMwCH6GvrJ5amY9N-rymyfu-UIWx2vBryF6E9vp33ifoXcXkYaaLZfXwAKSkK-nMdk40eYjurUUBhCm8pQ7-qrQFiJa_yM6hsK7GKjtJrB4cfAUS5Cnr3oj3JyAW7UrBcPgJGjk9diGAvvr38Ph7ojy28-Y6HCWQru5jFd1Pf5eKKl0RmGlT5gVdt6h941T1jhW7qJX6IyIOkmnezarkB8dslGfy7m3TN90kWmHDp-OZC9V9bB5mPEXBq9jKE0DUxp_LLPlz9ysm5bK4ZUAAAAAEwKIdxAA"
TOKEN = "6085244632:AAFgvCOhdrL33gqoIeiWJWEVXTnN3eBOucU"


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
