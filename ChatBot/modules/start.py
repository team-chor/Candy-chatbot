import asyncio
import random
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.enums import ChatType
from config import STICKER, FSUB
from ChatBot import app
from ChatBot.database import add_user, add_chat, remove_chat, get_fsub


@app.on_message(filters.command("start") & ~filters.bot)
async def start(client, m: Message):
    if FSUB and not await get_fsub(client, m):
        return

    bot_name = app.name

    if m.chat.type == ChatType.PRIVATE:
        user_id = m.from_user.id
        await add_user(user_id, m.from_user.username or None)

        if STICKER and isinstance(STICKER, list):
            sticker_to_send = random.choice(STICKER)
            umm = await m.reply_sticker(sticker=sticker_to_send)
            await asyncio.sleep(2)
            await umm.delete()

        await m.reply_text(
            f"""
<b>Hey {m.from_user.mention}. 💖</b>  

Welcome to <b>{bot_name}</b>, your cute and sassy chat buddy! ✨  
I'm here to keep you entertained, tease you a little, and make sure you never feel lonely.  

<i>SassyVibes FunChat MagicMoments SnarkyReplies PlayfulChats SassyTalks </i> <a href='https://unitedcamps.in/Images/file_10516.jpg'>🦋</a>💖
""",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text="🍷 ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ 🍷", url=f"https://t.me/{app.username}?startgroup=true")],
                [
                    InlineKeyboardButton(text="🫧 ᴄʜᴀɴɴᴇʟ 🫧", url="https://t.me/C0DE_SEARCH"),
                    InlineKeyboardButton(text="🫧 sᴜᴘᴘᴏʀᴛ 🫧", url="https://t.me/AsuraaSupports")
                ],
                [InlineKeyboardButton(text="📜 ᴍʏ ᴄᴏᴍᴍᴀɴᴅs 📜", callback_data="help")]
            ]),
            disable_web_page_preview=False,
            reply_to_message_id=m.id
        )

    elif m.chat.type in {ChatType.GROUP, ChatType.SUPERGROUP}:
        chat_id = m.chat.id
        await add_chat(chat_id, m.chat.title)
        await m.reply_text(
            f"Hey {m.from_user.mention}, I’m {bot_name}, here to keep the energy high. Use /help to see what I can do.",
            disable_web_page_preview=False
        )


@app.on_chat_member_updated()
async def chat_updates(client, m):
    bot_id = (await client.get_me()).id

    if m.new_chat_member and m.new_chat_member.user.id == bot_id:
        chat_id = m.chat.id
        await add_chat(chat_id, m.chat.title)

    elif m.old_chat_member and m.old_chat_member.user.id == bot_id and not m.new_chat_member:
        chat_id = m.chat.id
        await remove_chat(chat_id)


@app.on_message(filters.command("help") & filters.group)
async def help(client, m: Message):
    await m.reply_text(
        "Need help? Click below to see all my commands.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📜 ᴄᴏᴍᴍᴀɴᴅs ᴀɴᴅ ɢᴜɪᴅᴇ 📜", url="http://t.me/MissAaru_Robot?start=help")]
        ]),
        disable_web_page_preview=False
    )


@app.on_callback_query()
async def callback(client, query: CallbackQuery):
    bot_name = app.name

    if query.data == "start":
        if query.message.chat.type == ChatType.PRIVATE:
            new_text = f"""
<b>Hey {query.from_user.mention}. 💖</b>  

Welcome to <b>{bot_name}</b>, your cute and sassy chat buddy! ✨  
I'm here to keep you entertained, tease you a little, and make sure you never feel lonely.  

<i>SassyVibes FunChat MagicMoments SnarkyReplies PlayfulChats SassyTalks </i> <a href='https://unitedcamps.in/Images/file_10516.jpg'>🦋</a>💖
"""

            if query.message.text != new_text:
                await query.message.edit_text(
                    new_text,
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton(text="🍷ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ🍷", url="https://t.me/MissAaru_Robot?startgroup=true")],
                        [
                            InlineKeyboardButton(text="🫧ᴄʜᴀɴɴᴇʟ🫧", url="https://t.me/C0DE_SEARCH"),
                            InlineKeyboardButton(text="🫧sᴜᴘᴘᴏʀᴛ🫧", url="https://t.me/AsuraaSupports")
                        ],
                        [InlineKeyboardButton(text="📜 ᴍʏ ᴄᴏᴍᴍᴀɴᴅs 📜", callback_data="help")]
                    ]),
                    disable_web_page_preview=False
                )

    elif query.data == "help":
        if query.message.chat.type == ChatType.PRIVATE:
            help_message = f"""
<b><blockquote>❖ Aaru’s Magic Tricks. 💫</blockquote></b>  
⬤ /start ➥ Start our chat, baby. 🌟
⬤ /ping ➥ Check if I'm awake. 🔔
⬤ /draw ➥ Let’s get artsy, I’ll draw your imagination. 🎨
⬤ /ask ➥ Provide me with a query to ask Aaru AI. 😋
⬤ /stats ➥ Get group and user stats. 📊
⬤ /chatbot ➥ Toggle my AI replies in groups. 🤖
⬤ /song ➥ Name the track, and I’ll deliver the magic. 🎶
⬤ /sticker ➥ Searching for a sticker pack? Drop a name, and I'll find it for you. 🖼️ 
⬤ /kiss ➥ Get a virtual kiss from me. 😘  
⬤ /hug ➥ Let me wrap you in a warm hug. 🤗 
⬤ /waifu ➥ Want a cute waifu image? Just drop a tag, and I'll fetch one for you. 💕
⬤ /horny ➥ Reply to an image to get a horny card. 💖
⬤ /anime ➥ Reply to an image, and I'll turn it into an anime-style masterpiece. 🎨✨
⬤ /repo ➥ Get the Aaru ChatBot source code instantly! Tap the link below. 📂✨

<i><blockquote>More coming soon... I keep getting better. ✨</blockquote></i>  
"""

            if query.message.text != help_message:
                await query.message.edit_text(
                    help_message,
                    reply_markup=InlineKeyboardMarkup([
                        [
                            InlineKeyboardButton(text="🫧ʙᴀᴄᴋ🫧", callback_data="start"),
                            InlineKeyboardButton(text="🫧ᴄʜᴀɴɴᴇʟ🫧", url="https://t.me/C0DE_SEARCH")
                        ]
                    ]),
                    disable_web_page_preview=False
                )