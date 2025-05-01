# Gemini Chat Web Application

A web-based chat application using Google's Gemini AI model.

## Features

- Modern, responsive web interface
- Real-time chat with Gemini AI
- Typing indicators
- Error handling and logging
- CORS support
- Health check endpoint

## Setup

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with your Google API key:
```
GOOGLE_API_KEY=your_api_key_here
```

## Running the Application

1. Start the server:
```bash
python chat.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

## API Endpoints

- `GET /`: Serve the main chat interface
- `POST /api/chat/start`: Start a new chat session
- `POST /api/chat/message`: Send a message to Gemini
- `GET /api/health`: Health check endpoint

## Project Structure

```
gemini_chat/
├── chat.py              # Main server application
├── requirements.txt     # Python dependencies
├── static/
│   └── index.html      # Frontend interface
└── .env                # Environment variables (create this file)
```

## Logging

The application logs to both console and `chat_server.log` file. Logs include:
- Server startup/shutdown
- Chat session initialization
- Message sending/receiving
- Error handling

## Security Notes

- The application uses CORS for cross-origin requests
- API keys are stored in environment variables
- Input validation is performed on all API endpoints 