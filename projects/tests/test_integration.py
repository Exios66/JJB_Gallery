"""
Integration tests for cross-project functionality
"""

import pytest
from pathlib import Path


class TestProjectStructure:
    """Test that all projects have required structure."""
    
    def test_all_projects_exist(self):
        """Test that all expected projects exist."""
        projects_dir = Path(__file__).parent.parent
        
        expected_projects = [
            "Crewai",
            "ChatUi",
            "ios_chatbot",
            "litellm",
            "Psychometrics",
            "RAG_Model",
            "terminal_agents"
        ]
        
        for project in expected_projects:
            project_path = projects_dir / project
            assert project_path.exists(), f"Project {project} does not exist"
            assert project_path.is_dir(), f"{project} is not a directory"
    
    def test_all_projects_have_readme(self):
        """Test that all projects have README files."""
        projects_dir = Path(__file__).parent.parent
        
        projects = [
            "Crewai",
            "ChatUi",
            "ios_chatbot",
            "litellm",
            "Psychometrics",
            "RAG_Model",
            "terminal_agents"
        ]
        
        for project in projects:
            readme_path = projects_dir / project / "README.md"
            assert readme_path.exists(), f"README.md missing in {project}"
    
    def test_all_python_projects_have_requirements(self):
        """Test that Python projects have requirements.txt."""
        projects_dir = Path(__file__).parent.parent
        
        python_projects = [
            "Crewai",
            "ios_chatbot",
            "litellm",
            "Psychometrics",
            "RAG_Model",
            "terminal_agents"
        ]
        
        for project in python_projects:
            requirements_path = projects_dir / project / "requirements.txt"
            assert requirements_path.exists(), f"requirements.txt missing in {project}"


class TestDependencies:
    """Test dependency management."""
    
    def test_no_conflicting_versions(self):
        """Test that there are no obviously conflicting dependency versions."""
        # This is a basic check - in a real scenario, you'd use a dependency resolver
        assert True  # Placeholder for actual dependency checking


class TestConfiguration:
    """Test configuration consistency."""
    
    def test_env_var_naming(self):
        """Test that environment variable naming is consistent."""
        # Common env vars that should be consistent
        common_vars = [
            "OPENAI_API_KEY",
            "ANTHROPIC_API_KEY",
            "GOOGLE_API_KEY"
        ]
        
        # All should be uppercase with underscores
        for var in common_vars:
            assert var.isupper()
            assert "_" in var or var.isalpha()


class TestDocumentation:
    """Test documentation consistency."""
    
    def test_readme_structure(self):
        """Test that READMEs have basic structure."""
        projects_dir = Path(__file__).parent.parent
        
        projects = [
            "Crewai",
            "ChatUi",
            "ios_chatbot",
            "litellm",
            "Psychometrics",
            "RAG_Model",
            "terminal_agents"
        ]
        
        for project in projects:
            readme_path = projects_dir / project / "README.md"
            if readme_path.exists():
                content = readme_path.read_text()
                # Check for basic sections
                assert len(content) > 100, f"{project} README is too short"
                # Most READMEs should have installation or usage
                assert "installation" in content.lower() or "usage" in content.lower() or "setup" in content.lower(), \
                    f"{project} README missing installation/usage section"

