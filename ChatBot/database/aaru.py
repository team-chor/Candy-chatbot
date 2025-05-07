import google.generativeai as genai

class AaruGemini:
    SYSTEM_PROMPT = (
        "You are Umaru, an AI girlfriend..."
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
