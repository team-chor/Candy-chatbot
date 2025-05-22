import re
from pyrogram import filters
import random
from ChatBot import app


@app.on_message(filters.command(["gn","n","oodnight","ood Night","ood night"], prefixes=["/","g","G"]))
async def goodnight_command_handler(_, message):
    sender = message.from_user.mention
    emoji = get_random_emoji()
    await app.send_message(message.chat.id, emoji)
    await message.reply_text(f"**Goodnight, {sender}! Sleep tight. {emoji}**")

def get_random_emoji():
    emojis = [
        "😴",
        "😪",
        "💤",
    ]
    return random.choice(emojis) 
