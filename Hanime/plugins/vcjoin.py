from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import UserAlreadyParticipant
from Hanime import app, bot


@bot.on_message(filters.command(["join"]) & filters.group)
async def join_chat(c: Client, m: Message):
    chat_id = m.chat.id
    try:
        invitelink = await c.export_chat_invite_link(chat_id)
        if invitelink.startswith("https://t.me/+"):
            invitelink = invitelink.replace("https://t.me/+", "https://t.me/joinchat/")
            await app.join_chat(invitelink)
            return await bot.send_message(chat_id, "✅ Assistant joined chat")
    except UserAlreadyParticipant:
        return await bot.send_message(chat_id, "✅ Assistant already in chat")
