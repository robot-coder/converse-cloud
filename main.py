import uvicorn
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from starlette.responses import JSONResponse
import requests
from typing import List, Optional

# CHALLENGE: Integrating LiteLLM for multiple LLM options
# SOLUTION: Placeholder for LLM selection; actual implementation depends on LiteLLM API

# Initialize FastAPI app
app = FastAPI()

# Define request and response models
class Message(BaseModel):
    role: str  # 'user' or 'assistant'
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    model: Optional[str] = "lite-llm"  # default model, can be extended
    temperature: Optional[float] = 0.7

class ChatResponse(BaseModel):
    reply: str

# Placeholder for LLM API endpoint or method
# DETAIL: Assuming LiteLLM provides a REST API or Python interface
# For demonstration, we'll mock the LLM response

def get_llm_response(messages: List[Message], model: str, temperature: float) -> str:
    """
    Send messages to the LLM and get a response.
    """
    # CHALLENGE: Actual integration with LiteLLM API
    # SOLUTION: Mock response for demonstration purposes
    # In production, replace with actual API call to LiteLLM
    try:
        # Example: If LiteLLM has a REST API, send a request here
        # response = requests.post("http://localhost:8000/api/generate", json={
        #     "messages": [msg.dict() for msg in messages],
        #     "model": model,
        #     "temperature": temperature
        # })
        # response.raise_for_status()
        # result = response.json()
        # return result.get("reply", "Sorry, I couldn't generate a response.")
        # For now, return a placeholder response
        last_user_message = next((msg.content for msg in reversed(messages) if msg.role == "user"), "")
        return f"Echo: {last_user_message}"
    except Exception as e:
        # Log error if needed
        raise RuntimeError(f"LLM response error: {str(e)}")

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Handle chat messages and return LLM response.
    """
    try:
        reply_text = get_llm_response(request.messages, request.model, request.temperature)
        return ChatResponse(reply=reply_text)
    except Exception as e:
        # Error handling: return HTTP 500 with error message
        raise HTTPException(status_code=500, detail=str(e))

# Optional: Root endpoint for health check
@app.get("/")
async def root():
    return {"message": "Chat Assistant API is running."}

# To run the server: uvicorn main:app --host 0.0.0.0 --port 8000
# Note: Deployment on Render.com will use this command or similar in startup script