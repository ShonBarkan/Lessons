import google.generativeai as genai
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('chat_server.log'),
        logging.StreamHandler()
    ]
)

# Load environment variables
load_dotenv()

class GeminiChat:
    def __init__(self):
        # Configure the Gemini API
        genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        self.chat = None
        logging.info("GeminiChat initialized successfully")

    def start_new_chat(self):
        """Start a new chat session"""
        self.chat = self.model.start_chat(history=[])
        logging.info("New chat session started")
        return {"status": "success", "message": "New chat session started"}

    def send_message(self, message):
        """Send a message to Gemini and get response"""
        try:
            if not self.chat:
                self.start_new_chat()
            
            response = self.chat.send_message(message)
            logging.info(f"Message sent successfully: {message[:50]}...")
            return {
                "status": "success",
                "response": response.text
            }
        except Exception as e:
            logging.error(f"Error in send_message: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }

# Initialize Flask app
app = Flask(__name__, static_folder='static')
CORS(app)  # Enable CORS for all routes

# Initialize GeminiChat instance
gemini_chat = GeminiChat()

@app.route('/')
def index():
    """Serve the main chat interface"""
    return send_from_directory('static', 'index.html')

@app.route('/api/chat/start', methods=['POST'])
def start_chat():
    """Start a new chat session"""
    try:
        result = gemini_chat.start_new_chat()
        return jsonify(result)
    except Exception as e:
        logging.error(f"Error starting chat: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/chat/message', methods=['POST'])
def send_message():
    """Send a message to Gemini"""
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({"status": "error", "message": "No message provided"}), 400
        
        result = gemini_chat.send_message(data['message'])
        return jsonify(result)
    except Exception as e:
        logging.error(f"Error sending message: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

if __name__ == "__main__":
    logging.info("Starting Gemini Chat Server...")
    app.run(host='0.0.0.0', port=5000, debug=True) 