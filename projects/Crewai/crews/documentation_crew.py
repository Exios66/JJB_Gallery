"""
Documentation Crew Orchestration.
Manages technical writing and documentation tasks.
"""

from crewai import Crew, Process, Agent, Task  # type: ignore
from typing import Dict, Any, Optional, List
from ..config import config


class DocumentationCrew:
    """Main crew class for documentation workflows."""

    def __init__(self, process: str = "sequential"):
        self.process = Process.sequential if process == "sequential" else Process.hierarchical
        self.agents = self._create_agents()
        self.tasks = self._create_tasks()
        self.crew = self._create_crew()

    def _create_agents(self) -> Dict[str, Any]:
        return {
            "technical_writer": Agent(
                role='Technical Writer',
                goal='Create clear and comprehensive technical documentation',
                backstory="You are an experienced technical writer who excels at explaining complex technical concepts.",
                verbose=config.VERBOSE,
                allow_delegation=False
            )
        }

    def _create_tasks(self) -> List[Any]:
        agent = self.agents["technical_writer"]
        return [
            Task(
                description="Create technical documentation for: {topic}",
                expected_output="Comprehensive technical documentation.",
                agent=agent,
                output_file=config.get_output_path("documentation.md")
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
        crew_inputs = inputs or {"topic": "System Architecture"}
        return self.crew.kickoff(inputs=crew_inputs)

    @staticmethod
    def get_status() -> Dict[str, Any]:
        return {"agents_available": 1}

