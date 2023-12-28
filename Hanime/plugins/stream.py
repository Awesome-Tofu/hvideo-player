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


async def fetch_random_file():
    random_url = "https://hentaibar.onrender.com/random"
    response = requests.get(random_url)    
    if response.status_code == 200:
        data = response.json()
        file_url = data.get("file")
        title = data.get("name")
        thumb_url = data.get("thumbnailUrl")
        duration = data.get("duration")
        if file_url:
            return {file_url, title, thumb_url, duration}
    return None


@bot.on_message(filters.command(["hplay"]) & filters.group)
async def hplay_command(_, message):
    try:
        chat_id = message.chat.id
        await message.delete()
        m = await message.reply_text("🔄 ᴘʀᴏᴄᴇssɪɴɢ...")
        state = message.command[0].lower()

        if len(message.command) > 1 and message.command[1].lower() == "random":
            random_file = await fetch_random_file()
            link = random_file["file_url"]
            title = random_file["title"]
            thumb_url = random_file["thumb_url"]
            duration = random_file["duration"]
        else:
            link = message.text.split(None, 1)[1]

        audio_path = await download_audio(link)
        await app.join_group_call(
            chat_id,
            AudioVideoPiped(audio_path)
        )
        await m.delete()
        await message.send_photo(chat_id=chat_id,photo=thumb_url,caption=f"♬ Started Streaming |\n\n⋆ Title : {title}\n⋆ Duration : {duration}\n", disable_web_page_preview=True)

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
