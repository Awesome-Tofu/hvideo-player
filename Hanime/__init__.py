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
SESSION = "BQCX0gUADTLzdx-SSwEItNlpoI-RhRP7YnztWHO2W50ExQNzmvI4daKgtnbK4vGqlcMi-XXN_7bBSM13hQz_fWfNjvsDVs7K0k_vdXeqCijjtQOz2tJgQ6bWlvp_8X0VTFYelNZbmxDx4UW6TMWLUEys-9r52YYoYYMvjILPjrzhmPHq6RxE6v0e215Ij1VUJ6fDjhbXUdX0CGIrnUj4fB5VLzvCh5ggPmSPQHAbnM0YJR8SCDgmnyp6oTrr9jVYe0Tb3vsRLYO1tal-XRyOz7p7iDSU4PLnCIopLAvB_b_-MVttL9cysQqJgtJC10n7FsBtpzaWiYKikTtW5HTW9CWSDRugTgAAAAEwKIdxAA"
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
