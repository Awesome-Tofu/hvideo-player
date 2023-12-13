import os
import asyncio
import subprocess
from pyrogram import Client, filters
from pytgcalls import StreamType
from pytgcalls.types import AudioPiped, VideoPiped, AudioVideoPiped
from Hanime import app, bot, music
import requests

@bot.on_message(filters.command(["play", "vplay", "test"]) & filters.group)
async def play_command(_, message):
    try:
        link = message.text.split(None, 1)[1]
        chat_id = -1001849819947
        await message.delete()
        state = message.command[0].lower()
        testfile = "test.mkv"

        if state == "play":
            damn = AudioPiped
            emj = "🎵"
            stream_file = link
        elif state == "vplay":
            damn = VideoPiped
            emj = "🎬"
            stream_file = link
        elif state == "test":
            damn = AudioVideoPiped
            emj = "🎵🎬"
            stream_file = testfile

        m = await message.reply_text("🔄 ᴘʀᴏᴄᴇssɪɴɢ...")
        await app.join_group_call(
            chat_id,
            damn(stream_file)
        )
        await m.edit(f"{emj} sᴛᴀʀᴛᴇᴅ sᴛʀᴇᴀᴍɪɴɢ: [Link]({link})", disable_web_page_preview=True)

    except Exception as e:
        print(e)
        return await m.edit(str(e))

    except requests.exceptions.RequestException as err:
        await message.reply_text(f"Error fetching data: {err}")

    else:
        await message.reply_text("Error: kela")
