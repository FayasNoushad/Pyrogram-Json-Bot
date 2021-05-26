# Made with python3
# (C) @FayasNoushad
# Copyright permission under MIT License
# All rights reserved by FayasNoushad
# License -> https://github.com/FayasNoushad/Pyrogram-Json-Bot/blob/main/LICENSE

import os
import pyrogram
import aiofiles
from pyrogram import Client, filters

FayasNoushad = Client(
    "Pyrogram Json Bot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
)

@FayasNoushad.on_message(filters.private)
async def private(bot, update):
    json = update
    if len(json) > 4096:
        async with aiofiles.open('update.json') as json_file:
            await json_file.write(json)
            await update.reply_document(document='update.json')
        os.remove('update.json')
    else:
        await update.reply_text(
            text=json,
            disable_web_page_preview=True
        )

@FayasNoushad.on_message(filters.group & filters.command(["json"]))
async def group(bot, update):
    json = update.reply_to_message
    if len(json) > 4096:
        async with aiofiles.open('update.json') as json_file:
            await json_file.write(json)
            await update.reply_document(document='update.json')
        os.remove('update.json')
    else:
        await update.reply_text(
            text=json,
            disable_web_page_preview=True
        )
