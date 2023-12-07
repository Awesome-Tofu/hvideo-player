import os
import asyncio
from pytgcalls import GroupCallFactory
from pyrogram import Client, filters
from pyrogram.types import Message
from Hanime import app, bot, music

group_call_factory = GroupCallFactory(app, GroupCallFactory.MTPROTO_CLIENT_TYPE.PYROGRAM)
VIDEO_CALL = {}


async def download_and_convert_video(reply_message, chat_id):
    try:
        video = await music.download_media(reply_message)
        os.system(f'ffmpeg -i "{video}" -vn -f s16le -ac 2 -ar 48000 -acodec pcm_s16le -filter:a "atempo=0.81" vid-{chat_id}.raw -y')
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
            group_call = group_call_factory.get_file_group_call(f'vid-{chat_id}.raw')
            await group_call.start(chat_id)
            await group_call.set_video_capture(await music.download_media(replied_message))
            VIDEO_CALL[chat_id] = group_call
            await message.reply("**▶️ Started Streaming!**")
    except Exception as e:
        await message.reply(f"**Error during streaming: {e}**")


@bot.on_message(filters.command("stop"))
async def stop_video(client, message):
    chat_id = message.chat.id
    try:
        await VIDEO_CALL[chat_id].stop()
        await message.reply("**⏹️ Stopped Streaming!**")
        # Clean up temporary files after stopping the stream
        os.remove(f'vid-{chat_id}.raw')
    except Exception as e:
        await message.reply(f"**Error during stopping the stream: {e}**")
