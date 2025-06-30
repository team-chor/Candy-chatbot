import asyncio
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.enums import ChatAction

from ChatBot import app
from ChatBot.database import is_chatbot_enabled, enable_chatbot, disable_chatbot, chatbot_api, is_admins

async def text_filter(_, __, m: Message):
    return (
        bool(m.text)
        and not m.text.startswith(("!", "/"))
        and (not m.reply_to_message or m.reply_to_message.reply_to_message_id == m._client.me.id)
        and not (m.mentioned and (m.text.startswith("!") or m.text.startswith("/")))
    )

chatbot_filter = filters.create(text_filter)

@app.on_message(
    (
        (filters.text & filters.group & chatbot_filter) 
        | (filters.mentioned & ~filters.via_bot & ~filters.regex("^[!/]"))
    ) 
    & ~filters.bot 
    & ~filters.sticker
)
async def chatbot(_, message: Message):
    chat_id = message.chat.id

    if not await is_chatbot_enabled(chat_id) and not message.mentioned:
        return

    await app.send_chat_action(chat_id, ChatAction.TYPING)
    reply = chatbot_api.ask_question(message.text)
    await message.reply_text(reply or "❖ ChatBot Error. Contact @TEAM_CHOR.")

@app.on_message(filters.command(["chatbot"]) & filters.group & ~filters.bot)
@is_admins
async def chatbot_toggle(_, message: Message):
    chat_id = message.chat.id
    args = message.command[1:]  

    if not args:
        await message.reply_text("❖ Usage: `/chatbot on` or `/chatbot off`")
        return

    if args[0].lower() in ["on", "enable"]:
        if await is_chatbot_enabled(chat_id):
            await message.reply_text("❖ Chatbot is already enabled.")
            return
        await enable_chatbot(chat_id)
        await message.reply_text(f"❖ Chatbot enabled by {message.from_user.mention}.")

    elif args[0].lower() in ["off", "disable"]:
        if not await is_chatbot_enabled(chat_id):
            await message.reply_text("❖ Chatbot is already disabled.")
            return
        await disable_chatbot(chat_id)
        await message.reply_text(f"❖ Chatbot disabled by {message.from_user.mention}.")

    else:
        await message.reply_text("❖ Invalid option. Use `/chatbot on` or `/chatbot off`.")
