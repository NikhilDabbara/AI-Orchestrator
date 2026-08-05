from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import traceback

# Import our custom logic
from Database.database import create_session, add_message, get_recent_history, get_all_sessions, delete_session
from Database.vector_db import search_memory
from Agents.ollama_coder import ask_ollama
from Agents.gemini_coder import ask_gemini
from Agents.groq_router import route_prompt
from Agents.gemini_compressor import compress_history

app = FastAPI(title="AI Orchestrator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SessionRequest(BaseModel):
    session_name: str

class ChatRequest(BaseModel):
    session_id: int
    message: str

@app.get("/")
def read_root():
    return {"status": "Server is running!"}

@app.get("/sessions")
def fetch_all_sessions():
    return get_all_sessions()

@app.post("/sessions")
def create_new_session(request: SessionRequest):
    session_id = create_session(request.session_name)
    if not session_id:
        raise HTTPException(status_code=500, detail="Failed to create session in database.")
    return {"session_id": session_id, "session_name": request.session_name}

@app.delete("/sessions/{session_id}")
def delete_session_endpoint(session_id: int):
    success = delete_session(session_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete session.")
    return {"status": "deleted"}

@app.get("/history/{session_id}")
def get_session_history(session_id: int):
    return get_recent_history(session_id, limit=50)

@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    try:
        System_Prompt = """
        - Your name is OrchAI. You are an AI orchestration of Gemini, groq, and ollama.
        - Your main goal is to give out the best response to the user.
        - Remember to look up the past sessions that will be attatched to this prompt to answer more precisely. 
        """
        # 1. Search Global Memory (ChromaDB)
        print(f"\n🔍 Searching memory for: '{request.message}'...")
        past_memories = search_memory(request.message, n_results=3)
        
        memory_string = ""
        if len(past_memories) > 0:
            memory_string = "RECALLED MEMORIES FROM PREVIOUS CHATS:\n"
            for mem in past_memories:
                memory_string += f"- {mem}\n"
            memory_string += "\n"
        else:
            print("No relevant memories found.")

        # 2. Fetch Recent History (MySQL)
        raw_history = get_recent_history(request.session_id, limit=5)

        raw_history_string = "RECENT CONVERSATION HISTORY:\n"
        for msg in raw_history:
            role = msg["role"].upper()
            content = msg["content"]
            raw_history_string += f"[{role}]: {content}\n"

        # 3. Compress History
        if len(raw_history) > 2:
            prompt_context = compress_history(raw_history_string)
        else:
            prompt_context = raw_history_string

        # 4. Build Final Payload
        final_payload = f"""
            {System_Prompt}
            {memory_string}
            {prompt_context}

            [USER]: {request.message}
            [ASSISTANT]: """

        # === THE MIND READER (Helps you debug!) ===
        print("\n=== WHAT THE AI ACTUALLY SEES ===")
        print(final_payload)
        print("=================================\n")
        # ==========================================

        # 5. Route the task
        decision = route_prompt(request.message)
        print(f"🚦 Groq decided to use: {decision.upper()}")

        # 6. Execute Agent
        if decision == "ollama":
            agent_response = ask_ollama(final_payload, "qwen2.5-coder:7b")
        else:
            agent_response = ask_gemini(final_payload)

        # 7. Save to Database
        add_message(request.session_id, "user", request.message)
        add_message(request.session_id, "assistant", agent_response)

        return {
            "session_id": request.session_id,
            "route_used": decision,
            "response": agent_response
        }
    except Exception as e:
        print("\n=== ERROR IN CHAT ENDPOINT ===")
        traceback.print_exc()
        print("==============================\n")
        raise HTTPException(status_code=500, detail=f"Backend Error: {str(e)}")