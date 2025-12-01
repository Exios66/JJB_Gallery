# iOS-Inspired Chatbot

A modern, iOS-style chat interface built with Streamlit. This application provides a beautiful, native iOS-like chat experience in your web browser.

## 🎨 Features

- **iOS-Style Design**: Beautiful, native iOS-inspired UI with smooth animations
- **OpenAI Integration**: Powered by OpenAI's GPT models
- **Real-time Chat**: Instant responses with typing indicators
- **Message History**: Persistent conversation history
- **Customizable**: Easy model selection and API key configuration
- **Responsive**: Works on desktop and mobile devices

## 📋 Prerequisites

- Python 3.8+
- OpenAI API key (or compatible API)

## 🛠️ Installation

1. **Clone and navigate to the project:**
   ```bash
   cd projects/ios_chatbot
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment (optional):**
   ```bash
   cp .env.example .env
   # Edit .env with your OpenAI API key
   ```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key_here
DEFAULT_MODEL=gpt-3.5-turbo
```

Or set the API key directly in the Streamlit app's sidebar.

## 🚀 Usage

### Start the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### Using the Chat Interface

1. **Configure API Key**: Enter your OpenAI API key in the sidebar
2. **Select Model**: Choose from GPT-3.5-turbo, GPT-4, or GPT-4-turbo
3. **Start Chatting**: Type your message and press Enter
4. **Clear Chat**: Use the "Clear Chat" button to start a new conversation

## 🎯 Features in Detail

### iOS-Style Design Elements

- **Bubble Messages**: User messages appear as blue bubbles on the right
- **Bot Messages**: Assistant messages appear as gray bubbles on the left
- **Smooth Animations**: Fade-in animations for new messages
- **Timestamps**: Each message includes a timestamp
- **Gradient Background**: Beautiful gradient background

### Model Support

- **GPT-3.5-turbo**: Fast and cost-effective
- **GPT-4**: More capable but slower
- **GPT-4-turbo-preview**: Latest GPT-4 variant

## 📦 Project Structure

```
ios_chatbot/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── .env.example       # Environment template
└── README.md          # This file
```

## 🔧 Customization

### Changing Colors

Edit the CSS in `app.py`:

```python
.user-message {
    background: #007AFF;  # Change to your preferred color
}
```

### Adding New Models

Add models to the selectbox in the sidebar:

```python
model = st.selectbox(
    "Model",
    ["gpt-3.5-turbo", "gpt-4", "your-custom-model"],
)
```

## 🐛 Troubleshooting

### API Key Issues

- Ensure your OpenAI API key is valid
- Check that you have sufficient credits
- Verify the API key is correctly entered (no extra spaces)

### Connection Errors

- Check your internet connection
- Verify OpenAI API status
- Try a different model if one fails

## 📚 API Usage

The app uses OpenAI's Chat Completions API:

```python
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages,
    temperature=0.7,
    max_tokens=500
)
```

## 🔒 Security

- API keys are stored in session state (not persisted)
- Never commit `.env` files to version control
- Use environment variables for production deployments

## 🚀 Deployment

### Streamlit Cloud

1. Push your code to GitHub
2. Connect your repo to [Streamlit Cloud](https://streamlit.io/cloud)
3. Add your `OPENAI_API_KEY` as a secret
4. Deploy!

### Docker

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

## 📄 License

This project is part of the JJB Gallery portfolio. See the main repository LICENSE file.

## 🔗 Related Projects

- [ChatUI](../ChatUi/README.md) - Full-featured chat interface
- [RAG Model](../RAG_Model/README.md) - Document-based Q&A
- [CrewAI](../Crewai/README.md) - Multi-agent system

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues or questions, please open an issue in the main repository.
