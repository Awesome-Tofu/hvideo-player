import pyrogram
from pytgcalls import idle
from Hanime import bot, app, music
import config

async def run_clients():
    await bot.start()
    await app.start()
    await music.start()
    await pyrogram.idle() 
    await bot.send_message(
        chat_id=config.GROUP_ID,
        text="hello bot"
    )
    await music.send_message(
        chat_id=config.GROUP_ID,
        text="hello app"
    )
    await idle()

if __name__ == "__main__":
    app.loop.run_until_complete(run_clients())