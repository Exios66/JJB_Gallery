"""
Research Crew Orchestration.
Manages general research tasks.
"""

from crewai import Crew, Process, Agent, Task  # type: ignore
from typing import Dict, Any, Optional, List
from ..config import config


class ResearchCrew:
    """Main crew class for research workflows."""

    def __init__(self, process: str = "sequential"):
        self.process = Process.sequential if process == "sequential" else Process.hierarchical
        self.agents = self._create_agents()
        self.tasks = self._create_tasks()
        self.crew = self._create_crew()

    def _create_agents(self) -> Dict[str, Any]:
        return {
            "researcher": Agent(
                role='Senior Researcher',
                goal='Conduct deep research on given topics',
                backstory="You are a senior researcher with expertise in finding and synthesizing information.",
                verbose=config.VERBOSE,
                allow_delegation=False
            )
        }

    def _create_tasks(self) -> List[Any]:
        agent = self.agents["researcher"]
        return [
            Task(
                description="Conduct comprehensive research on the following topic: {topic}",
                expected_output="Detailed research report with key findings.",
                agent=agent,
                output_file=config.get_output_path("research_report.md")
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
        crew_inputs = inputs or {"topic": "General ML Trends"}
        return self.crew.kickoff(inputs=crew_inputs)

    @staticmethod
    def get_status() -> Dict[str, Any]:
        return {"agents_available": 1}

