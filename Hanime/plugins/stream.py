import os
import requests
from pyrogram import Client, filters
from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped, VideoPiped
from Hanime import app, bot, music

@bot.on_message(filters.command(["play", "vplay", "test"]) & filters.group)
async def play_command(_, message):
    try:
        chat_id = -1001849819947
        state = message.command[0].lower()
        testfile = "test.mkv"

        # Check if the message is a reply
        if message.reply_to_message and (message.reply_to_message.audio or message.reply_to_message.video):
            media = message.reply_to_message.audio or message.reply_to_message.video
            file_id = media.file_id
            file_path = await app.download_media(file_id)
        else:
            link = message.text.split(None, 1)[1]
            file_path = f"downloaded_file.{link.split('.')[-1]}"
            # Download the file to the server
            response = requests.get(link, stream=True)
            with open(file_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)

        await message.delete()

        if state == "test":
            damn = AudioVideoPiped
            emj = "🎵🎬"
            stream_file = testfile
        else:
            return await message.reply_text("Error: Invalid state")

        m = await message.reply_text("🔄 ᴘʀᴏᴄᴇssɪɴɢ...")
        
        await app.join_group_call(
            chat_id,
            damn(file_path)
        )
        await m.edit(f"{emj} sᴛᴀʀᴛᴇᴅ sᴛʀᴇᴀᴍɪɴɢ: [Link]({file_path})", disable_web_page_preview=True)

    except Exception as e:
        print(e)
        return await m.edit(str(e))

    except requests.exceptions.RequestException as err:
        await message.reply_text(f"Error fetching data: {err}")

    else:
        await message.reply_text("Error: kela")
