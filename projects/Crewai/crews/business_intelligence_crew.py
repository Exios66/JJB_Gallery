"""
Business Intelligence Crew Orchestration for CrewAI.
Manages business analysis, market research, and strategic insights workflows.
"""

from crewai import Crew, Process  # type: ignore
from typing import Dict, Any, Optional, List
from config import config


class BusinessIntelligenceCrew:
    """Main crew class for business intelligence workflows."""

    def __init__(self, process: str = "sequential"):
        """Initialize the business intelligence crew with agents and tasks.

        Args:
            process: Process type ("sequential" or "hierarchical")
        """
        self.process = Process.sequential if process == "sequential" else Process.hierarchical
        self.agents = self._create_agents()
        self.tasks = self._create_tasks()
        self.crew = self._create_crew()

    def _create_agents(self) -> Dict[str, Any]:
        """Create all specialized business intelligence agents."""
        # Import here to avoid circular imports
        from agents.business_intelligence_agents import (  # type: ignore
            MarketResearcherAgent,
            DataAnalystAgent,
            StrategyConsultantAgent,
            FinancialAnalystAgent,
            BusinessReporterAgent,
        )

        return {
            "market_researcher": MarketResearcherAgent.create(),
            "data_analyst": DataAnalystAgent.create(),
            "strategy_consultant": StrategyConsultantAgent.create(),
            "financial_analyst": FinancialAnalystAgent.create(),
            "business_reporter": BusinessReporterAgent.create(),
        }

    def _create_tasks(self) -> List[Any]:
        """Create the business intelligence workflow tasks."""
        # Import here to avoid circular imports
        from tasks.business_intelligence_tasks import get_business_intelligence_workflow_tasks  # type: ignore
        return get_business_intelligence_workflow_tasks(self.agents)

    def _create_crew(self) -> Crew:
        """Create the main crew with all agents and tasks."""
        return Crew(
            agents=list(self.agents.values()),
            tasks=self.tasks,
            verbose=config.VERBOSE,
            process=self.process,
        )

    def kickoff(self, inputs: Optional[Dict[str, Any]] = None) -> Any:
        """Execute the business intelligence workflow."""
        try:
            print("📊 Starting Business Intelligence Crew...")
            print(f"Process: {self.process}")
            print(f"Agents: {len(self.agents)}")
            print(f"Tasks: {len(self.tasks)}")
            print("-" * 50)

            # Use provided inputs or default
            crew_inputs = inputs or {
                "company": "TechCorp Inc.",
                "industry": "artificial_intelligence",
                "analysis_type": "market_analysis",
                "time_period": "2024_Q1",
                "geographic_scope": "global",
            }

            result = self.crew.kickoff(inputs=crew_inputs)

            print("-" * 50)
            print("💼 Business Intelligence Analysis Complete!")
            return result

        except Exception as e:
            print(f"❌ Error during business analysis: {str(e)}")
            raise

    def get_agent(self, name: str) -> Any:
        """Get a specific agent by name."""
        return self.agents.get(name)

    def get_task(self, index: int) -> Any:
        """Get a specific task by index."""
        if 0 <= index < len(self.tasks):
            return self.tasks[index]
        return None

    @staticmethod
    def get_workflow_description() -> str:
        """Get description of the business intelligence workflow."""
        return """
        Business Intelligence Workflow:
        1. Market Researcher: Conducts market analysis and competitive intelligence
        2. Data Analyst: Processes business data and generates insights
        3. Strategy Consultant: Develops strategic recommendations and roadmaps
        4. Financial Analyst: Performs financial modeling and valuation analysis
        5. Business Reporter: Creates executive reports and presentations
        """

    @staticmethod
    def get_supported_industries() -> List[str]:
        """Get list of supported industries."""
        return [
            "technology",
            "healthcare",
            "finance",
            "retail",
            "manufacturing",
            "energy",
            "real_estate",
            "education",
            "transportation",
            "entertainment",
            "agriculture",
            "pharmaceuticals",
            "automotive",
            "telecommunications",
            "consulting",
        ]

    @staticmethod
    def get_supported_analysis_types() -> List[str]:
        """Get list of supported analysis types."""
        return [
            "market_analysis",
            "competitive_intelligence",
            "customer_segmentation",
            "financial_modeling",
            "trend_analysis",
            "risk_assessment",
            "merger_acquisition",
            "product_launch",
            "pricing_strategy",
            "expansion_planning",
            "operational_efficiency",
            "customer_satisfaction",
        ]