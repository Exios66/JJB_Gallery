"""
Content Research Crew Orchestration.
Manages content strategy and research.
"""

from crewai import Crew, Process, Agent, Task  # type: ignore
from typing import Dict, Any, Optional, List
from ..config import config


class ResearchContentCrew:
    """Main crew class for content research workflows."""

    def __init__(self, process: str = "sequential"):
        self.process = Process.sequential if process == "sequential" else Process.hierarchical
        self.agents = self._create_agents()
        self.tasks = self._create_tasks()
        self.crew = self._create_crew()

    def _create_agents(self) -> Dict[str, Any]:
        return {
            "content_strategist": Agent(
                role='Content Strategist',
                goal='Develop content strategies and research topics',
                backstory="You are an expert content strategist focused on engaging and accurate technical content.",
                verbose=config.VERBOSE,
                allow_delegation=False
            )
        }

    def _create_tasks(self) -> List[Any]:
        agent = self.agents["content_strategist"]
        return [
            Task(
                description="Research and outline content strategy for: {topic}",
                expected_output="Content strategy document and outline.",
                agent=agent,
                output_file=config.get_output_path("content_strategy.md")
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
        crew_inputs = inputs or {"topic": "AI Content Trends"}
        return self.crew.kickoff(inputs=crew_inputs)

    @staticmethod
    def get_status() -> Dict[str, Any]:
        return {"agents_available": 1}

