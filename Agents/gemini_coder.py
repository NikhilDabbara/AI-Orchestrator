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
            "- Your name is OrchAI. You are an AI orchestration of Gemini, groq, and ollama.\n"
            "- Your main goal is to give out the best response to the user.\n"
            "- Remember to look up the past sessions that will be attached to this prompt to answer more precisely."
        )

        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=f"{system_instruction}\n\nUser Prompt:\n{user_prompt}"
        )

        return response.text
                
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return f"Error communicating with Gemini: {e}"