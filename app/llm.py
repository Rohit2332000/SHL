import json
from groq import Groq

from app.config import GROQ_API_KEY, MODEL_NAME


class GroqLLM:
    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.2,
    ) -> str:
        """
        Generic text generation.
        """

        response = self.client.chat.completions.create(
            model=MODEL_NAME,
            temperature=temperature,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
        )

        return response.choices[0].message.content.strip()

    def generate_json(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> dict:
        """
        Ask Groq to return ONLY JSON.
        """

        response = self.generate(
            system_prompt,
            user_prompt,
            temperature=0,
        )

        try:
            return json.loads(response)
        except Exception:
            return {}

    def generate_reply(
        self,
        prompt: str,
    ) -> str:
        """
        Used for recommendation explanations.
        """

        response = self.client.chat.completions.create(
            model=MODEL_NAME,
            temperature=0.3,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response.choices[0].message.content.strip()


llm = GroqLLM()