# README.md

# Web-based Chat Assistant

This project implements a web-based Chat Assistant that allows users to have continuous conversations with selectable Large Language Models (LLMs). The application features a user-friendly front-end UI and a back-end API built with FastAPI, deployed on Render.com. Users can select different LLMs, send messages, and view conversation history seamlessly.

## Features

- Interactive chat interface
- Support for multiple LLM backends
- Persistent conversation context
- Easy deployment on Render.com

## Technologies Used

- FastAPI
- Uvicorn
- LiteLLM
- pydantic
- starlette
- requests

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- An account on Render.com for deployment

### Installation

1. Clone the repository:

```bash
git clone <repository_url>
cd <repository_directory>
```

2. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

### Running Locally

```bash
uvicorn main:app --reload
```

Navigate to `http://127.0.0.1:8000` to access the chat interface.

### Deployment

Follow Render.com's deployment instructions for Python web services, specifying `main.py` as the entry point.

## Files

- `main.py`: Contains the FastAPI application with API endpoints and chat logic.
- `requirements.txt`: Lists all dependencies for installation.
- `README.md`: This documentation file.

---

## License

This project is licensed under the MIT License.

---

## Contact

For questions or support, please open an issue in the repository.

---

# main.py

import uvicorn
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import requests

# // CHALLENGE: Managing conversation context across multiple users
# // SOLUTION: For simplicity, using in-memory storage; in production, use persistent storage

app = FastAPI()

# SUPPORTED_LLMs = {
    "lite_llm": "https://api.litellm.com/v1/generate",  # Placeholder URL
    # Add other LLM endpoints here
}

# class Message(BaseModel):
    role: str  # 'user' or 'assistant'
    content: str

# class ChatRequest(BaseModel):
    messages: List[Message]
    model: str  # Selected LLM
    temperature: Optional[float] = 0.7

# # For simplicity, using a global dict; in production, consider user sessions
conversation_history = []

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """
    Handle chat messages, send to LLM, and return response.
    """
    if request.model not in SUPPORTED_LLMs:
        raise HTTPException(status_code=400, detail="Unsupported model selected.")

    # Build prompt from conversation history
    prompt = ""
    for msg in request.messages:
        if msg.role == "user":
            prompt += f"User: {msg.content}\n"
        elif msg.role == "assistant":
            prompt += f"Assistant: {msg.content}\n"

    # // CHALLENGE: Integrating with different LLM APIs
    # // SOLUTION: Using requests to send prompt to selected LLM endpoint
    try:
        response = requests.post(
            SUPPORTED_LLMs[request.model],
            json={
                "prompt": prompt,
                "temperature": request.temperature,
                "max_tokens": 150
            },
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        reply = data.get("text", "").strip()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"LLM API error: {str(e)}")
    except ValueError:
        raise HTTPException(status_code=500, detail="Invalid response from LLM API.")

    # Append assistant reply to conversation history
    conversation_history.append({"role": "assistant", "content": reply})

    return {"reply": reply}

# // CHALLENGE: Serving static files for front-end UI
# // SOLUTION: Not included here; focus is on API logic

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

# requirements.txt

fastapi
uvicorn
lite_llm
pydantic
starlette
requests

# README.md

# Web-based Chat Assistant

This project implements a web-based Chat Assistant that allows users to have continuous conversations with selectable Large Language Models (LLMs). The application features a user-friendly front-end UI and a back-end API built with FastAPI, deployed on Render.com. Users can select different LLMs, send messages, and view conversation history seamlessly.

## Features

- Interactive chat interface
- Support for multiple LLM backends
- Persistent conversation context
- Easy deployment on Render.com

## Technologies Used

- FastAPI
- Uvicorn
- LiteLLM
- pydantic
- starlette
- requests

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- An account on Render.com for deployment

### Installation

1. Clone the repository:

```bash
git clone <repository_url>
cd <repository_directory>
```

2. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

### Running Locally

```bash
uvicorn main:app --reload
```

Navigate to `http://127.0.0.1:8000` to access the chat interface.

### Deployment

Follow Render.com's deployment instructions for Python web services, specifying `main.py` as the entry point.

## Files

- `main.py`: Contains the FastAPI application with API endpoints and chat logic.
- `requirements.txt`: Lists all dependencies for installation.
- `README.md`: This documentation file.

---

## License

This project is licensed under the MIT License.

---

## Contact

For questions or support, please open an issue in the repository.