import os
from openai import OpenAI

class TranslationService:
    def __init__(self):
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) # TODO: Load API key securely

    async def translate_to_urdu(self, text: str) -> str:
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo", # TODO: Make model configurable
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that translates English to Urdu."},
                    {"role": "user", "content": f"Translate the following English text to Urdu: {text}"}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error translating text: {e}")
            return "Translation service currently unavailable."
