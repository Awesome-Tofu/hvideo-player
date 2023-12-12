import pyrogram
from pytgcalls import idle
from Hanime import bot, app, music
import config

async def run_clients():
    await bot.start()
    await app.start()

    if not music.is_connected:
        await music.start()

    await pyrogram.idle()
    await bot.send_message(chat_id=config.GROUP_ID, text="I Started Successfully `Bot`")
    await music.send_message(chat_id=config.GROUP_ID, text="I Started Successfully `app`")
    await idle()

if __name__ == "__main__":
    import asyncio
    asyncio.get_event_loop().run_until_complete(run_clients())

print("INFO: ALL CLIENTS STARTED SUCCESSFULLY")
