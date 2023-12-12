import os
import asyncio
import subprocess
from pyrogram import Client, filters
from pytgcalls import StreamType
from pytgcalls.types import AudioPiped
from Hanime import app, bot, music
import requests

api_url_hentai = "https://hentaibar.onrender.com/random"

async def fetch_hentai_data():
    try:
        response = requests.get(api_url_hentai)
        response.raise_for_status()  # Check for errors

        hentai_data = response.json()

        thumb_url = hentai_data.get('thumbnailUrl')
        file_url = hentai_data.get('file')
        name = hentai_data.get('name')
        upload_date = hentai_data.get('upload_date')
        duration = hentai_data.get('duration')

        if thumb_url and file_url and name and upload_date and duration:
            return {
                'thumb_url': thumb_url,
                'file_url': file_url,
                'name': name,
                'upload_date': upload_date,
                'duration': duration
            }
        else:
            return None

    except requests.exceptions.RequestException as err:
        return None

@bot.on_message(filters.command("play", prefixes="/"))
async def play_command(client, message):
    try:
        chat_id = -1001849819947
        await message.reply("Please wait patiently. Fetching data for your request...")

        hentai_data = await fetch_hentai_data()

        if hentai_data:
            thumb_url = hentai_data['thumb_url']
            file_url = hentai_data['file_url']
            name = hentai_data['name']
            upload_date = hentai_data['upload_date']
            duration = hentai_data['duration']

            await message.reply_photo(thumb_url, caption=f"Name: {name}\nUpload Date: {upload_date}\nDuration: {duration}\n\nStreamlink: {file_url}")

            await app.join_group_call(
                chat_id,
                VideoPiped(file_url)
            )

        else:
            await message.reply_text("Error: Incomplete data received from the API.")

    except requests.exceptions.RequestException as err:
        await message.reply_text(f"Error fetching data: {err}")
