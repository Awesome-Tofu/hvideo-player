import os
import asyncio
import random
import aiohttp
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


async def fetch_hbar(url):
    response = requests.get(url)    
    if response.status_code == 200:
        data = response.json()
        file_url = data.get("file")
        title = data.get("name")
        thumb_url = data.get("thumbnailUrl")
        duration = data.get("duration")
        if data:
            return {"file_url": file_url, "title": title, "thumb_url": thumb_url, "duration": duration}
    return None

async def fetch_hbar_search(query):
    response = requests.get(f"https://hentaibar.onrender.com/search/{query}/1")    
    if response.status_code == 200:
        data = response.json()
        result = random.choice(data["results"])
        fetched_vid = await fetch_hbar(result["url"])
        file_url = fetched_vid.get("file_url")
        title = fetched_vid.get("title")
        thumb_url = fetched_vid.get("thumb_url")
        duration = fetched_vid.get("duration")
        if data:
            return {"file_url": file_url, "title": title, "thumb_url": thumb_url, "duration": duration}
    return None    



@bot.on_message(filters.command(["hplay"]) & filters.group)
async def hplay_command(_, message):
    try:
        chat_id = message.chat.id
        await message.delete()
        m = await message.reply_text("🔄 ᴘʀᴏᴄᴇssɪɴɢ...")
        QUEUE[chat_id] = True
        state = message.command[0].lower()

        if len(message.command) > 1 and message.command[1].lower() == "random":
            random_file = await fetch_hbar("https://hentaibar.onrender.com/random")
            link = random_file["file_url"]
            title = random_file["title"]
            thumb_url = random_file["thumb_url"]
            duration = random_file["duration"]          
        else:
            if len(message.command) <= 1:
                await m.edit("❗ **PLEASE USE LIKE /hplay <query>**")
                return
            query = message.text.split(None, 1)[1]
            search_file = await fetch_hbar_search(query)
            link = search_file["file_url"]
            title = search_file["title"]
            thumb_url = search_file["thumb_url"]
            duration = search_file["duration"]

        audio_path = await download_audio(link)
        await app.join_group_call(
            chat_id,
            AudioVideoPiped(audio_path)
        )
        await m.delete()
        await message.reply_photo(photo=thumb_url,caption=f"**♬ Started Streaming |**\n\n**⋆ Title** : {title}\n**⋆ Duration** : {duration}\n")

    except Exception as e:
        print(e)
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


@bot.on_message(filters.command("pause") & filters.group)
async def pause(_, message):
    await message.delete()
    chat_id = message.chat.id
    if chat_id in QUEUE:
        try:
            await app.pause_stream(chat_id)
            await message.reply_text("II ᴘᴀᴜsᴇᴅ sᴛʀᴇᴀᴍɪɴɢ.")
        except:
            await message.reply_text("❗ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ.")
    else:
        await message.reply_text("❗ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ.")
        
        
@bot.on_message(filters.command("resume") & filters.group)
async def resume(_, message):
    await message.delete()
    chat_id = message.chat.id
    if chat_id in QUEUE:
        try:
            await app.resume_stream(chat_id)
            await message.reply_text("▷ ʀᴇsᴜᴍᴇᴅ sᴛʀᴇᴀᴍɪɴɢ.")
        except:
            await message.reply_text("❗ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ.")
    else:
        await message.reply_text("❗ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ.")
