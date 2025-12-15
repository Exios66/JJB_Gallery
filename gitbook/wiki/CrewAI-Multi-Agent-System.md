# CrewAI Multi-Agent System

A comprehensive multi-agent framework using CrewAI, featuring multiple specialized agent swarms for different domains including machine learning, research, development, business intelligence, and documentation.

## Overview

This project implements a versatile multi-agent system where different specialized agent swarms collaborate on complex workflows. Each swarm contains domain-specific agents designed for particular tasks and industries.

## Features

- ✅ **Multiple Agent Swarms**: Specialized swarms for different domains
- ✅ **Web Interface**: Streamlit-based chat interface
- ✅ **CLI Interface**: Terminal-based interaction
- ✅ **Multiple LLM Providers**: Support for Ollama, OpenAI, Anthropic, Google, Azure
- ✅ **Offline Mode**: Support for offline LLM usage
- ✅ **Comprehensive Tools**: Domain-specific tools for each swarm

## Installation

```bash
cd projects/Crewai
pip install -r requirements.txt
```

**Key Dependencies:**
- crewai
- crewai-tools
- streamlit
- pydantic

## Quick Start

### Setup Environment

```bash
python main.py --setup
```

This will:
- Check for available LLM providers
- Validate configuration
- Show setup instructions if needed

### Run ML Analysis Swarm

```bash
python main.py --run ml
```

### Run Research Swarm

```bash
python main.py --run research
```

### Web Interface

```bash
streamlit run interface_web.py
```

### CLI Interface

```bash
python interface_cli.py
```

## Available Agent Swarms

### 1. ML Analysis Swarm

**Specialization**: Random Forest and machine learning evaluation

**Agents:**
- **Data Analyst**: Dataset exploration and preprocessing recommendations
- **Model Evaluator**: Performance assessment and comparison analysis
- **Feature Engineer**: Feature importance analysis and engineering suggestions
- **Hyperparameter Optimizer**: Parameter tuning and optimization strategies
- **Report Writer**: Comprehensive report generation for stakeholders

### 2. Research Swarm

**Specialization**: ML research, trends, and innovation

**Agents:**
- **Literature Reviewer**: Academic paper analysis and scholarly research
- **Trend Analyzer**: Industry trends and market developments
- **Innovation Scout**: Novel applications and breakthrough technologies
- **Research Summarizer**: Synthesis of research findings

### 3. Academic Research Swarm

**Specialization**: Scholarly research and academic analysis

**Agents:**
- **Literature Reviewer**: Comprehensive academic literature review
- **Research Designer**: Experimental design and methodology
- **Academic Data Analyst**: Statistical analysis for research
- **Thesis Writer**: Academic writing and documentation
- **Citation Manager**: Reference management and formatting

### 4. Business Intelligence Swarm

**Specialization**: Market and business analysis

**Agents:**
- **Market Analyst**: Market research and competitive analysis
- **Financial Analyst**: Financial data analysis and forecasting
- **Strategy Consultant**: Strategic planning and recommendations
- **Report Generator**: Business report creation

### 5. Development & Code Swarm

**Specialization**: Software development workflows

**Agents:**
- **Code Reviewer**: Code quality and best practices
- **Architect**: System design and architecture
- **Developer**: Code implementation and debugging
- **Tester**: Test creation and quality assurance

### 6. Documentation Swarm

**Specialization**: Technical writing and documentation

**Agents:**
- **Technical Writer**: Documentation creation
- **API Documenter**: API documentation generation
- **Tutorial Creator**: Step-by-step guides
- **Documentation Reviewer**: Quality assurance for docs

## LLM Configuration

### Ollama (Recommended - Free, Local)

```bash
# Install Ollama from https://ollama.ai
ollama pull llama3.1:8b

# Set environment variable (optional)
export OLLAMA_BASE_URL=http://localhost:11434
export OLLAMA_MODEL=llama3.1:8b
```

### OpenAI

```bash
export OPENAI_API_KEY=sk-...
export OPENAI_MODEL_NAME=gpt-4o-mini
```

### Anthropic

```bash
export ANTHROPIC_API_KEY=sk-ant-...
export ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
```

### Google

```bash
export GOOGLE_API_KEY=...
export GOOGLE_MODEL=gemini-pro
```

## Usage Examples

### Command Line

```bash
# List all available swarms
python main.py --list-crews

# Run specific swarm
python main.py --run ml
python main.py --run research
python main.py --run business_intelligence

# Check status
python main.py --status
```

### Programmatic Usage

```python
from crews import MLCrew, ResearchCrew
from config import config

# Initialize ML crew
ml_crew = MLCrew(process=config.PROCESS_TYPE)

# Execute workflow
result = ml_crew.kickoff()
print(result)
```

### Web Interface

```bash
streamlit run interface_web.py
```

Features:
- Select swarm type
- Enter task description
- View agent progress
- Download results

## Configuration

### Environment Variables

```bash
# LLM Provider (auto-detected if not set)
LLM_PROVIDER=ollama  # or openai, anthropic, google, azure

# Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b

# OpenAI
OPENAI_API_KEY=sk-...
OPENAI_MODEL_NAME=gpt-4o-mini

# Anthropic
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022

# Google
GOOGLE_API_KEY=...
GOOGLE_MODEL=gemini-pro

# System
VERBOSE=true
PROCESS_TYPE=sequential  # or hierarchical
```

## Project Structure

```
Crewai/
├── agents/              # Agent definitions
├── crews/              # Crew/swarm definitions
├── tasks/              # Task definitions
├── tools/              # Tool definitions
├── config.py           # Configuration
├── llm_config.py       # LLM configuration
├── main.py             # CLI entry point
├── interface_web.py     # Streamlit interface
├── interface_cli.py     # CLI interface
└── router.py           # API router
```

## Advanced Usage

### Custom Agents

Create custom agents in `agents/`:

```python
from crewai import Agent

custom_agent = Agent(
    role="Custom Role",
    goal="Custom Goal",
    backstory="Custom backstory",
    verbose=True
)
```

### Custom Tools

Create custom tools in `tools/`:

```python
from crewai_tools import tool

@tool
def custom_tool(input: str) -> str:
    """Custom tool description."""
    return f"Processed: {input}"
```

### Custom Crews

Create custom crews in `crews/`:

```python
from crewai import Crew
from agents import custom_agent
from tasks import custom_task

custom_crew = Crew(
    agents=[custom_agent],
    tasks=[custom_task],
    verbose=True
)
```

## Troubleshooting

### LLM Provider Not Detected

```bash
# Check provider status
python main.py --status

# Get setup instructions
python main.py --setup-llm
```

### Import Errors

```bash
pip install -r requirements.txt
```

### Ollama Connection Issues

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama
ollama serve
```

## Resources

- [CrewAI Documentation](https://docs.crewai.com/)
- [CrewAI GitHub](https://github.com/joaomdmoura/crewAI)
- [LLM Setup Guide](LLM-Setup.md)

## Related Documentation

- [Installation Guide](Installation-Guide.md)
- [Configuration Guide](Configuration-Guide.md)
- [Quick Start](Quick-Start.md)

