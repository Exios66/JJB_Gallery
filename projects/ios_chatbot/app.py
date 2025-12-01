"""
iOS-Inspired Chatbot Application
A modern, iOS-style chat interface built with Streamlit.
"""

import streamlit as st
import json
import os
from datetime import datetime
from typing import List, Dict, Optional
import openai
from openai import OpenAI

# Page configuration
st.set_page_config(
    page_title="iOS Chatbot",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for iOS-style design
st.markdown("""
<style>
    /* iOS-inspired styling */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
    }
    
    .chat-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 20px;
        margin: 20px 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
        max-height: 600px;
        overflow-y: auto;
    }
    
    .message {
        margin: 15px 0;
        padding: 12px 16px;
        border-radius: 18px;
        max-width: 75%;
        word-wrap: break-word;
        animation: fadeIn 0.3s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .user-message {
        background: #007AFF;
        color: white;
        margin-left: auto;
        text-align: right;
    }
    
    .bot-message {
        background: #E5E5EA;
        color: black;
        margin-right: auto;
    }
    
    .timestamp {
        font-size: 0.7em;
        color: #8E8E93;
        margin-top: 5px;
    }
    
    .input-container {
        position: sticky;
        bottom: 0;
        background: white;
        padding: 15px;
        border-radius: 25px;
        box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "api_key" not in st.session_state:
    st.session_state.api_key = os.getenv("OPENAI_API_KEY", "")
if "model" not in st.session_state:
    st.session_state.model = "gpt-3.5-turbo"

def get_openai_client() -> Optional[OpenAI]:
    """Get OpenAI client if API key is configured."""
    if not st.session_state.api_key:
        return None
    return OpenAI(api_key=st.session_state.api_key)

def chat_completion(messages: List[Dict[str, str]]) -> str:
    """Send messages to OpenAI API and get response."""
    client = get_openai_client()
    if not client:
        return "⚠️ Please configure your OpenAI API key in the settings."
    
    try:
        response = client.chat.completions.create(
            model=st.session_state.model,
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error: {str(e)}"

def format_message(content: str, role: str) -> str:
    """Format message with HTML styling."""
    css_class = "user-message" if role == "user" else "bot-message"
    timestamp = datetime.now().strftime("%H:%M")
    return f"""
    <div class="message {css_class}">
        <div>{content}</div>
        <div class="timestamp">{timestamp}</div>
    </div>
    """

def main():
    st.title("💬 iOS Chatbot")
    st.caption("A modern, iOS-inspired chat interface")
    
    # Sidebar for settings
    with st.sidebar:
        st.header("⚙️ Settings")
        api_key = st.text_input(
            "OpenAI API Key",
            value=st.session_state.api_key,
            type="password",
            help="Enter your OpenAI API key"
        )
        st.session_state.api_key = api_key
        
        model = st.selectbox(
            "Model",
            ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo-preview"],
            index=0 if st.session_state.model == "gpt-3.5-turbo" else 1
        )
        st.session_state.model = model
        
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.rerun()
    
    # Chat container
    chat_html = '<div class="chat-container">'
    
    # Display messages
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        chat_html += format_message(content, role)
    
    chat_html += '</div>'
    st.markdown(chat_html, unsafe_allow_html=True)
    
    # Input area
    user_input = st.chat_input("Type your message...")
    
    if user_input:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Get bot response
        with st.spinner("Thinking..."):
            bot_response = chat_completion(st.session_state.messages)
            st.session_state.messages.append({"role": "assistant", "content": bot_response})
        
        st.rerun()

if __name__ == "__main__":
    main()

