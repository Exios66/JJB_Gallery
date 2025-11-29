"""
Dev Code Crew Orchestration.
Manages software architecture, coding, and code review workflows.
"""

from crewai import Crew, Process, Agent, Task  # type: ignore
from typing import Dict, Any, Optional, List
from config import config
from tools.dev_tools import CodeExecutorTool, FileManagerTool, CodeAnalyzerTool, TestGeneratorTool, ArchitectureAnalyzerTool


class DevCodeCrew:
    """Main crew class for development workflows."""

    def __init__(self, process: str = "sequential"):
        self.process = Process.sequential if process == "sequential" else Process.hierarchical
        self.agents = self._create_agents()
        self.tasks = self._create_tasks()
        self.crew = self._create_crew()

    def _create_agents(self) -> Dict[str, Any]:
        # Development tools
        architecture_analyzer = ArchitectureAnalyzerTool()
        code_executor = CodeExecutorTool()
        file_manager = FileManagerTool()
        code_analyzer = CodeAnalyzerTool()
        test_generator = TestGeneratorTool()

        return {
            "software_architect": Agent(
                role='Software Architect',
                goal='Design scalable and robust system architectures',
                backstory="""You are a veteran architect who thinks in systems. You design software structures that are
                maintainable, scalable, and secure. You make high-level decisions about patterns, databases, and APIs.""",
                verbose=config.VERBOSE,
                tools=[architecture_analyzer, file_manager],
                allow_delegation=False
            ),
            "senior_developer": Agent(
                role='Senior Python Developer',
                goal='Implement clean, efficient, and well-documented code',
                backstory="""You are a coding machine. You write Pythonic code that is easy to read and hard to break.
                You follow PEP8 standards and believe in the power of type hinting and unit tests.""",
                verbose=config.VERBOSE,
                tools=[code_executor, file_manager, code_analyzer],
                allow_delegation=False
            ),
            "code_reviewer": Agent(
                role='Code QA Engineer',
                goal='Review code for bugs, security issues, and best practices',
                backstory="""You are the gatekeeper. Nothing goes into production without your seal of approval. You spot
                edge cases, race conditions, and security vulnerabilities that others miss.""",
                verbose=config.VERBOSE,
                tools=[code_analyzer, test_generator, code_executor],
                allow_delegation=False
            )
        }

    def _create_tasks(self) -> List[Any]:
        software_architect = self.agents["software_architect"]
        senior_developer = self.agents["senior_developer"]
        code_reviewer = self.agents["code_reviewer"]

        task_architecture = Task(
            description="""Design the software architecture for: {topic}
            1. Use the Architecture Analyzer Tool to evaluate design options.
            2. Define the system components and their interactions.
            3. Select appropriate design patterns (e.g., MVC, Singleton).
            4. Outline data models and API endpoints.
            5. Identify potential bottlenecks.""",
            expected_output="Technical design document and architecture diagram description.",
            agent=software_architect,
            output_file=config.get_output_path("architecture_design.md")
        )

        task_implementation = Task(
            description="""Implement the solution based on the architecture for: {topic}
            1. Use the Code Executor Tool to verify code snippets.
            2. Write the core logic in Python.
            3. Include docstrings and type hints.
            4. Ensure error handling is robust.
            5. Provide example usage snippets.""",
            expected_output="Python source code files and implementation notes.",
            agent=senior_developer,
            context=[task_architecture],
            output_file=config.get_output_path("implementation_code.md")
        )

        task_review = Task(
            description="""Review the implementation code for: {topic}
            1. Use the Code Analyzer Tool and Test Generator Tool.
            2. Check for adherence to the design spec.
            3. Identify logic errors or inefficiencies.
            4. Suggest refactoring for readability.
            5. Verify security best practices.""",
            expected_output="Code review report with change requests and approval status.",
            agent=code_reviewer,
            context=[task_architecture, task_implementation],
            output_file=config.get_output_path("code_review.md")
        )

        return [task_architecture, task_implementation, task_review]

    def _create_crew(self) -> Crew:
        return Crew(
            agents=list(self.agents.values()),
            tasks=self.tasks,
            verbose=config.VERBOSE,
            process=self.process,
        )

    def kickoff(self, inputs: Optional[Dict[str, Any]] = None) -> Any:
        crew_inputs = inputs or {"topic": "Python API Development"}
        return self.crew.kickoff(inputs=crew_inputs)

    @staticmethod
    def get_status() -> Dict[str, Any]:
        return {"agents_available": 3}
    
    @staticmethod
    def validate_environment() -> Dict[str, bool]:
        """Validate environment configuration (delegates to config)."""
        from config import config
        return config.validate_environment()
