from motor.motor_asyncio import AsyncIOMotorClient
import config

# Database connection
ChatBot = AsyncIOMotorClient(config.MONGO_URL)
db = ChatBot["ChatBot"]  # Database
usersdb = db["users"]    # Users Collection
chatsdb = db["chats"]    # Chats Collection

# Import functions for use in other parts of the application
from .chats import *
from .admin import *
from .fsub import *
from .aaru import *
from .chatbot import *
from ChatBot.aaru_gemini import AaruGemini

chatbot_api = AaruGemini(api_key="AIzaSyCmZYuxe4JeEbGURuJa6jPoQNvt677tp0E")
