import os
from dotenv import load_dotenv 
from google import genai

load_dotenv()

def compress_history(history: str) -> str:

    gemini_API = os.environ.get("GEMINI_API_KEY")
    if not gemini_API:
        return "Error: No Gemini API Key found."
    
    try:
        client = genai.Client(api_key=gemini_API)
        
        system_instruction = (
            "You are an AI memory compressor. Read the following conversation history. "
            "Write a dense, highly compressed summary of the key facts, context, and "
            "user preferences. Do not exceed 3 sentences. Be concise."
        )

        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=f"{system_instruction}\n\nHistory to compress:\n{history}"
        )

        return response.text
        
    except Exception as e:
        print(f"Gemini Compression Error: {e}")
        return history
