import re
from pyrogram import filters
import random
from ChatBot import app


# Good Morning Handler
@app.on_message(filters.command(["gm", "orning", "oodmorning", "ood Morning", "ood morning"], prefixes=["/", "g", "G"]))
async def goodmorning_command_handler(_, message):
    sender = message.from_user.mention
    emoji = get_random_morning_emoji()
    await app.send_message(message.chat.id, emoji)
    await message.reply_text(f"**Good morning, {sender}! Have a wonderful day. {emoji}**")

def get_random_morning_emoji():
    emojis = [
        "☀️",
        "🌞",
        "🌅",
    ]
    return random.choice(emojis)
