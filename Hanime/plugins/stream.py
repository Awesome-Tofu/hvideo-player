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
from pyrogram.enums import ChatMemberStatus, ChatType
from functools import wraps 
from queue import QUEUE, add_to_queue, get_queue, clear_queue, pop_an_item





BUTTONS = InlineKeyboardMarkup(
    [ 
        [ 
            InlineKeyboardButton(text="▷", callback_data="pause"),
            InlineKeyboardButton(text="II", callback_data="resume"),
            InlineKeyboardButton(text="‣‣I", callback_data="skip"),
            InlineKeyboardButton(text="▢", callback_data="stop")
        ],
        [ 
            InlineKeyboardButton(text="🔇", callback_data="mute"),
            InlineKeyboardButton(text="🔊", callback_data="unmute")
        ],
        [ 
            InlineKeyboardButton(text="• ᴄʟᴏsᴇ •", callback_data="ok")
        ]
    ]
)


async def skip_current_song(chat_id):
    if chat_id in QUEUE:
        chat_queue = get_queue(chat_id)
        if len(chat_queue) == 1:
            await app.leave_group_call(chat_id)
            clear_queue(chat_id)
            return 1
        else:
            title = chat_queue[1][0]
            duration = chat_queue[1][1]
            thumb_url = chat_queue[1][2]            
            pop_an_item(chat_id)
            await bot.send_photo(chat_id, photo = thumb_url,
                                 caption = f"[»] <b>ɴᴏᴡ ᴘʟᴀʏɪɴɢ:</b> [{title}]\n\n[»] <b>ᴅᴜʀᴀᴛɪᴏɴ:</b> {duration}",
                                 reply_markup = BUTTONS)
            return [title, duration, thumb_url]
    else:
        return 0

@bot.on_callback_query()
async def callbacks(_, cq: CallbackQuery):
    user_id = cq.from_user.id
    try:
        user = await cq.message.chat.get_member(user_id)
        admin_strings = ("creator", "administrator")
        if user.status not in admin_strings:
            is_admin = False
        else:
            is_admin = True
    except ValueError:
        is_admin = True        
    if not is_admin:
        return await cq.answer("[»] ʏᴏᴜ ᴀʀᴇɴ'ᴛ ᴀɴ ᴀᴅᴍɪɴ.")   
    chat_id = cq.message.chat.id
    data = cq.data
    if data == "close":
        return await cq.message.delete()
    if not chat_id in QUEUE:
        return await cq.answer("[»] ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ.")

    if data == "pause":
        try:
            await app.pause_stream(chat_id)
            await cq.answer("[»] ᴘᴀᴜsᴇᴅ sᴛʀᴇᴀᴍɪɴɢ.")
        except:
            await cq.answer("[»] ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ.")
      
    elif data == "resume":
        try:
            await app.resume_stream(chat_id)
            await cq.answer("[»] Resumed streaming.")
        except:
            await cq.answer("[»] ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ.")   

    elif data == "stop":
        await app.leave_group_call(chat_id)
        clear_queue(chat_id)
        await cq.answer("[»] sᴛᴏᴘᴘᴇᴅ sᴛʀᴇᴀᴍɪɴɢ.")  

    elif data == "mute":
        try:
            await app.mute_stream(chat_id)
            await cq.answer("[»] ᴍᴜᴛᴇᴅ sᴛʀᴇᴀᴍɪɴɢ.")
        except:
            await cq.answer("[»] ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ.")
            
    elif data == "unmute":
        try:
            await app.unmute_stream(chat_id)
            await cq.answer("[»] ᴜɴᴍᴜᴛᴇᴅ sᴛʀᴇᴀᴍɪɴɢ.")
        except:
            await cq.answer("[»] ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ.")
            
    elif data == "skip":
        op = await skip_current_video(chat_id)
        if op == 0:
            await cq.answer("[»] ɴᴏᴛʜɪɴɢ ɪɴ ᴛʜᴇ ǫᴜᴇᴜᴇ ᴛᴏ sᴋɪᴘ.")
        elif op == 1:
            await cq.answer("[»] ᴇᴍᴘᴛʏ ǫᴜᴇᴜᴇ, sᴛᴏᴘᴘᴇᴅ sᴛʀᴇᴀᴍɪɴɢ.")
        else:
            await cq.answer("[»] sᴋɪᴘᴘᴇᴅ.")

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

       
        queue_index = add_to_queue(chat_id, title, duration, thumb_url)

        state = message.command[0].lower()

        if len(message.command) > 1 and message.command[1].lower() == "random":
            random_file = await fetch_hbar("https://hentaibar.onrender.com/random")
            link = random_file["file_url"]
            title = random_file["title"]
            thumb_url = random_file["thumb_url"]
            duration = random_file["duration"]          
        else:
            if len(message.command) <= 1:
                await message.reply_text("❗ **PLEASE USE LIKE /hplay <query>**")
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

       
        current_queue = get_queue(chat_id)
        if current_queue:
            await message.reply_photo(photo=thumb_url, caption=f"**♬ Added to Queue | Position:** {queue_index + 1}\n\n**⋆ Title** : {title}\n**⋆ Duration** : {duration}\n")
        else:
            await message.reply_photo(photo=thumb_url, caption=f"**♬ Started Streaming |**\n\n**⋆ Title** : {title}\n**⋆ Duration** : {duration}\n")

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

        # Use clear_queue function to clear the queue for the current chat ID
        clear_queue(chat_id)

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

@bot.on_message(filters.command("mute") & filters.group)
async def mute(_, message):
    await message.delete()
    chat_id = message.chat.id
    if chat_id in QUEUE:
        try:
            await app.mute_stream(chat_id)
            await message.reply_text("🔇 ᴍᴜᴛᴇᴅ sᴛʀᴇᴀᴍɪɴɢ.")
        except:
            await message.reply_text("❗ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ.")
    else:
        await message.reply_text("❗ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ.")

@bot.on_message(filters.command("unmute") & filters.group)
async def unmute(_, message):
    await message.delete()
    chat_id = message.chat.id
    if chat_id in QUEUE:
        try:
            await app.unmute_stream(chat_id)
            await message.reply_text("🔊 ᴜɴᴍᴜᴛᴇᴅ sᴛʀᴇᴀᴍɪɴɢ.")
        except:
            await message.reply_text("❗ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ.")
    else:
        await message.reply_text("❗ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ.")
