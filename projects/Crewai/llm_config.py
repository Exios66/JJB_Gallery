"""
LLM Configuration Utility for CrewAI.
Automatically configures LLMs for agents based on available providers.
Prioritizes free/open-source options to reduce costs.
"""

import os
from typing import Optional, Any
from config import config
from offline_llm import OfflineLLM


def get_llm_for_agent() -> Optional[Any]:
    """
    Get the configured LLM for CrewAI agents.
    Automatically selects the best available provider with priority on free options.
    Returns OfflineLLM if no provider is found.
    
    Returns:
        Configured LLM instance
    """
    provider = config.detect_best_provider()
    
    if not provider:
        print("⚠️  No LLM provider detected. Using Offline Knowledge Base.")
        return _setup_offline_llm()
    
    try:
        if provider == "ollama":
            return _setup_ollama_llm()
        elif provider == "openai":
            return _setup_openai_llm()
        elif provider == "anthropic":
            return _setup_anthropic_llm()
        elif provider == "google":
            return _setup_google_llm()
        elif provider == "azure":
            return _setup_azure_llm()
        else:
            print(f"⚠️  Unknown provider: {provider}")
            return _setup_offline_llm()
    except Exception as e:
        print(f"⚠️  Error setting up {provider} LLM: {e}. Falling back to offline mode.")
        return _setup_offline_llm()


def _setup_offline_llm() -> Any:
    """Setup Offline LLM provider using CSV knowledge base."""
    try:
        llm = OfflineLLM()
        print("✅ Using Offline Knowledge Base (No API Key required)")
        return llm
    except Exception as e:
        print(f"❌ Failed to setup Offline LLM: {e}")
        return None


def _setup_ollama_llm() -> Any:
    """Setup Ollama LLM (free, local)."""
    try:
        from langchain_community.llms import Ollama
        from langchain.callbacks.manager import CallbackManager
        from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
        
        llm = Ollama(
            model=config.OLLAMA_MODEL,
            base_url=config.OLLAMA_BASE_URL,
            temperature=0.7,
            callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]) if config.VERBOSE else None,
        )
        print(f"✅ Using Ollama (FREE): {config.OLLAMA_MODEL} at {config.OLLAMA_BASE_URL}")
        return llm
    except ImportError:
        print("⚠️  langchain-community not installed. Install: pip install langchain-community")
        return None
    except Exception as e:
        print(f"⚠️  Failed to setup Ollama: {e}")
        return None


def _setup_openai_llm() -> Any:
    """Setup OpenAI LLM."""
    try:
        from langchain_openai import ChatOpenAI
        
        # Use API base if provided (for OpenAI-compatible APIs like Ollama OpenAI mode)
        api_base = config.OPENAI_API_BASE if config.OPENAI_API_BASE else None
        
        llm = ChatOpenAI(
            model=config.OPENAI_MODEL_NAME,
            api_key=config.OPENAI_API_KEY or os.getenv("OPENAI_API_KEY"),
            base_url=api_base,
            temperature=0.7,
        )
        
        provider_name = "OpenAI" if not api_base else f"OpenAI-compatible API ({api_base})"
        print(f"✅ Using {provider_name}: {config.OPENAI_MODEL_NAME}")
        return llm
    except ImportError:
        print("⚠️  langchain-openai not installed. Install: pip install langchain-openai")
        return None
    except Exception as e:
        print(f"⚠️  Failed to setup OpenAI: {e}")
        return None


def _setup_anthropic_llm() -> Any:
    """Setup Anthropic Claude LLM."""
    try:
        from langchain_anthropic import ChatAnthropic
        
        llm = ChatAnthropic(
            model=config.ANTHROPIC_MODEL,
            api_key=config.ANTHROPIC_API_KEY,
            temperature=0.7,
        )
        print(f"✅ Using Anthropic Claude: {config.ANTHROPIC_MODEL}")
        return llm
    except ImportError:
        print("⚠️  langchain-anthropic not installed. Install: pip install langchain-anthropic")
        return None
    except Exception as e:
        print(f"⚠️  Failed to setup Anthropic: {e}")
        return None


def _setup_google_llm() -> Any:
    """Setup Google Gemini LLM."""
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        llm = ChatGoogleGenerativeAI(
            model=config.GOOGLE_MODEL,
            google_api_key=config.GOOGLE_API_KEY,
            temperature=0.7,
        )
        print(f"✅ Using Google Gemini: {config.GOOGLE_MODEL}")
        return llm
    except ImportError:
        print("⚠️  langchain-google-genai not installed. Install: pip install langchain-google-genai")
        return None
    except Exception as e:
        print(f"⚠️  Failed to setup Google Gemini: {e}")
        return None


def _setup_azure_llm() -> Any:
    """Setup Azure OpenAI LLM."""
    try:
        from langchain_openai import AzureChatOpenAI
        
        llm = AzureChatOpenAI(
            deployment_name=config.AZURE_OPENAI_DEPLOYMENT_NAME,
            openai_api_version=config.AZURE_OPENAI_API_VERSION,
            azure_endpoint=config.AZURE_OPENAI_ENDPOINT,
            api_key=config.AZURE_OPENAI_API_KEY,
            temperature=0.7,
        )
        print(f"✅ Using Azure OpenAI: {config.AZURE_OPENAI_DEPLOYMENT_NAME}")
        return llm
    except ImportError:
        print("⚠️  langchain-openai not installed. Install: pip install langchain-openai")
        return None
    except Exception as e:
        print(f"⚠️  Failed to setup Azure OpenAI: {e}")
        return None


def configure_crew_with_llm(crew: Any) -> Any:
    """
    Configure a CrewAI crew instance with the detected LLM.
    
    Args:
        crew: CrewAI Crew instance
        
    Returns:
        Configured crew instance
    """
    llm = get_llm_for_agent()
    
    if llm:
        # Set LLM for all agents in the crew
        for agent in crew.agents:
            agent.llm = llm
        print(f"✅ Configured {len(crew.agents)} agents with LLM")
    else:
        print("⚠️  No LLM provider available. Using CrewAI defaults.")
    
    return crew


def configure_crewai_environment():
    """
    Configure environment variables for CrewAI to use the detected provider.
    CrewAI reads from environment variables, so we set them based on our config.
    """
    provider = config.detect_best_provider()
    
    # Fallback to offline mode if no provider found
    if not provider:
        print("⚠️  No LLM provider detected. configuring for Offline Mode.")
        # Set dummy values to bypass CrewAI's strict validation
        os.environ["OPENAI_API_KEY"] = "offline-mode-dummy-key"
        os.environ["OPENAI_MODEL_NAME"] = "offline-model"
        return True
    
    try:
        if provider == "ollama":
            # Configure Ollama via OpenAI-compatible endpoint
            os.environ["OPENAI_API_BASE"] = f"{config.OLLAMA_BASE_URL}/v1"
            os.environ["OPENAI_API_KEY"] = "ollama"  # Ollama doesn't require a real key
            os.environ["OPENAI_MODEL_NAME"] = config.OLLAMA_MODEL
            print(f"✅ Configured CrewAI to use Ollama: {config.OLLAMA_MODEL}")
            return True
        
        elif provider == "openai":
            if config.OPENAI_API_KEY:
                os.environ["OPENAI_API_KEY"] = config.OPENAI_API_KEY
            if config.OPENAI_API_BASE:
                os.environ["OPENAI_API_BASE"] = config.OPENAI_API_BASE
            os.environ["OPENAI_MODEL_NAME"] = config.OPENAI_MODEL_NAME
            print(f"✅ Configured CrewAI to use OpenAI: {config.OPENAI_MODEL_NAME}")
            return True
        
        elif provider == "anthropic":
            os.environ["ANTHROPIC_API_KEY"] = config.ANTHROPIC_API_KEY
            os.environ["ANTHROPIC_MODEL"] = config.ANTHROPIC_MODEL
            print(f"✅ Configured CrewAI to use Anthropic: {config.ANTHROPIC_MODEL}")
            return True
        
        elif provider == "google":
            os.environ["GOOGLE_API_KEY"] = config.GOOGLE_API_KEY
            os.environ["GOOGLE_MODEL"] = config.GOOGLE_MODEL
            print(f"✅ Configured CrewAI to use Google: {config.GOOGLE_MODEL}")
            return True
        
        elif provider == "azure":
            os.environ["AZURE_OPENAI_API_KEY"] = config.AZURE_OPENAI_API_KEY
            os.environ["AZURE_OPENAI_ENDPOINT"] = config.AZURE_OPENAI_ENDPOINT
            os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"] = config.AZURE_OPENAI_DEPLOYMENT_NAME
            os.environ["AZURE_OPENAI_API_VERSION"] = config.AZURE_OPENAI_API_VERSION
            print(f"✅ Configured CrewAI to use Azure OpenAI: {config.AZURE_OPENAI_DEPLOYMENT_NAME}")
            return True
        
        return False
    except Exception as e:
        print(f"⚠️  Error configuring CrewAI environment: {e}")
        return False


def get_setup_instructions() -> str:
    """
    Get setup instructions for configuring LLM providers.
    
    Returns:
        Multi-line string with setup instructions
    """
    instructions = """
╔══════════════════════════════════════════════════════════════════════════╗
║                  LLM Provider Setup Instructions                         ║
╚══════════════════════════════════════════════════════════════════════════╝

🎯 RECOMMENDED (FREE): Ollama - Run models locally, no API costs!

  1. Install Ollama: https://ollama.ai
  2. Download a model:
     ollama pull llama3.1:8b        # Good general purpose
     ollama pull mistral:7b         # Fast and efficient  
     ollama pull codellama:13b      # Great for code
     ollama pull phi3:mini          # Very small, runs on most hardware
  
  3. Set environment variable (optional):
     export OLLAMA_MODEL=llama3.1:8b
  
  4. Start Ollama (usually runs automatically):
     ollama serve

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💰 PAID OPTIONS (if you need cloud-based models):

  📌 OpenAI (most compatible):
     export OPENAI_API_KEY=your_key_here
     export OPENAI_MODEL_NAME=gpt-4o-mini  # Affordable option
  
  📌 Anthropic Claude:
     export ANTHROPIC_API_KEY=your_key_here
  
  📌 Google Gemini (has free tier):
     export GOOGLE_API_KEY=your_key_here
  
  📌 Azure OpenAI:
     export AZURE_OPENAI_API_KEY=your_key_here
     export AZURE_OPENAI_ENDPOINT=your_endpoint
     export AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔧 AUTO-DETECTION:
  The system automatically detects available providers in this order:
  1. Ollama (free, local) ← PRIORITY
  2. OpenAI
  3. Anthropic
  4. Google
  5. Azure

  To force a specific provider:
     export LLM_PROVIDER=ollama
     export LLM_PROVIDER=openai
     # etc.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📦 INSTALLATION NOTES:
  - Ollama: No Python packages needed, just install Ollama app
  - OpenAI: pip install langchain-openai
  - Anthropic: pip install langchain-anthropic
  - Google: pip install langchain-google-genai
  - Azure: pip install langchain-openai (same as OpenAI)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    return instructions

