"""
Literature Reviewer Agent for CrewAI Research Swarm.
Specializes in academic research, papers, and scholarly analysis.
"""

from crewai import Agent  # type: ignore
from crewai_tools import SerperDevTool  # type: ignore
from ..config import config


class LiteratureReviewerAgent:
    """Agent specialized in academic literature review and research analysis."""

    @staticmethod
    def create() -> Agent:
        """Create and return the Literature Reviewer agent."""

        # Initialize tools
        search_tool = SerperDevTool() if config.SERPER_API_KEY else None

        tools = []
        if search_tool:
            tools.append(search_tool)

        return Agent(
            role='Senior Literature Reviewer',
            goal='Conduct comprehensive reviews of academic papers and research on machine learning and Random Forest algorithms',
            backstory="""You are a distinguished academic researcher with a PhD in Machine Learning and over 15 years
            of experience in reviewing scientific literature. You excel at identifying seminal papers, analyzing
            research methodologies, and synthesizing complex theoretical concepts. You have a particular expertise
            in ensemble methods and decision tree algorithms, and you stay current with the latest developments
            in the field through rigorous scholarly analysis.""",
            verbose=config.VERBOSE,
            allow_delegation=False,  # Focus on independent research
            tools=tools,
        )