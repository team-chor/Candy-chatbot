import io
import os
import google.generativeai as genai
from PIL import Image
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatAction
from ChatBot import app

# Configure Gemini API
genai.configure(api_key=os.environ.get("GEMINI_API_KEY", "AIzaSyCdTbKMDxg7YyQXe2rihjZQ29CuKXbl8RY"))
model = genai.GenerativeModel("gemini-2.0-flash-lite")

# Prompt
IDENTIFY_PROMPT = (
    "You are a image identifying expert, you can name all the characters from anime, Manga, Donghua and more. " 
    "This is a fan art or AI-generated image of a single anime or donghua character. "
    "Take your best guess at the character's name and which series they are from, even if you're unsure. "
    "Only reply in this format:\n\n"
    "I think it's\n"
    "Character: <most likely name>\n"
    "Series: <most likely series>\n\n" 
)

@app.on_message(filters.command("identify") & filters.reply)
async def identify_anime_character(client: Client, message: Message):
    reply = message.reply_to_message

    if not (reply.photo or reply.document):
        return await message.reply("⚠️ Please reply to an image or image document (stickers not supported).")

    await client.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)
    status = await message.reply("🔍 Identifying character, please wait...")

    try:
        # Download media
        media = reply.photo or reply.document
        image_bytes = await client.download_media(media, in_memory=True)
        image = Image.open(image_bytes).convert("RGB")

        # Generate response
        response = model.generate_content([IDENTIFY_PROMPT, image])
        result = response.text.strip()

        if not result:
            raise ValueError("Sorry I couldn't Identify.")

        # Parse output
        char_line = ""
        series_line = ""
        lines = result.splitlines()

        for line in lines:
            if line.lower().startswith("character:"):
                char_line = line.strip()
            elif line.lower().startswith("series:"):
                series_line = line.strip()

        # Check for vague or unknown results
        vague_keywords = ["unknown", "none", "Original Character", "not sure", "difficult", "unclear", "can't tell"]
        if any(keyword in result.lower() for keyword in vague_keywords) or not char_line or not series_line:
            return await status.edit(
                "⚠️ **Sorry, I couldn't confidently identify the character.**\n"
                "Try using a clearer or more recognizable image (face visible, minimal background)."
            )

        # Format and send final result
        formatted_output = (
    "**I think it's:**\n\n"
    f"**{char_line}**\n"
    f"**{series_line}**\n\n"
    "**Note:** I might not be correct, but this is my best guess."
        )
    
        await status.edit(formatted_output)

    except Exception as e:
        await status.edit(f"❌ **Error occurred:**\n`{str(e)}`") 
