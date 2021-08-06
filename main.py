# Made with python3
# (C) @FayasNoushad
# Copyright permission under MIT License
# All rights reserved by FayasNoushad
# License -> https://github.com/FayasNoushad/Pyrogram-Json-Bot/blob/main/LICENSE

import os
import pyrogram
from io import BytesIO
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

Bot = Client(
    "Pyrogram Json Bot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
)

START_TEXT = """
Hello {}, I am a telegram to pyrogram json bot. I can send details json of a message.

Made by @FayasNoushad
"""
HELP_TEXT = """
- Just send any type of message for json details
- Add me to group and send any type of message in group and reply /json for json details of message

Made by @FayasNoushad
"""
ABOUT_TEXT = """
- **Bot :** `Pyrogram Json Bot`
- **Creator :** [Fayas](https://telegram.me/TheFayas)
- **Channel :** [Fayas Noushad](https://telegram.me/FayasNoushad)
- **Source :** [Click here](https://github.com/FayasNoushad/Pyrogram-Json-Bot)
- **Language :** [Python3](https://python.org)
- **Library :** [Pyrogram](https://pyrogram.org)
- **Server :** [Heroku](https://heroku.com)
"""
START_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Channel', url='https://telegram.me/FayasNoushad'),
        InlineKeyboardButton('Feedback', url='https://telegram.me/TheFayas')
        ],[
        InlineKeyboardButton('Help', callback_data='help'),
        InlineKeyboardButton('About', callback_data='about'),
        InlineKeyboardButton('Close', callback_data='close')
        ]]
    )
HELP_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Home', callback_data='home'),
        InlineKeyboardButton('About', callback_data='about'),
        InlineKeyboardButton('Close', callback_data='close')
        ]]
    )
ABOUT_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Home', callback_data='home'),
        InlineKeyboardButton('Help', callback_data='help'),
        InlineKeyboardButton('Close', callback_data='close')
        ]]
    )
JSON_BUTTON = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('⚙ Join Updates Channel ⚙', url='https://telegram.me/FayasNoushad')
        ]]
    )


@Bot.on_callback_query()
async def cb_handler(bot, update):
    if update.data == "home":
        await update.message.edit_text(
            text=START_TEXT.format(update.from_user.mention),
            reply_markup=START_BUTTONS,
            disable_web_page_preview=True
        )
    elif update.data == "help":
        await update.message.edit_text(
            text=HELP_TEXT,
            reply_markup=HELP_BUTTONS,
            disable_web_page_preview=True
        )
    elif update.data == "about":
        await update.message.edit_text(
            text=ABOUT_TEXT,
            reply_markup=ABOUT_BUTTONS,
            disable_web_page_preview=True
        )
    else:
        await update.message.delete()


@Bot.on_message(filters.private & filters.command(["start"]))
async def start(bot, update):
    await update.reply_text(
        text=START_TEXT.format(update.from_user.mention),
        disable_web_page_preview=True,
        reply_markup=START_BUTTONS
    )


@Bot.on_message(filters.private & filters.command(["help"]))
async def help(bot, update):
    await update.reply_text(
        text=HELP_TEXT,
        disable_web_page_preview=True,
        reply_markup=HELP_BUTTONS
    )


@Bot.on_message(filters.private & filters.command(["about"]))
async def about(bot, update):
    await update.reply_text(
        text=ABOUT_TEXT,
        disable_web_page_preview=True,
        reply_markup=ABOUT_BUTTONS
    )


@Bot.on_message(filters.private & (filters.text | filters.media | filters.service) & ~filters.reply & ~filters.edited)
async def private(bot, update):
    await reply_file(bot, update)


@Bot.on_message((filters.group | filters.private) & filters.command(["json"]))
async def group(bot, update):
    await reply_file(bot, update.reply_to_message)


async def reply_file(bot, update):
    with BytesIO(str.encode(str(update))) as file:
        file.name = "json.txt"
        await update.reply_document(
            document=file,
            quote=True,
            reply_markup=JSON_BUTTON
        )
        try:
            os.remove(file)
        except:
            pass


@Bot.on_inline_query()
async def inline(bot, update):
    await update.answer(
        results=[],
        switch_pm_text="Your json was sent to pm",
        switch_pm_parameter="start"
    )
    with BytesIO(str.encode(str(update))) as file:
        file.name = "json.txt"
        await bot.send_document(
            chat_id=update.from_user.id,
            document=file,
            reply_markup=JSON_BUTTON
        )
        try:
            os.remove(file)
        except:
            pass


Bot.run()
