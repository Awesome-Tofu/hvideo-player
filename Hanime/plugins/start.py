import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import MessageNotModified
from config import BOT_NAME, USERNAME
from config import SUPPORT_GROUP, UPDATES_CHANNEL
from strings import START_TEXT, HELP_TEXT, ABOUT_TEXT
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from Hanime import bot 

@bot.on_message(filters.command(["start", f"start@{USERNAME}"]))
async def start(_, message):
   buttons = [
            [
                InlineKeyboardButton("❔ HOW TO USE ME ❔", callback_data="help"),
            ],
            [
                InlineKeyboardButton("📢 CHANNEL", url=f"https://t.me/{UPDATES_CHANNEL}"),
                InlineKeyboardButton("DEVLOPER 📦", url=f"https://t.me/IkariS0_0"),
            ],
            [
                InlineKeyboardButton("🤖 ABOUT", callback_data="about"),
                InlineKeyboardButton("CLOSE 🔒", callback_data="close"),
            ],
            [
               InlineKeyboardButton("➕ ADD ME TO YOUR GROUP ➕", url=f"https://t.me/{USERNAME}?startgroup=true"),
            ]
            ]
   reply_markup = InlineKeyboardMarkup(buttons)
   if message.chat.type == 'private':
       await message.reply_text(
          START_TEXT,
          reply_markup=reply_markup
       )
   else:
      await message.reply_text(f"**{BOT_NAME} is Alive !** ✨")

@bot.on_callback_query()
async def cb_handler(client: bot, query: CallbackQuery):
    if query.data=="help":
        buttons = [
            [
                InlineKeyboardButton("🔙 BACK", callback_data="start"),
                InlineKeyboardButton ("SUPPORT 💬", url=f"https://t.me/{SUPPORT_GROUP}"),
            ]
            ]
        reply_markup = InlineKeyboardMarkup(buttons)
        try:
            await query.edit_message_text(
                HELP_TEXT,
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass

    elif query.data=="about":
        buttons = [
            [
                InlineKeyboardButton("🔙 BACK", callback_data="start"),
                InlineKeyboardButton ("SUPPORT 💬", url=f"https://t.me/{SUPPORT_GROUP}"),
            ]
            ]
        reply_markup = InlineKeyboardMarkup(buttons)
        try:
            await query.edit_message_text(
                ABOUT_TEXT,
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass

    elif query.data=="start":
        buttons = [
            [
                InlineKeyboardButton("❔ HOW TO USE ME ❔", callback_data="help"),
            ],
            [
                InlineKeyboardButton("📢 CHANNEL", url=f"https://t.me/{UPDATES_CHANNEL}"),
                InlineKeyboardButton("DEVLOPER 📦", url=f"https://t.me/IkariS0_0"),
            ],
            [
                InlineKeyboardButton("🤖 ABOUT", callback_data="about"),
                InlineKeyboardButton("CLOSE 🔒", callback_data="close"),
            ],
            [
               InlineKeyboardButton("➕ ADD ME TO YOUR GROUP ➕", url=f"https://t.me/{USERNAME}?startgroup=true"),
            ]
            ]
        reply_markup = InlineKeyboardMarkup(buttons)
        try:
            await query.edit_message_text(
                START_TEXT,
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass

    elif query.data=="close":
        try:
            await query.message.delete()
            await query.message.reply_to_message.delete()
        except:
            pass