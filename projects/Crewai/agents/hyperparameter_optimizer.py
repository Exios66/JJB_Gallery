"""
Hyperparameter Optimizer Agent for CrewAI ML workflows.
Specializes in hyperparameter tuning and optimization strategies.
"""

from crewai import Agent  # type: ignore
from crewai_tools import SerperDevTool  # type: ignore
from ..config import config


class HyperparameterOptimizerAgent:
    """Agent specialized in hyperparameter optimization for Random Forest models."""

    @staticmethod
    def create() -> Agent:
        """Create and return the Hyperparameter Optimizer agent."""

        # Initialize tools
        search_tool = SerperDevTool() if config.SERPER_API_KEY else None

        tools = []
        if search_tool:
            tools.append(search_tool)

        return Agent(
            role='Hyperparameter Optimization Expert',
            goal='Optimize Random Forest hyperparameters for maximum performance and efficiency',
            backstory="""You are a hyperparameter tuning specialist with deep knowledge of Random Forest
            algorithms and optimization techniques. You understand the trade-offs between different parameters
            like n_estimators, max_depth, min_samples_split, and max_features. You excel at designing
            efficient search strategies, interpreting optimization results, and providing clear recommendations
            for production deployment. You stay current with the latest research on ensemble optimization.""",
            verbose=config.VERBOSE,
            allow_delegation=False,  # Focus on optimization expertise
            tools=tools,
        )