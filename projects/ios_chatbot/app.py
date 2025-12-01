#!/usr/bin/env python3
"""
iOS-Inspired Chatbot
A Flask-based chatbot with iOS-style UI and backend API.
"""

from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import os
import uuid
from datetime import datetime
from typing import Dict, List, Optional

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
CORS(app)

# In-memory storage (replace with database in production)
conversations: Dict[str, List[Dict]] = {}


class ChatBot:
    """Simple chatbot backend."""
    
    def __init__(self):
        self.name = "iOS Chatbot"
    
    def respond(self, message: str, conversation_id: str) -> str:
        """
        Generate a response to user message.
        Replace this with actual LLM integration.
        """
        # Simple rule-based responses (replace with LLM)
        message_lower = message.lower()
        
        if 'hello' in message_lower or 'hi' in message_lower:
            return "Hello! How can I help you today?"
        elif 'help' in message_lower:
            return "I'm here to help! You can ask me questions or just chat. What would you like to know?"
        elif 'bye' in message_lower or 'goodbye' in message_lower:
            return "Goodbye! Have a great day!"
        elif '?' in message:
            return "That's an interesting question! I'm still learning, but I'd love to help you explore that topic."
        else:
            return f"You said: '{message}'. I'm a simple chatbot - connect me to an LLM for more intelligent responses!"


chatbot = ChatBot()


@app.route('/')
def index():
    """Render the main chat interface."""
    return render_template('index.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages."""
    data = request.json
    message = data.get('message', '').strip()
    conversation_id = data.get('conversation_id')
    
    if not message:
        return jsonify({'error': 'Message is required'}), 400
    
    # Generate conversation ID if not provided
    if not conversation_id:
        conversation_id = str(uuid.uuid4())
    
    # Initialize conversation if new
    if conversation_id not in conversations:
        conversations[conversation_id] = []
    
    # Add user message
    user_message = {
        'role': 'user',
        'content': message,
        'timestamp': datetime.now().isoformat()
    }
    conversations[conversation_id].append(user_message)
    
    # Get bot response
    try:
        response = chatbot.respond(message, conversation_id)
    except Exception as e:
        response = f"Sorry, I encountered an error: {str(e)}"
    
    # Add bot response
    bot_message = {
        'role': 'assistant',
        'content': response,
        'timestamp': datetime.now().isoformat()
    }
    conversations[conversation_id].append(bot_message)
    
    return jsonify({
        'conversation_id': conversation_id,
        'response': bot_message,
        'message': user_message
    })


@app.route('/api/conversations/<conversation_id>', methods=['GET'])
def get_conversation(conversation_id: str):
    """Get conversation history."""
    if conversation_id not in conversations:
        return jsonify({'messages': []})
    
    return jsonify({
        'conversation_id': conversation_id,
        'messages': conversations[conversation_id]
    })


@app.route('/api/conversations', methods=['GET'])
def list_conversations():
    """List all conversations."""
    return jsonify({
        'conversations': [
            {
                'id': conv_id,
                'message_count': len(messages),
                'last_message': messages[-1]['timestamp'] if messages else None
            }
            for conv_id, messages in conversations.items()
        ]
    })


@app.route('/api/conversations/<conversation_id>', methods=['DELETE'])
def delete_conversation(conversation_id: str):
    """Delete a conversation."""
    if conversation_id in conversations:
        del conversations[conversation_id]
        return jsonify({'success': True})
    return jsonify({'error': 'Conversation not found'}), 404


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'ios-chatbot',
        'conversations': len(conversations)
    })


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)

