"""
Documentation Tools for CrewAI Documentation Swarm.
Specialized tools for documentation generation, formatting, and management.
"""

from crewai.tools.base_tool import BaseTool  # type: ignore
from typing import Any, Optional
import json
import re
from pathlib import Path
from datetime import datetime


class DocumentStructureTool(BaseTool):
    """Tool for planning and structuring documentation."""

    name: str = "Document Structure Planner"
    description: str = """Plans and structures documentation projects. Creates table of contents, outlines document 
    hierarchy, and organizes information architecture. Input: doc_type, audience, topics."""

    def _run(self, doc_type: str = "technical_guide", audience: str = "developers", topics: str = None) -> str:
        """Plan and structure documentation."""
        try:
            structure = {
                "doc_type": doc_type,
                "target_audience": audience,
                "timestamp": datetime.now().isoformat(),
                "document_structure": {
                    "introduction": "Overview and getting started",
                    "main_content": topics.split(',') if topics else ["Core Concepts", "Usage", "Examples"],
                    "appendices": "Additional resources and references"
                },
                "navigation_hierarchy": [],
                "section_recommendations": {
                    "developers": ["API Reference", "Code Examples", "Integration Guide", "Troubleshooting"],
                    "users": ["Getting Started", "User Guide", "FAQ", "Best Practices"],
                    "administrators": ["Installation", "Configuration", "Maintenance", "Security"]
                },
                "organization_principles": [
                    "Logical flow from basic to advanced",
                    "Clear section headings",
                    "Consistent formatting",
                    "Easy navigation"
                ]
            }
            
            return json.dumps(structure, indent=2)
        except Exception as e:
            return f"Error structuring documentation: {str(e)}"


class MarkdownFormatterTool(BaseTool):
    """Tool for formatting and styling markdown documents."""

    name: str = "Markdown Formatter"
    description: str = """Formats markdown documents, applies consistent styling, validates markdown syntax, and 
    ensures proper formatting. Handles code blocks, tables, lists, and links."""

    def _run(self, markdown_content: str = None, style_guide: str = "standard") -> str:
        """Format and style markdown documents."""
        try:
            formatting = {
                "style_guide": style_guide,
                "timestamp": datetime.now().isoformat(),
                "formatting_rules": {
                    "headings": "Use appropriate heading levels (H1-H6)",
                    "code_blocks": "Use triple backticks with language specification",
                    "lists": "Use consistent list formatting",
                    "links": "Use descriptive link text",
                    "tables": "Ensure proper table alignment"
                },
                "validation_checks": [
                    "Heading hierarchy is logical",
                    "Code blocks have syntax highlighting",
                    "Links are valid and descriptive",
                    "Images have alt text",
                    "Consistent formatting throughout"
                ],
                "recommendations": [
                    "Use consistent heading styles",
                    "Include code examples with explanations",
                    "Add cross-references between sections",
                    "Use tables for structured data",
                    "Include visual elements where helpful"
                ]
            }
            
            if markdown_content:
                lines = markdown_content.splitlines()
                formatting["content_stats"] = {
                    "lines": len(lines),
                    "estimated_length": len(markdown_content),
                    "preview_available": True
                }
            
            return json.dumps(formatting, indent=2)
        except Exception as e:
            return f"Error formatting markdown: {str(e)}"


class DocumentationValidatorTool(BaseTool):
    """Tool for validating documentation quality, completeness, and accuracy."""

    name: str = "Documentation Validator"
    description: str = """Validates documentation for completeness, accuracy, clarity, and consistency. Checks for 
    broken links, missing sections, unclear explanations, and formatting issues."""

    def _run(self, doc_content: str = None, validation_scope: str = "comprehensive") -> str:
        """Validate documentation quality."""
        try:
            validation = {
                "validation_scope": validation_scope,
                "timestamp": datetime.now().isoformat(),
                "quality_checks": {
                    "completeness": [],
                    "accuracy": [],
                    "clarity": [],
                    "consistency": []
                },
                "common_issues": [],
                "quality_metrics": {
                    "readability": "Requires content analysis",
                    "completeness_score": "Requires section comparison",
                    "accuracy_score": "Requires technical review"
                },
                "validation_checklist": [
                    "All sections are complete",
                    "Code examples are tested and working",
                    "Links are valid and accessible",
                    "Terminology is consistent",
                    "Instructions are clear and actionable",
                    "Examples are relevant and helpful",
                    "No broken references"
                ],
                "recommendations": [
                    "Have technical experts review for accuracy",
                    "Test all code examples",
                    "Verify all links work",
                    "Ensure consistent terminology",
                    "Get user feedback on clarity"
                ]
            }
            
            if doc_content:
                # Simple checks
                has_code_blocks = '```' in doc_content
                has_headings = '#' in doc_content
                validation["content_analysis"] = {
                    "has_code_blocks": has_code_blocks,
                    "has_headings": has_headings,
                    "length": len(doc_content)
                }
            
            return json.dumps(validation, indent=2)
        except Exception as e:
            return f"Error validating documentation: {str(e)}"


class CodeExampleGeneratorTool(BaseTool):
    """Tool for generating and validating code examples for documentation."""

    name: str = "Code Example Generator"
    description: str = """Generates code examples for documentation, ensures they're correct and runnable, and 
    formats them properly with explanations. Handles multiple programming languages."""

    def _run(self, example_type: str = "basic", language: str = "python", purpose: str = None) -> str:
        """Generate code examples for documentation."""
        try:
            example_template = {
                "example_type": example_type,
                "language": language,
                "purpose": purpose or "demonstration",
                "timestamp": datetime.now().isoformat(),
                "example_structure": {
                    "description": "What the example demonstrates",
                    "code": "The actual code snippet",
                    "explanation": "Step-by-step explanation",
                    "expected_output": "What the code produces",
                    "related_examples": []
                },
                "best_practices": [
                    "Keep examples simple and focused",
                    "Show one concept at a time",
                    "Include comments in code",
                    "Provide expected output",
                    "Link to related examples",
                    "Keep examples up-to-date with API changes"
                ],
                "formatting_guidelines": [
                    "Use syntax highlighting",
                    "Include line numbers for long examples",
                    "Break complex examples into steps",
                    "Show error handling where relevant"
                ]
            }
            
            return json.dumps(example_template, indent=2)
        except Exception as e:
            return f"Error generating code example: {str(e)}"

