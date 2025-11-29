# Testing Instructions for CrewAI Swarms

This guide explains how to verify the installation and test specific swarms using the provided test runner.

## 🚀 Quick Start

Run the verification suite to check everything:

```bash
python run_tests.py --all --tools
```

## 🛠️ Test Options

### 1. Verify All Tools
To check that all 31 specialized tools are functioning correctly (including Code Executor, File Manager, and ML Analyzers):

```bash
python run_tests.py --tools
```

### 2. Test a Specific Swarm
To verify the configuration of a specific crew (checks agents, tools, and task loading):

**ML Crew:**
```bash
python run_tests.py --crew ml
```

**Research Crew:**
```bash
python run_tests.py --crew research
```

**Business Intelligence Crew:**
```bash
python run_tests.py --crew business_intelligence
```

**Other Available Swarms:**
- `research_academic`
- `research_content`
- `dev_code`
- `documentation`

### 3. Full System Check
To run all checks at once:

```bash
python run_tests.py --all
```

## 🧪 What is Tested?

1.  **Import Verification**: Ensures all tool modules and dependencies are correctly installed.
2.  **Functional Testing**:
    *   **CodeExecutorTool**: Verifies it can run Python code and capture output.
    *   **DatasetAnalyzerTool**: Verifies it can read and analyze CSV files (using mock data).
3.  **Crew Instantiation**:
    *   Creates an instance of the requested crew.
    *   Verifies agents are created.
    *   Checks that tools are correctly assigned to agents.
    *   *Note: This step requires valid LLM API keys (OpenAI, Anthropic, or Ollama).*

## ⚠️ Troubleshooting

**"Error importing native provider: OPENAI_API_KEY is required"**
- This means you haven't set up your LLM provider yet.
- Run `python main.py --setup-llm` to see setup instructions.
- If using Ollama (local), make sure it is running (`ollama serve`) and configured.

**"ModuleNotFoundError"**
- Ensure you are running the command from the `projects/Crewai` directory.
- Check that you are using the correct Python environment.

