import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions

# Initialize the Chroma Client
client = chromadb.PersistentClient(path="./chroma_data")

# Setup the Embedding Function
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

# Get or Create our Collection
try:
    memory_collection = client.get_or_create_collection(
        name="global_memory",
        embedding_function=sentence_transformer_ef
    )
except Exception as e:
    print(f"Error initializing ChromaDB: {e}")
    memory_collection = None

def add_to_memory(session_id: int, role: str, content: str):
    """Saves a message to the vector database for future searching."""
    if memory_collection is None:
        return False
        
    try:
        import time
        doc_id = f"sess_{session_id}_{int(time.time() * 1000)}"
        
        document = f"[{role.upper()}]: {content}"
        
        memory_collection.add(
            documents=[document],
            metadatas=[{"session_id": session_id, "role": role}],
            ids=[doc_id]
        )
        print(f"✅ Saved to ChromaDB: {doc_id}")
        return True
    except Exception as e:
        print(f"❌ Error adding to ChromaDB: {e}")
        return False

def search_memory(query: str, n_results: int = 3):
    """Searches the database for messages related to the query."""
    if memory_collection is None:
        return []
        
    try:
        # BUG FIX: Count the documents first to prevent crashes!
        count = memory_collection.count()
        if count == 0:
            print("ChromaDB is empty! Nothing to search yet.")
            return []
            
        # If we ask for 3 but only have 1, safely ask for 1 instead.
        safe_n_results = min(n_results, count)
        
        results = memory_collection.query(
            query_texts=[query],
            n_results=safe_n_results
        )
        
        if results and "documents" in results and len(results["documents"][0]) > 0:
            return results["documents"][0]
        return []
    except Exception as e:
        print(f"❌ Error searching ChromaDB: {e}")
        return []