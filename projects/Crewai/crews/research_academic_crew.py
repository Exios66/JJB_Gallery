"""
Academic Research Crew Orchestration.
Manages scholarly research and literature reviews.
"""

from crewai import Crew, Process, Agent, Task  # type: ignore
from typing import Dict, Any, Optional, List
from ..config import config


class ResearchAcademicCrew:
    """Main crew class for academic research workflows."""

    def __init__(self, process: str = "sequential"):
        self.process = Process.sequential if process == "sequential" else Process.hierarchical
        self.agents = self._create_agents()
        self.tasks = self._create_tasks()
        self.crew = self._create_crew()

    def _create_agents(self) -> Dict[str, Any]:
        return {
            "academic_researcher": Agent(
                role='Academic Researcher',
                goal='Analyze academic papers and literature',
                backstory="You are a distinguished academic researcher specializing in literature review.",
                verbose=config.VERBOSE,
                allow_delegation=False
            )
        }

    def _create_tasks(self) -> List[Any]:
        agent = self.agents["academic_researcher"]
        return [
            Task(
                description="Conduct an academic literature review on: {topic}",
                expected_output="Academic literature review report with citations.",
                agent=agent,
                output_file=config.get_output_path("academic_review.md")
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
        crew_inputs = inputs or {"topic": "Machine Learning Theory"}
        return self.crew.kickoff(inputs=crew_inputs)

    @staticmethod
    def get_status() -> Dict[str, Any]:
        return {"agents_available": 1}

