"""
ML Crew Orchestration for CrewAI.
Manages machine learning analysis and random forest evaluation.
"""

from crewai import Crew, Process, Agent, Task  # type: ignore
from typing import Dict, Any, Optional, List
from ..config import config


class MLCrew:
    """Main crew class for ML analysis workflows."""

    def __init__(self, process: str = "sequential"):
        self.process = Process.sequential if process == "sequential" else Process.hierarchical
        self.agents = self._create_agents()
        self.tasks = self._create_tasks()
        self.crew = self._create_crew()

    def _create_agents(self) -> Dict[str, Any]:
        """Create ML agents."""
        return {
            "ml_engineer": Agent(
                role='ML Engineer',
                goal='Analyze datasets and build random forest models',
                backstory="You are an expert ML engineer specializing in Random Forest algorithms.",
                verbose=config.VERBOSE,
                allow_delegation=False
            )
        }

    def _create_tasks(self) -> List[Any]:
        """Create ML tasks."""
        agent = self.agents["ml_engineer"]
        return [
            Task(
                description="Analyze the dataset and train a Random Forest model. Topic: {topic}",
                expected_output="Model performance report and analysis.",
                agent=agent,
                output_file=config.get_output_path("ml_analysis_report.md")
            )
        ]

    def _create_crew(self) -> Crew:
        """Create the main crew."""
        return Crew(
            agents=list(self.agents.values()),
            tasks=self.tasks,
            verbose=config.VERBOSE,
            process=self.process,
        )

    def kickoff(self, inputs: Optional[Dict[str, Any]] = None) -> Any:
        """Execute the workflow."""
        crew_inputs = inputs or {"topic": "Random Forest Classification"}
        return self.crew.kickoff(inputs=crew_inputs)

    @staticmethod
    def get_status() -> Dict[str, Any]:
        return {"agents_available": 1}

