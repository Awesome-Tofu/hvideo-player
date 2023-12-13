import os
import asyncio
import subprocess
from pyrogram import Client, filters
from pytgcalls import StreamType
from pytgcalls.types import AudioPiped, AudioVideoPiped
from Hanime import app, bot, music
import requests

@bot.on_message(filters.command(["play", "vplay"]) & filters.group)
async def play_command(_, message):
    try:
        link = message.text.split(None, 1)[1]
        chat_id = -1001849819947
        await message.delete()
        state = message.command[0].lower()

        if state == "saudio":
            damn = AudioPiped
            emj = "🎵"
        elif state == "svideo":
            damn = AudioVideoPiped
            emj = "🎬"
        m = await message.reply_text("🔄 ᴘʀᴏᴄᴇssɪɴɢ...")

        await app.join_group_call(
            chat_id,
            damn(link),
            stream_type=StreamType().pulse_stream
        )
        await m.edit(f"{emj} sᴛᴀʀᴛᴇᴅ sᴛʀᴇᴀᴍɪɴɢ: [Link]({link})", disable_web_page_preview=True)

    except Exception as e:
        return await m.edit(str(e))

    except requests.exceptions.RequestException as err:
        await message.reply_text(f"Error fetching data: {err}")

    else:
        await message.reply_text("Error: kela")
