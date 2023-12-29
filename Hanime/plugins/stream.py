import os
import asyncio
import random
import aiohttp
import subprocess
from pyrogram import Client, filters, enums
from pytgcalls import StreamType, idle
from pytgcalls.types.input_stream import AudioPiped, VideoPiped, AudioVideoPiped
from Hanime import app, bot, music
import requests
from pySmartDL import SmartDL
from pyrogram.enums import ChatMemberStatus, ChatType
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from functools import wraps 
from Hanime.functions.queue import QUEUE, add_to_queue, get_queue, clear_queue, pop_an_item

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
            InlineKeyboardButton(text="• ᴄʟᴏsᴇ •", callback_data="close")
        ]
    ]
)

async def skip_current_song(chat_id, link):
    if chat_id in QUEUE:
        chat_queue = get_queue(chat_id)
        if len(chat_queue) == 1:
            await app.leave_group_call(chat_id)
            clear_queue(chat_id)
            return 1
        else:
            audio_path = await download_audio(link)
            
            await app.join_group_call(
                chat_id,
                AudioVideoPiped(audio_path)
            )
            
            title, duration, thumb_url = pop_an_item(chat_id)
            await bot.send_photo(chat_id, photo=thumb_url,
                                caption=f"[»] <b>ɴᴏᴡ ᴘʟᴀʏɪɴɢ:</b> [{title}]\n\n[»] <b>ᴅᴜʀᴀᴛɪᴏɴ:</b> {duration}",
                                reply_markup=BUTTONS)
            return [title, duration, thumb_url, link]
    else:
        return 0

async def skip_item(chat_id, lol):
    if chat_id in QUEUE:
        chat_queue = get_queue(chat_id)
        try:
            x = int(lol)
            title = chat_queue[x][0]
            chat_queue.pop(x)
            return title
        except Exception as e:
            print(e)
            return 0
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
        op = await skip_current_song(chat_id)
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
        state = message.command[0].lower()

        # Process command based on state
        if len(message.command) > 1 and message.command[1].lower() == "random":
            random_file = await fetch_hbar("https://hentaibar.onrender.com/random")
        else:
            if len(message.command) <= 1:
                return await message.reply_text("❗ **PLEASE USE LIKE /hplay <query>**")

            query = message.text.split(None, 1)[1]
            search_file = await fetch_hbar_search(query)
            if not search_file:
                return await message.reply_text("❗ **NO RESULTS FOUND**")

            random_file = search_file

        link = random_file["file_url"]
        title = random_file["title"]
        thumb_url = random_file["thumb_url"]
        duration = random_file["duration"]

        # Add to queue and join the voice chat if not joined
        queue_index = add_to_queue(chat_id, title, duration, thumb_url, link)
        if chat_id not in QUEUE:
            audio_path = await download_audio(link)
            await app.join_group_call(chat_id, AudioVideoPiped(audio_path))

        # Send response
        current_queue = get_queue(chat_id)
        if current_queue:
            caption = (
                f"**♬ Added to Queue | Position:** {queue_index}\n\n"
                f"**⋆ Title** : {title}\n**⋆ Duration** : {duration}\n"
            )
            await message.reply_photo(chat_id, thumb_url, caption, reply_markup=BUTTONS)
        else:
            caption = (
                f"**♬ Started Streaming |**\n\n"
                f"**⋆ Title** : {title}\n**⋆ Duration** : {duration}\n"
            )
            await message.send_photo(chat_id, thumb_url, caption, reply_markup=BUTTONS)

    except Exception as e:
        print(e)
        return await message.reply_text(f"❗ **ERROR:** {e}")

    except requests.exceptions.RequestException as err:
        await message.reply_text(f"Error fetching data: {err}")



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


@bot.on_message(filters.command("skip") & filters.group)
async def skip(_, message):
    await message.delete()
    chat_id = message.chat.id
    if len(message.command) < 2:
        op = await skip_current_song(chat_id, link)
        if op == 0:
            await message.reply_text("❗️ɴᴏᴛʜɪɴɢ ɪɴ ᴛʜᴇ ǫᴜᴇᴜᴇ ᴛᴏ sᴋɪᴘ.")
        elif op == 1:
            await message.reply_text("❗️ᴇᴍᴘᴛʏ ǫᴜᴇᴜᴇ, sᴛᴏᴘᴘᴇᴅ sᴛʀᴇᴀᴍɪɴɢ.")
    else:
        skip = message.text.split(None, 1)[1]
        out = "🗑 <ʙ>ʀᴇᴍᴏᴠᴇᴅ ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ sᴏɴɢs ғʀᴏᴍ ᴛʜᴇ ǫᴜᴇᴜᴇ:</b> \n"
        if chat_id in QUEUE:
            items = [int(x) for x in skip.split(" ") if x.isdigit()]
            items.sort(reverse=True)
            for x in items:
                if x == 0:
                    pass
                else:
                    hm = await skip_item(chat_id, x)
                    if hm == 0:
                        pass
                    else:
                        out = out + "\n" + f"<b>#️⃣ {x}</b> - {hm}"
            await message.reply_text(out)

@bot.on_message(filters.command(["playlist", "queue"]) & filters.group)
async def playlist(_, message):
    chat_id = message.chat.id
    if chat_id in QUEUE:
        chat_queue = get_queue(chat_id)
        if chat_queue and len(chat_queue) > 0:
            if len(chat_queue[0]) >= 5:  # Ensure there are at least 5 elements in chat_queue[0]
                await message.delete()
                await message.reply_text(
                    f"▶️ <b>ɴᴏᴡ ᴘʟᴀʏɪɴɢ:</b> [{chat_queue[0][0]}]({chat_queue[0][2]}) | `{chat_queue[0][4]}`",
                    disable_web_page_preview=True,
                )
                if len(chat_queue) > 1:
                    out = f"<b>📃 Player queue:</b> \n\n▶️ <b>ɴᴏᴡ ᴘʟᴀʏɪɴɢ:</b> [{chat_queue[0][0]}]({chat_queue[0][2]}) | `{chat_queue[0][4]}` \n"
                    for x in range(1, len(chat_queue)):
                        if len(chat_queue[x]) >= 3:  # Ensure there are at least 3 elements in chat_queue[x]
                            title = chat_queue[x][0]
                            link = chat_queue[x][4]
                            duration = chat_queue[x][2]
                            out += f"\n<b>#️⃣ {x}</b> - [{title}]({link}) | `{duration}` \n"
                else:
                    out = "<b>📃 Player queue is empty.</b>"
                await message.reply_text(out, disable_web_page_preview=True)
            else:
                await message.reply_text("❗ Insufficient elements in the queue data.")
        else:
            await message.reply_text("❗ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ.")
    else:
        await message.reply_text("❗ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ.")
