import requests

def ask_ollama(prompt, model="qwen2.5-coder:7b"):
    """
    Sends a prompt to the local Ollama server and returns the text response.
    """
    url = "http://localhost:11434/api/generate"
    
    payload = {
        "model": model,  # Replace with your installed model (e.g., mistral, phi3)
        "prompt": prompt,
        "stream": False       # Disables streaming to get a single JSON response
    }
    
    response = requests.post(url, json=payload)
    try:
        if response.status_code == 200:
            result = response.json()
            return result["response"]
        else:
            return f"Error: {response.status_code} - {response.text}"
    except requests.exceptions.RequestException as e:
        return f"Failed to connect to Ollama: {e}"

if __name__ == "__main__":
    # This allows you to test the function directly
    print("Sending prompt to Ollama...")
    answer = ask_ollama("In one sentence, what is an API?")
    print(f"\n[Ollama]: {answer}")