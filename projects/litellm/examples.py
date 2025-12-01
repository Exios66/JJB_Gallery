#!/usr/bin/env python3
"""
LiteLLM Usage Examples
Demonstrates various ways to use LiteLLM with different providers.
"""

import os
from typing import List, Dict

try:
    from litellm import completion, acompletion
    LITELLM_AVAILABLE = True
except ImportError:
    LITELLM_AVAILABLE = False
    print("Install LiteLLM: pip install litellm")


def example_openai():
    """Example: Using OpenAI through LiteLLM."""
    if not LITELLM_AVAILABLE:
        print("LiteLLM not available")
        return
    
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "your-key-here")
    
    try:
        response = completion(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello! How are you?"}]
        )
        print("OpenAI Response:")
        print(response.choices[0].message.content)
    except Exception as e:
        print(f"Error: {e}")


def example_anthropic():
    """Example: Using Anthropic Claude through LiteLLM."""
    if not LITELLM_AVAILABLE:
        print("LiteLLM not available")
        return
    
    os.environ["ANTHROPIC_API_KEY"] = os.getenv("ANTHROPIC_API_KEY", "your-key-here")
    
    try:
        response = completion(
            model="claude-3-sonnet-20240229",
            messages=[{"role": "user", "content": "Explain quantum computing in simple terms."}]
        )
        print("Anthropic Response:")
        print(response.choices[0].message.content)
    except Exception as e:
        print(f"Error: {e}")


def example_ollama():
    """Example: Using Ollama (local) through LiteLLM."""
    if not LITELLM_AVAILABLE:
        print("LiteLLM not available")
        return
    
    try:
        response = completion(
            model="ollama/llama3.1:8b",
            messages=[{"role": "user", "content": "What is machine learning?"}]
        )
        print("Ollama Response:")
        print(response.choices[0].message.content)
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure Ollama is running: ollama serve")


async def example_async():
    """Example: Async completion."""
    if not LITELLM_AVAILABLE:
        print("LiteLLM not available")
        return
    
    import asyncio
    
    try:
        response = await acompletion(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello from async!"}]
        )
        print("Async Response:")
        print(response.choices[0].message.content)
    except Exception as e:
        print(f"Error: {e}")


def example_streaming():
    """Example: Streaming responses."""
    if not LITELLM_AVAILABLE:
        print("LiteLLM not available")
        return
    
    try:
        response = completion(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Count from 1 to 10"}],
            stream=True
        )
        
        print("Streaming Response:")
        for chunk in response:
            if chunk.choices[0].delta.content:
                print(chunk.choices[0].delta.content, end="", flush=True)
        print()  # New line
    except Exception as e:
        print(f"Error: {e}")


def example_multiple_providers():
    """Example: Using multiple providers with fallback."""
    if not LITELLM_AVAILABLE:
        print("LiteLLM not available")
        return
    
    # Try multiple providers in order
    providers = [
        ("gpt-3.5-turbo", "OPENAI_API_KEY"),
        ("claude-3-sonnet-20240229", "ANTHROPIC_API_KEY"),
        ("ollama/llama3.1:8b", None)  # Ollama doesn't need API key
    ]
    
    message = "What is the capital of France?"
    
    for model, env_key in providers:
        if env_key and not os.getenv(env_key):
            continue
        
        try:
            print(f"\nTrying {model}...")
            response = completion(
                model=model,
                messages=[{"role": "user", "content": message}]
            )
            print(f"Success with {model}:")
            print(response.choices[0].message.content)
            break
        except Exception as e:
            print(f"Failed with {model}: {e}")
            continue


def example_custom_prompt():
    """Example: Using custom prompts and parameters."""
    if not LITELLM_AVAILABLE:
        print("LiteLLM not available")
        return
    
    try:
        response = completion(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that explains things clearly."},
                {"role": "user", "content": "Explain recursion"}
            ],
            temperature=0.3,  # Lower temperature for more focused responses
            max_tokens=200
        )
        print("Custom Prompt Response:")
        print(response.choices[0].message.content)
    except Exception as e:
        print(f"Error: {e}")


def main():
    """Run examples."""
    print("=" * 60)
    print("LiteLLM Usage Examples")
    print("=" * 60)
    
    if not LITELLM_AVAILABLE:
        print("\n⚠️  LiteLLM is not installed!")
        print("Install with: pip install litellm")
        print("\nSome examples require API keys:")
        print("  - OPENAI_API_KEY for OpenAI")
        print("  - ANTHROPIC_API_KEY for Anthropic")
        print("  - Ollama running locally for Ollama examples")
        return
    
    examples = [
        ("OpenAI", example_openai),
        ("Anthropic", example_anthropic),
        ("Ollama", example_ollama),
        ("Streaming", example_streaming),
        ("Custom Prompt", example_custom_prompt),
        ("Multiple Providers", example_multiple_providers),
    ]
    
    for name, func in examples:
        print(f"\n{'=' * 60}")
        print(f"Example: {name}")
        print('=' * 60)
        try:
            if name == "Async":
                import asyncio
                asyncio.run(func())
            else:
                func()
        except Exception as e:
            print(f"Error in {name} example: {e}")


if __name__ == "__main__":
    main()

