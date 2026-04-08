import os
from google import genai
from dotenv import load_dotenv
from backend.logger import get_logger

load_dotenv()
logger = get_logger()

class GeminiClient:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")

        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found")

        self.client = genai.Client(api_key=self.api_key)

    def get_response(self, prompt):
        try:
            logger.info("Sending request to Gemini API")

            response = self.client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=prompt
            )

            logger.info("Received response from Gemini API")

            return response.text

        except Exception as e:
            logger.error(f"Gemini API Error: {str(e)}")
            return None