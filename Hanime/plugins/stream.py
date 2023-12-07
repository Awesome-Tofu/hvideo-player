import os
import asyncio
import subprocess
from pyrogram import Client, filters
from pytgcalls import StreamType
from Hanime import app, bot, music

VIDEO_CALL = {}


async def download_and_convert_video(reply_message, chat_id):
    try:
        video = await music.download_media(reply_message)
        subprocess.run([
            'ffmpeg',
            '-i', video,
            '-vn', '-f', 's16le',
            '-ac', '2', '-ar', '48000',
            '-acodec', 'pcm_s16le',
            '-filter:a', 'atempo=0.81',
            f'vid-{chat_id}.raw', '-y'
        ], check=True)
        return True
    except Exception as e:
        print(f"Error during download and conversion: {e}")
        return False


@bot.on_message(filters.command("stream"))
async def stream_video(client, message):
    replied_message = message.reply_to_message
    if not replied_message:
        await message.reply("`Reply to some Video!`")
        return

    chat_id = message.chat.id
    try:
        await message.reply("`Downloading...`")
        if await download_and_convert_video(replied_message, chat_id):
            await asyncio.sleep(5)  # Give some time before starting the stream

            # Use app.join_group_call with a play link and pulse_stream stream type
            playlink = "https://hentaibar.onrender.com/video_83e23452.mp4"  # Replace with your actual playlink
            await app.join_group_call(
                chat_id,
                playlink,
                stream_type=StreamType().pulse_stream
            )

            VIDEO_CALL[chat_id] = True  # You can use this to track the active call
            await message.reply("**▶️ Started Streaming!**")
    except Exception as e:
        await message.reply(f"**Error during streaming: {e}**")


@bot.on_message(filters.command("stop"))
async def stop_video(client, message):
    chat_id = message.chat.id
    try:
        if VIDEO_CALL.get(chat_id):
            await app.leave_group_call(chat_id)
            VIDEO_CALL[chat_id] = False  # Update the status of the call
            await message.reply("**⏹️ Stopped Streaming!**")

            # Clean up temporary files after stopping the stream
            os.remove(f'vid-{chat_id}.raw')
        else:
            await message.reply("**❌ No active stream to stop!**")
    except Exception as e:
        await message.reply(f"**Error during stopping the stream: {e}**")
