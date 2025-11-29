"""
Dev Code Crew Orchestration.
Manages software development and coding tasks.
"""

from crewai import Crew, Process, Agent, Task  # type: ignore
from typing import Dict, Any, Optional, List
from ..config import config


class DevCodeCrew:
    """Main crew class for development workflows."""

    def __init__(self, process: str = "sequential"):
        self.process = Process.sequential if process == "sequential" else Process.hierarchical
        self.agents = self._create_agents()
        self.tasks = self._create_tasks()
        self.crew = self._create_crew()

    def _create_agents(self) -> Dict[str, Any]:
        return {
            "senior_developer": Agent(
                role='Senior Developer',
                goal='Write clean, efficient, and well-documented code',
                backstory="You are a senior software engineer with expertise in Python and system architecture.",
                verbose=config.VERBOSE,
                allow_delegation=False
            )
        }

    def _create_tasks(self) -> List[Any]:
        agent = self.agents["senior_developer"]
        return [
            Task(
                description="Develop code solution for: {topic}",
                expected_output="Production-ready code with documentation.",
                agent=agent,
                output_file=config.get_output_path("code_solution.md")
            )
        ]

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
        return {"agents_available": 1}

