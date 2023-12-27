import os
import asyncio
import subprocess
from pyrogram import Client, filters
from pytgcalls import StreamType, idle
from pytgcalls.types.input_stream import AudioPiped, VideoPiped, AudioVideoPiped
from Hanime import app, bot, music
import requests
from pySmartDL import SmartDL

async def download_audio(url):
    obj = SmartDL(url, verify=False)
    obj.start()
    obj.wait()
    return obj.get_dest()

@bot.on_message(filters.command(["play", "vplay", "test"]) & filters.group)
async def play_command(_, message):
    try:
        chat_id = -1002107596400
        await message.delete()
        state = message.command[0].lower()

        if state == "play":
            damn = AudioPiped
            emj = "🎵"
            link = message.text.split(None, 1)[1]
        elif state == "vplay":
            damn = AudioVideoPiped
            emj = "🎬"
            link = message.text.split(None, 1)[1]
        elif state == "test":
            damn = VideoPiped
            emj = "🎬"
            link = "test.mkv"
        m = await message.reply_text("🔄 ᴘʀᴏᴄᴇssɪɴɢ...")

        audio_path = await download_audio(link)
        await app.join_group_call(
            chat_id,
            damn(audio_path)
        )
        await idle()
        await m.edit(f"{emj} sᴛᴀʀᴛᴇᴅ sᴛʀᴇᴀᴍɪɴɢ: [Link]({link})", disable_web_page_preview=True)

    except Exception as e:
        return await m.edit(str(e))

    except requests.exceptions.RequestException as err:
        await message.reply_text(f"Error fetching data: {err}")

    else:
        await message.reply_text("Error: kela")
