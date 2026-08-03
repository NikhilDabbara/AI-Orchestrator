import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

def ask_gemini(user_prompt: str)->str:
    gemini_API = os.environ.get("GEMINI_API_KEY")
    if not gemini_API:
        return "Error: No Gemini API Key found."

    try:
        client = genai.Client(api_key = gemini_API)

        system_instruction = (
            "You are an expert AI assistant. Your role is to provide clear, "
            "insightful, and accurate answers for general knowledge, writing, "
            "research, and reasoning tasks. Provide well-formatted and easy-to-read responses."
        )

        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=f"{system_instruction}\n\nUser Prompt:\n{user_prompt}"
        )

        return response.text
                
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return f"Error communicating with Gemini: {e}"