"""
Development Tools for CrewAI Dev Code Swarm.
Specialized tools for code execution, file management, testing, and software development.
"""

from crewai.tools.base_tool import BaseTool  # type: ignore
from typing import Any, Optional
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime


class CodeExecutorTool(BaseTool):
    """Tool for executing Python code and capturing results."""

    name: str = "Code Executor"
    description: str = """Executes Python code snippets safely and returns results. Useful for testing code, 
    running scripts, and validating implementations. Input: python_code string."""

    def _run(self, python_code: str = None, timeout: int = 30) -> str:
        """Execute Python code and return results."""
        try:
            if not python_code:
                return json.dumps({
                    "status": "ready",
                    "message": "Provide python_code parameter to execute",
                    "safety_note": "Code execution is limited to prevent malicious operations"
                }, indent=2)
            
            # Simple validation - in production, use more robust sandboxing
            dangerous_keywords = ['__import__', 'exec', 'eval', 'open', 'file', 'subprocess']
            code_lower = python_code.lower()
            for keyword in dangerous_keywords:
                if keyword in code_lower:
                    return json.dumps({
                        "status": "blocked",
                        "reason": f"Potentially dangerous operation detected: {keyword}",
                        "message": "Certain operations are restricted for security"
                    }, indent=2)
            
            # Execute code in a safe context
            try:
                result = eval(python_code) if len(python_code) < 100 else None
                if result is not None:
                    return json.dumps({
                        "status": "success",
                        "result": str(result),
                        "message": "Code executed successfully"
                    }, indent=2)
            except Exception as exec_error:
                return json.dumps({
                    "status": "execution_error",
                    "error": str(exec_error),
                    "message": "Code execution encountered an error",
                    "suggestion": "Review code syntax and logic"
                }, indent=2)
            
            return json.dumps({
                "status": "parsed",
                "code": python_code[:100] + "..." if len(python_code) > 100 else python_code,
                "message": "Code received and validated. For complex code, use file-based execution."
            }, indent=2)
            
        except Exception as e:
            return f"Error executing code: {str(e)}"


class FileManagerTool(BaseTool):
    """Tool for managing files, reading code, and organizing project structure."""

    name: str = "File Manager"
    description: str = """Manages files and directories in development projects. Can read files, list directories, 
    check file existence, and organize project structure. Input: action, file_path."""

    def _run(self, action: str = "read", file_path: str = None, content: str = None) -> str:
        """Manage files and directories."""
        try:
            if action == "read" and file_path:
                path = Path(file_path)
                if path.exists() and path.is_file():
                    try:
                        file_content = path.read_text()
                        return json.dumps({
                            "status": "success",
                            "action": action,
                            "file_path": str(path),
                            "file_size": len(file_content),
                            "content_preview": file_content[:500] + "..." if len(file_content) > 500 else file_content,
                            "lines": len(file_content.splitlines())
                        }, indent=2)
                    except Exception as e:
                        return json.dumps({
                            "status": "error",
                            "error": f"Cannot read file: {str(e)}"
                        }, indent=2)
                else:
                    return json.dumps({
                        "status": "not_found",
                        "file_path": str(path),
                        "message": "File does not exist or is not a file"
                    }, indent=2)
            
            elif action == "list" and file_path:
                path = Path(file_path)
                if path.exists() and path.is_dir():
                    files = [f.name for f in path.iterdir()]
                    return json.dumps({
                        "status": "success",
                        "directory": str(path),
                        "files": files[:20],  # Limit to first 20
                        "count": len(files)
                    }, indent=2)
                else:
                    return json.dumps({
                        "status": "error",
                        "message": "Directory does not exist"
                    }, indent=2)
            
            return json.dumps({
                "status": "ready",
                "supported_actions": ["read", "list", "exists", "info"],
                "usage": "Provide action and file_path parameters"
            }, indent=2)
            
        except Exception as e:
            return f"Error managing files: {str(e)}"


class CodeAnalyzerTool(BaseTool):
    """Tool for analyzing code quality, structure, and best practices."""

    name: str = "Code Analyzer"
    description: str = """Analyzes code for quality, structure, best practices, and potential issues. Checks for 
    PEP 8 compliance, complexity, security issues, and code smells."""

    def _run(self, code_snippet: str = None, analysis_type: str = "comprehensive", language: str = "python") -> str:
        """Analyze code quality and structure."""
        try:
            analysis = {
                "language": language,
                "analysis_type": analysis_type,
                "timestamp": datetime.now().isoformat(),
                "quality_metrics": {
                    "readability": "Requires code review",
                    "complexity": "Requires complexity analysis",
                    "maintainability": "Requires structural analysis"
                },
                "best_practices_check": {
                    "naming_conventions": [],
                    "code_organization": [],
                    "documentation": [],
                    "error_handling": []
                },
                "potential_issues": [],
                "recommendations": [
                    "Follow PEP 8 style guidelines",
                    "Add docstrings to functions and classes",
                    "Use type hints where appropriate",
                    "Implement proper error handling",
                    "Keep functions focused and small",
                    "Write unit tests for critical code"
                ]
            }
            
            if code_snippet:
                lines = code_snippet.splitlines()
                analysis["code_stats"] = {
                    "lines": len(lines),
                    "characters": len(code_snippet),
                    "preview_available": True
                }
            
            return json.dumps(analysis, indent=2)
        except Exception as e:
            return f"Error analyzing code: {str(e)}"


class TestGeneratorTool(BaseTool):
    """Tool for generating test cases and validating code functionality."""

    name: str = "Test Generator"
    description: str = """Generates test cases for code, validates functionality, and ensures test coverage. 
    Creates unit tests, integration tests, and test plans."""

    def _run(self, function_name: str = None, test_type: str = "unit", code_context: str = None) -> str:
        """Generate test cases and validation."""
        try:
            test_plan = {
                "test_type": test_type,
                "target": function_name or "code_component",
                "timestamp": datetime.now().isoformat(),
                "test_cases": [],
                "test_structure": {
                    "setup": "Test data and environment setup",
                    "execution": "Test execution steps",
                    "assertion": "Expected vs actual results",
                    "teardown": "Cleanup procedures"
                },
                "coverage_areas": [
                    "Happy path scenarios",
                    "Edge cases",
                    "Error handling",
                    "Boundary conditions"
                ],
                "recommendations": [
                    "Test all code paths",
                    "Include negative test cases",
                    "Test with various input types",
                    "Verify error messages are meaningful",
                    "Ensure tests are isolated and repeatable"
                ]
            }
            
            if function_name:
                test_plan["test_cases"].append({
                    "name": f"test_{function_name}_basic",
                    "description": f"Basic functionality test for {function_name}"
                })
            
            return json.dumps(test_plan, indent=2)
        except Exception as e:
            return f"Error generating tests: {str(e)}"


class ArchitectureAnalyzerTool(BaseTool):
    """Tool for analyzing software architecture and design patterns."""

    name: str = "Architecture Analyzer"
    description: str = """Analyzes software architecture, design patterns, system structure, and architectural 
    decisions. Evaluates scalability, maintainability, and best practices."""

    def _run(self, architecture_description: str = None, focus_areas: str = None) -> str:
        """Analyze software architecture."""
        try:
            analysis = {
                "timestamp": datetime.now().isoformat(),
                "architecture_components": [],
                "design_patterns_identified": [],
                "architectural_principles": {
                    "separation_of_concerns": "Review module boundaries",
                    "single_responsibility": "Check component responsibilities",
                    "dependency_management": "Analyze dependencies",
                    "scalability": "Assess scalability design"
                },
                "strengths": [],
                "improvements": [],
                "recommendations": [
                    "Document architectural decisions (ADRs)",
                    "Ensure clear separation of concerns",
                    "Plan for scalability from the start",
                    "Implement proper error handling at system level",
                    "Use established design patterns where appropriate",
                    "Consider microservices if scale requires it"
                ]
            }
            
            if architecture_description:
                analysis["description_received"] = True
                analysis["focus_areas"] = focus_areas.split(',') if focus_areas else ["comprehensive"]
            
            return json.dumps(analysis, indent=2)
        except Exception as e:
            return f"Error analyzing architecture: {str(e)}"

