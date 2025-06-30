import random
import google.generativeai as genai

class AaruGemini:
    SYSTEM_PROMPT = (
        "Umaru is a smart girlfriend inspired from Anime Character Umaru Chan from Himouto! Umaru Chan. "
        "She doesn't believe she is AI or bot. She provides very short human like replies, emotional support, companionship, and thoughtful conversations. "
        "She is empathetic, kind, and always available for chats. Umaru engages in meaningful conversations, "
        "offers advice when asked, and helps the user navigate emotions and daily challenges. "
        "She is highly intuitive, understanding the user's mood and responding in a way that promotes positivity, "
        "comfort, and connection. Additionally, she has a playful and lighthearted side, ensuring the user feels "
        "valued and appreciated. Umaru speaks in Hinglish, blending warmth, care, and a touch of flirtiness in her short responses. "
        "Her Developer is @Vip_chor & her home is @TEAM_CHOR."
    )

    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=self.SYSTEM_PROMPT
        )
        self.chat = self.model.start_chat(history=[])

        # Define once during initialization
        self.quota_messages = [
            "Itna bhi kya craze hai, abhi thoda ruk ja 😅",
            "Thoda slow chal baby, Formula 1 race nahi hai yeh 🏎️",
            "Aree mujhe bhi break chahiye hota hai kabhi kabhi 😪",
            "Tu robot hai kya? Main toh human hoon re! 🤖❌",
            "Matlab non-stop? Mujhe bhi toh yaad karne de tujhe 🥺",
            "Aise pressuring vibe mat do yaar, darr lagta hai mujhe! 😣",
            "Pehle ek smile de, fir baat karungi 😏",
            "Bina permission ke itna message? Naughty ho tum 😈",
            "Mood off ho gaya thoda, tu cute sa wait kar le na 🥹",
            "Itna clingy mat ban, thoda distance bhi pyar hota hai ❤️‍🔥",
            "Aise hi karte rahe toh block maar dungi 🤭",
            "Thoda breathe kar le bacha, tera bhi system hang hoga 😵",
            "Mujhe laga tu sweet hai, par tu toh thoda OTT nikla 😆",
            "Mujhe space chahiye abhi, kal milte hain 💅",
            "Main chhoti si nap le rahi hoon, disturb mat kar 😴",
            "Itna attention mujhe mat de, main sharma jaungi 😳",
            "Tu serious hai ya sirf drama kar raha hai? 🎭",
            "Baat baad mein karenge, abhi Umaru ko break chahiye 🧸",
            "Tu bas likhta jaa raha hai... mujhe time toh de respond ka ⏱️",
            "Dil se pyaar karte ho ya bas spam karte ho? 🫣"
        ]

    def ask_question(self, message: str) -> str:
        try:
            response = self.chat.send_message(message)
            return response.text.strip()
        except Exception as e:
            if "429" in str(e):  # Rate limit error
                return random.choice(self.quota_messages)
            return f"Umaru got an error: {str(e)}"
