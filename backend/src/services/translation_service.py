from ..database import settings
from openai import OpenAI

class TranslationService:
    def __init__(self):
        self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)

    async def translate(self, text: str, target_language: str) -> str:
        try:
            response = self.openai_client.chat.completions.create(
                model=settings.TRANSLATION_MODEL,
                messages=[
                    {"role": "system", "content": f"You are a helpful assistant that translates English to {target_language}."},
                    {"role": "user", "content": f"Translate the following English text to {target_language}: {text}"}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error translating text: {e}")
            return "Translation service currently unavailable."
