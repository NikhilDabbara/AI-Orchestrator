# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from Database.database import create_session, add_message, get_recent_history, get_all_sessions, delete_session 
# from Agents.ollama_coder import ask_ollama
# from Agents.gemini_coder import ask_gemini
# from Agents.groq_router import route_prompt
# from Agents.gemini_compressor import compress_history

# app = FastAPI(title="AI Orchestrator API")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Allows all origins (good for local testing)
#     allow_credentials=True,
#     allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
#     allow_headers=["*"],
# )

# class SessionRequest(BaseModel):
#     session_name: str

# class ChatRequest(BaseModel):
#     session_id: int
#     message: str

# # @app.get("/")
# # def read_root():
# #     return {"status": "Server is running!", "message": "Welcome to the AI Orchestrator API"}

# # @app.post("/api/sessions")
# # def create_new_session(request: SessionRequest):
# #     """Creates a new session in the database."""
# #     session_id = create_session(request.session_name)
# #     if not session_id:
# #         raise HTTPException(status_code=500, detail="Failed to create session in database.")
    
# #     return {"session_id": session_id, "session_name": request.session_name}

# @app.get("/")
# def read_root():
#     return {"status": "Server is running!"}

# @app.get("/sessions")
# def fetch_all_sessions():
#     """Returns all sessions for the UI sidebar."""
#     return get_all_sessions()

# @app.post("/sessions")
# def create_new_session(request: SessionRequest):
#     """Creates a new session in the database."""
#     session_id = create_session(request.session_name)
#     if not session_id:
#         raise HTTPException(status_code=500, detail="Failed to create session in database.")
    
#     return {"session_id": session_id, "session_name": request.session_name}

# @app.delete("/sessions/{session_id}")
# def delete_session_endpoint(session_id: int):
#     """Deletes a session."""
#     success = delete_session(session_id)
#     if not success:
#         raise HTTPException(status_code=500, detail="Failed to delete session.")
#     return {"status": "deleted"}

# @app.get("/history/{session_id}")
# def get_session_history(session_id: int):
#     """Returns the chat history for a specific session."""
#     # We increase the limit here so the UI can load a good amount of past messages
#     return get_recent_history(session_id, limit=50)

# @app.post("/api/chat")
# def chat_endpoint(request: ChatRequest):
#     """Handles the core AI conversational loop."""
    
#     # 1. Fetch History
#     raw_history = get_recent_history(request.session_id, limit=5)

#     # 2. Build the context string
#     raw_history_string = "This is the conversation history:\n"
#     for msg in raw_history:
#         role = msg["role"].upper()
#         content = msg["content"]
#         raw_history_string += f"[{role}]: {content}\n"

#     # 3. Compress if too long
#     if len(raw_history) > 2:
#         prompt_context = compress_history(raw_history_string)
#     else:
#         prompt_context = raw_history_string

#     # 4. Append the new message
#     prompt_context += f"\n[USER]: {request.message}\n[ASSISTANT]: "

#     # 5. Route the task
#     print(f"Routing task for message: '{request.message}'...")
#     decision = route_prompt(request.message)
#     print(f"Groq decided to use: {decision.upper()}")

#     # 6. Execute Agent
#     if decision == "ollama":
#         agent_response = ask_ollama(prompt_context, "qwen2.5-coder:7b")
#     else:
#         agent_response = ask_gemini(prompt_context)

#     # 7. Save to Database
#     add_message(request.session_id, "user", request.message)
#     add_message(request.session_id, "assistant", agent_response)

#     # 8. Return the data to the frontend
#     return {
#         "session_id": request.session_id,
#         "route_used": decision,
#         "response": agent_response
#     }





from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import traceback # <--- NEW IMPORT FOR ERROR DEBUGGING

# Import our custom logic
from Database.database import create_session, add_message, get_recent_history, get_all_sessions, delete_session
from Agents.ollama_coder import ask_ollama
from Agents.gemini_coder import ask_gemini
from Agents.groq_router import route_prompt
from Agents.gemini_compressor import compress_history

# Initialize the application
app = FastAPI(title="AI Orchestrator API")

# --- CORS SETUP ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Data Models ---
class SessionRequest(BaseModel):
    session_name: str

class ChatRequest(BaseModel):
    session_id: int
    message: str

# --- Routes ---

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
        # 1. Fetch History
        raw_history = get_recent_history(request.session_id, limit=5)

        # 2. Build the context string
        raw_history_string = "This is the conversation history:\n"
        for msg in raw_history:
            role = msg["role"].upper()
            content = msg["content"]
            raw_history_string += f"[{role}]: {content}\n"

        # 3. Compress if too long
        if len(raw_history) > 2:
            prompt_context = compress_history(raw_history_string)
        else:
            prompt_context = raw_history_string

        # 4. Append the new message
        prompt_context += f"\n[USER]: {request.message}\n[ASSISTANT]: "

        # 5. Route the task
        print(f"Routing task for message: '{request.message}'...")
        decision = route_prompt(request.message)
        print(f"Groq decided to use: {decision.upper()}")

        # 6. Execute Agent
        if decision == "ollama":
            agent_response = ask_ollama(prompt_context, "qwen2.5-coder:7b")
        else:
            agent_response = ask_gemini(prompt_context)

        # 7. Save to Database
        add_message(request.session_id, "user", request.message)
        add_message(request.session_id, "assistant", agent_response)

        # 8. Return the data to the frontend
        return {
            "session_id": request.session_id,
            "route_used": decision,
            "response": agent_response
        }
    except Exception as e:
        print("\n=== ERROR IN CHAT ENDPOINT ===")
        traceback.print_exc() # Prints the exact red error to your terminal
        print("==============================\n")
        # Send the exact Python error back to the web browser!
        raise HTTPException(status_code=500, detail=f"Backend Error: {str(e)}")