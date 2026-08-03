from groq import Groq
from dotenv import load_dotenv
import os
import json
load_dotenv()
Groq_API = os.environ.get("GROQ_API_KEY")

client = Groq(api_key = Groq_API)

def route_prompt(user_prompt: str) -> str:
    system_prompt = (
        "You are a routing classifier. Given a user's prompt, decide which "
        "backend it should be routed to.\n\n"
        "- Route to 'ollama' if the prompt is about writing, debugging, explaining, "
        "or reviewing code, or any software/programming-related task.\n"
        "- Route to 'gemini' for all other general-purpose tasks (writing, research, "
        "reasoning, everyday questions, etc.).\n\n"
        "Respond ONLY with a JSON object in this exact format:\n"
        '{"route": "ollama"} or {"route": "gemini"}'
    )
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object"},
        temperature=0,
    )

    content = response.choices[0].message.content

    try:
        data = json.loads(content)
        route = data.get("route", "").strip().lower()
    except (json.JSONDecodeError, AttributeError):
        route = ""

    if route not in ("ollama", "gemini"):
        route = "gemini"

    return route


if __name__ == "__main__":
    print(route_prompt("Write a Python function to reverse a linked list"))  
    print(route_prompt("What's a good recipe for banana bread?"))  