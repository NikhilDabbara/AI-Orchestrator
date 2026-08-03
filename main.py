from Database.database import create_session, add_message, get_recent_history
from Agents.ollama_coder import ask_ollama
from Agents.groq_router import route_prompt
from Agents.gemini_compressor import compress_history
from Agents.gemini_coder import ask_gemini

def main():
    session_id = create_session("Local Chat Test")
    if not session_id:
        print("Failed to connect to the database. Exiting.")
        return
    print(f"\n--- Chat Session Started (ID: {session_id}) ---")
    print("Type 'exit' to quit.\n")

    while True:
        user_text = input("You: ")
        if user_text.lower() == "exit":
            break

        raw_history = get_recent_history(session_id, limit=5)

        raw_history_string = "This is the conversation history:\n"
        
        for msg in raw_history:
            role = msg["role"].upper()
            content = msg["content"]
            
            raw_history_string += f"[{role}]: {content}\n"

        if len(raw_history) > 2:
            prompt_context = compress_history(raw_history_string)
        else:
            prompt_context = raw_history_string

        prompt_context += f"\n[USER]: {user_text}\n[ASSISTANT]: "

        print("Routing task...")
        decision = route_prompt(user_text)
        print(f"Groq decided to use: {decision.upper()}")

        if decision == "ollama":
            print("Ollama is thinking...")
            agent_response = ask_ollama(prompt_context, "qwen2.5-coder:7b")
        else:
            print("Routing to Gemini...")
            agent_response = ask_gemini(prompt_context)

        print(f"\nAI: {agent_response}\n")

        add_message(session_id, "user", user_text)
        add_message(session_id, "assistant", agent_response)

if __name__ == "__main__":
    main()