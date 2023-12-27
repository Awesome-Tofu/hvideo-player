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


async def fetch_random_file(message):
    random_url = "https://hentaibar.onrender.com/random"
    response = requests.get(random_url)    
    if response.status_code == 200:
        data = response.json()
        file_url = data.get("file")
        if file_url:
            return file_url
    return None


@bot.on_message(filters.command(["play", "vplay", "test"]) & filters.group)
async def play_command(_, message):
    try:
        chat_id = message.chat.id
        await message.delete()
        m = await message.reply_text("🔄 ᴘʀᴏᴄᴇssɪɴɢ...")
        state = message.command[0].lower()

        if len(message.command) > 1 and message.command[1].lower() == "random":
            link = await fetch_random_file(message)
        else:
            link = message.text.split(None, 1)[1]

        if state == "play":
            damn = AudioPiped
            emj = "🎵"
        elif state == "vplay":
            damn = AudioVideoPiped
            emj = "🎬"

        audio_path = await download_audio(link)
        await app.join_group_call(
            chat_id,
            damn(audio_path)
        )
        await m.edit(f"{emj} sᴛᴀʀᴛᴇᴅ sᴛʀᴇᴀᴍɪɴɢ: [Link]({link})", disable_web_page_preview=True)

    except Exception as e:
        return await m.edit(str(e))

    except requests.exceptions.RequestException as err:
        await message.reply_text(f"Error fetching data: {err}")

    else:
        print("Error: kela")


@bot.on_message(filters.command(["end"]) & filters.group)
async def end_command(_, message):
    try:
        chat_id = message.chat.id
        await app.leave_group_call(chat_id)
        m = await message.reply_text("🔴 ʟᴇꜰᴛ ᴛʜᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ!")
    except Exception as e:
        await m.edit(f"An error occurred: {e}")
