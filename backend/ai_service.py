import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("models/gemini-flash-lite-latest")

def generate_reply(user_message):
    try:
        prompt = f"""
You are a concise ecommerce support assistant.

Store Info:
- Shipping: 3 - 7 business days
- Returns: 30 days
- Refunds: 5 - 7 business days
- Support: Mon-Fri, 9AM-6PM IST
- USA Shipping: Unavailable
- International Shipping: India only

User: {user_message}
"""

        response = model.generate_content(prompt)

        print("Gemini response received")

        if not response:
            return "Sorry, I couldn't generate a response."

        if hasattr(response, "text") and response.text:
            return response.text.strip()

        if hasattr(response, "candidates") and response.candidates:
            candidate = response.candidates[0]

            if candidate.content and candidate.content.parts:
                return candidate.content.parts[0].text.strip()

        return "Sorry, I couldn't understand that. Please try again."

    except Exception as e:
        print("GEMINI ERROR:", e)
        return "Sorry, I'm temporarily unavailable. Please try again."