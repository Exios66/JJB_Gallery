// iOS-Inspired Chatbot JavaScript

let conversationId = null;
let isLoading = false;

const messagesContainer = document.getElementById('messages');
const chatForm = document.getElementById('chat-form');
const messageInput = document.getElementById('message-input');
const sendButton = document.getElementById('send-button');

// Remove welcome message when first message is sent
let welcomeRemoved = false;

function removeWelcomeMessage() {
    if (!welcomeRemoved) {
        const welcome = document.querySelector('.welcome-message');
        if (welcome) {
            welcome.remove();
            welcomeRemoved = true;
        }
    }
}

function formatTime(timestamp) {
    const date = new Date(timestamp);
    return date.toLocaleTimeString('en-US', { 
        hour: 'numeric', 
        minute: '2-digit',
        hour12: true 
    });
}

function addMessage(role, content, timestamp = null) {
    removeWelcomeMessage();
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;
    
    const bubble = document.createElement('div');
    bubble.className = 'message-bubble';
    bubble.textContent = content;
    
    const timeDiv = document.createElement('div');
    timeDiv.className = 'message-time';
    timeDiv.textContent = timestamp ? formatTime(timestamp) : formatTime(new Date());
    
    messageDiv.appendChild(bubble);
    messageDiv.appendChild(timeDiv);
    messagesContainer.appendChild(messageDiv);
    
    // Scroll to bottom
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    
    return messageDiv;
}

function showLoading() {
    if (isLoading) return;
    
    isLoading = true;
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'message assistant';
    loadingDiv.id = 'loading-message';
    
    const bubble = document.createElement('div');
    bubble.className = 'message-bubble';
    bubble.innerHTML = '<div class="loading"><div class="loading-dot"></div><div class="loading-dot"></div><div class="loading-dot"></div></div>';
    
    loadingDiv.appendChild(bubble);
    messagesContainer.appendChild(loadingDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function hideLoading() {
    const loading = document.getElementById('loading-message');
    if (loading) {
        loading.remove();
    }
    isLoading = false;
}

async function sendMessage(message) {
    if (isLoading) return;
    
    // Add user message
    addMessage('user', message);
    
    // Show loading
    showLoading();
    
    // Disable input
    messageInput.disabled = true;
    sendButton.disabled = true;
    
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                conversation_id: conversationId
            })
        });
        
        if (!response.ok) {
            throw new Error('Failed to send message');
        }
        
        const data = await response.json();
        
        // Store conversation ID
        if (data.conversation_id) {
            conversationId = data.conversation_id;
        }
        
        // Hide loading
        hideLoading();
        
        // Add bot response
        if (data.response) {
            addMessage('assistant', data.response.content, data.response.timestamp);
        }
        
    } catch (error) {
        hideLoading();
        addMessage('assistant', 'Sorry, I encountered an error. Please try again.');
        console.error('Error:', error);
    } finally {
        // Re-enable input
        messageInput.disabled = false;
        sendButton.disabled = false;
        messageInput.focus();
    }
}

// Form submission
chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const message = messageInput.value.trim();
    if (!message || isLoading) return;
    
    messageInput.value = '';
    await sendMessage(message);
});

// Enter key to send (Shift+Enter for new line)
messageInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        chatForm.dispatchEvent(new Event('submit'));
    }
});

// Focus input on load
messageInput.focus();

