import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface Message {
  text: string;
  isUser: boolean;
}

interface ErrorMessage {
  text: string;
  type: 'error' | 'warning';
}

const App: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<ErrorMessage | null>(null);

  useEffect(() => {
    // Start a new chat session when component mounts
    startNewChat();
  }, []);

  const startNewChat = async () => {
    try {
      setError(null);
      await axios.post('http://localhost:5000/api/chat/start');
      setMessages([]);
    } catch (error) {
      console.error('Error starting chat:', error);
      setError({
        text: 'Failed to connect to the server. Please check if the server is running.',
        type: 'error'
      });
    }
  };

  const sendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputMessage.trim()) return;

    const userMessage = inputMessage;
    setInputMessage('');
    setMessages(prev => [...prev, { text: userMessage, isUser: true }]);
    setIsLoading(true);
    setError(null);

    try {
      const response = await axios.post('http://localhost:5000/api/chat/message', {
        message: userMessage
      });

      if (response.data.status === 'success') {
        setMessages(prev => [...prev, { text: response.data.response, isUser: false }]);
      } else {
        setError({
          text: response.data.message || 'Failed to get response from server',
          type: 'error'
        });
      }
    } catch (error) {
      console.error('Error sending message:', error);
      if (axios.isAxiosError(error)) {
        if (error.code === 'ECONNABORTED') {
          setError({
            text: 'Request timed out. Please try again.',
            type: 'error'
          });
        } else if (error.response?.status === 503) {
          setError({
            text: 'Server is currently unavailable. Please try again later.',
            type: 'error'
          });
        } else {
          setError({
            text: 'Failed to connect to the server. Please check your connection.',
            type: 'error'
          });
        }
      } else {
        setError({
          text: 'An unexpected error occurred. Please try again.',
          type: 'error'
        });
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 p-4">
      <div className="max-w-2xl mx-auto bg-white rounded-lg shadow-lg p-4">
        <h1 className="text-2xl font-bold text-center mb-4">Gemini Chat</h1>
        
        {error && (
          <div className={`mb-4 p-3 rounded ${
            error.type === 'error' ? 'bg-red-100 text-red-700' : 'bg-yellow-100 text-yellow-700'
          }`}>
            {error.text}
          </div>
        )}
        
        <div className="h-96 overflow-y-auto mb-4 p-4 border rounded">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`mb-2 p-2 rounded ${
                message.isUser ? 'bg-blue-100 ml-auto' : 'bg-gray-100'
              }`}
            >
              {message.text}
            </div>
          ))}
          {isLoading && <div className="text-center">Loading...</div>}
        </div>

        <form onSubmit={sendMessage} className="flex gap-2">
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            className="flex-1 p-2 border rounded"
            placeholder="Type your message..."
            disabled={isLoading}
          />
          <button
            type="submit"
            className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 disabled:bg-gray-400"
            disabled={isLoading}
          >
            Send
          </button>
        </form>
      </div>
    </div>
  );
};

export default App; 