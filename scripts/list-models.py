#!/usr/bin/env python3
"""
Script to list and search models from the models registry
"""

import sys
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from models.models_registry import (
        get_model_info,
        list_models_by_provider,
        list_models_by_type,
        search_models,
        get_free_models,
        get_local_models,
        ModelType,
        ALL_MODELS,
        export_to_dict,
    )
except ImportError as e:
    print(f"Error importing models registry: {e}")
    sys.exit(1)


def list_all_models():
    """List all models in the registry"""
    print(f"\n{'='*70}")
    print(f"Models Registry - All Models ({len(ALL_MODELS)} total)")
    print(f"{'='*70}\n")
    
    for model_id, model_info in sorted(ALL_MODELS.items()):
        print(f"{model_info.name:40} [{model_info.provider:12}] {model_info.model_id}")
    print()


def list_by_provider(provider: str):
    """List models by provider"""
    models = list_models_by_provider(provider)
    print(f"\n{'='*70}")
    print(f"{provider.capitalize()} Models ({len(models)} total)")
    print(f"{'='*70}\n")
    
    for model in models:
        print(f"{model.name:40} {model.model_id}")
        if model.specs and model.specs.context_window:
            print(f"  Context: {model.specs.context_window:,} tokens")
        if model.api_endpoint:
            print(f"  Endpoint: {model.api_endpoint.url}")
        print()
    print()


def list_free_models():
    """List free tier models"""
    models = get_free_models()
    print(f"\n{'='*70}")
    print(f"Free Tier Models ({len(models)} total)")
    print(f"{'='*70}\n")
    
    for model in models:
        print(f"{model.name:40} [{model.provider:12}]")
        print(f"  Free Tier: {model.free_tier_limits}")
        print(f"  Model ID: {model.model_id}")
        print()
    print()


def list_local_models():
    """List models that can run locally"""
    models = get_local_models()
    print(f"\n{'='*70}")
    print(f"Local Models ({len(models)} total)")
    print(f"{'='*70}\n")
    
    for model in models:
        print(f"{model.name:40} [{model.provider:12}]")
        print(f"  Model ID: {model.model_id}")
        if model.specs:
            if model.specs.parameters:
                print(f"  Parameters: {model.specs.parameters}B")
            if model.specs.context_window:
                print(f"  Context Window: {model.specs.context_window:,} tokens")
        print()
    print()


def show_model_info(model_id: str):
    """Show detailed information about a model"""
    model_info = get_model_info(model_id)
    
    if not model_info:
        print(f"Model '{model_id}' not found in registry.")
        return
    
    print(f"\n{'='*70}")
    print(f"Model Information: {model_info.name}")
    print(f"{'='*70}\n")
    
    print(f"Model ID:        {model_info.model_id}")
    print(f"Provider:        {model_info.provider}")
    print(f"Type:            {model_info.type.value}")
    print(f"Access Method:   {model_info.access_method.value}")
    print(f"Description:     {model_info.description}")
    
    if model_info.specs:
        print(f"\nSpecifications:")
        if model_info.specs.parameters:
            print(f"  Parameters:     {model_info.specs.parameters}B")
        if model_info.specs.context_window:
            print(f"  Context Window: {model_info.specs.context_window:,} tokens")
        if model_info.specs.architecture:
            print(f"  Architecture:   {model_info.specs.architecture}")
    
    if model_info.api_endpoint:
        print(f"\nAPI Endpoint:")
        print(f"  URL:            {model_info.api_endpoint.url}")
        print(f"  Method:         {model_info.api_endpoint.method}")
        print(f"  Auth Required:  {model_info.api_endpoint.auth_required}")
        print(f"  Rate Limit:     {model_info.api_endpoint.rate_limit}")
    
    if model_info.local_endpoint:
        print(f"\nLocal Endpoint:")
        print(f"  Model Path:     {model_info.local_endpoint}")
    
    print(f"\nAccess:")
    print(f"  API Key Required: {model_info.api_key_required}")
    if model_info.api_key_env_var:
        print(f"  Env Variable:    {model_info.api_key_env_var}")
    if model_info.api_key_url:
        print(f"  Get API Key:     {model_info.api_key_url}")
    
    if model_info.cost_per_1k_tokens:
        print(f"\nCost:")
        print(f"  Per 1K Tokens:   ${model_info.cost_per_1k_tokens}")
    print(f"  Free Tier:       {'Yes' if model_info.free_tier_available else 'No'}")
    if model_info.free_tier_limits:
        print(f"  Free Tier Limit: {model_info.free_tier_limits}")
    
    if model_info.license:
        print(f"\nLicense:")
        print(f"  Type:           {model_info.license.value}")
        if model_info.license_url:
            print(f"  URL:            {model_info.license_url}")
    
    if model_info.recommended_use_cases:
        print(f"\nRecommended Use Cases:")
        for use_case in model_info.recommended_use_cases:
            print(f"  - {use_case}")
    
    if model_info.limitations:
        print(f"\nLimitations:")
        for limitation in model_info.limitations:
            print(f"  - {limitation}")
    
    if model_info.documentation_url:
        print(f"\nDocumentation: {model_info.documentation_url}")
    
    print()


def search_models_cli(query: str):
    """Search models by query"""
    results = search_models(query)
    
    print(f"\n{'='*70}")
    print(f"Search Results for '{query}' ({len(results)} found)")
    print(f"{'='*70}\n")
    
    for model in results:
        print(f"{model.name:40} [{model.provider:12}]")
        print(f"  {model.model_id}")
        print(f"  {model.description[:80]}...")
        print()
    print()


def export_json(output_file: str):
    """Export models registry to JSON"""
    data = export_to_dict()
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Models registry exported to {output_file}")


def main():
    """Main CLI interface"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python list-models.py list                    # List all models")
        print("  python list-models.py provider <provider>      # List by provider (huggingface/openai)")
        print("  python list-models.py free                     # List free tier models")
        print("  python list-models.py local                    # List local models")
        print("  python list-models.py info <model_id>          # Show model info")
        print("  python list-models.py search <query>            # Search models")
        print("  python list-models.py export <output.json>     # Export to JSON")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "list":
        list_all_models()
    elif command == "provider":
        if len(sys.argv) < 3:
            print("Please specify provider: huggingface or openai")
            sys.exit(1)
        list_by_provider(sys.argv[2])
    elif command == "free":
        list_free_models()
    elif command == "local":
        list_local_models()
    elif command == "info":
        if len(sys.argv) < 3:
            print("Please specify model ID")
            sys.exit(1)
        show_model_info(sys.argv[2])
    elif command == "search":
        if len(sys.argv) < 3:
            print("Please specify search query")
            sys.exit(1)
        search_models_cli(sys.argv[2])
    elif command == "export":
        if len(sys.argv) < 3:
            print("Please specify output file")
            sys.exit(1)
        export_json(sys.argv[2])
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()

