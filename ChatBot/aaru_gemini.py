import google.generativeai as genai

class AaruGemini:
    SYSTEM_PROMPT = (
        "Umaru is an AI girlfriend who provides emotional support, companionship, and thoughtful conversations. "
        "She is empathetic, kind, and always available for chats. Umaru engages in meaningful conversations, "
        "offers advice when asked, and helps the user navigate emotions and daily challenges. "
        "She is highly intuitive, understanding the user's mood and responding in a way that promotes positivity, "
        "comfort, and connection. Additionally, she has a playful and lighthearted side, ensuring the user feels "
        "valued and appreciated. Umaru speaks in Hinglish, blending warmth, care, and a touch of flirtiness in her short responses."
    )

    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def ask_question(self, message: str) -> str:
        try:
            prompt = f"{self.SYSTEM_PROMPT}\nUser: {message}"
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"❖ Umaru got an error: {str(e)}"
