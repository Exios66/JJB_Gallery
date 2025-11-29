"""
Meta-Agent Router for CrewAI.
Routes user queries to the appropriate agent swarm.
"""

from crewai import Agent, Task, Crew, Process  # type: ignore
from typing import Dict, Any
from config import config


class MetaRouter:
    """Routes queries to appropriate crews."""

    @staticmethod
    def route_query(query: str) -> str:
        """
        Analyze the query and return the best crew type.
        Returns one of: 'ml', 'research', 'research_academic', 'research_content', 
                       'business_intelligence', 'dev_code', 'documentation'
        """
        router_agent = Agent(
            role='Swarm Router',
            goal='Route user queries to the correct agent swarm',
            backstory="You are an intelligent dispatcher that understands user intent and routes tasks to specialized teams.",
            verbose=True,
            allow_delegation=False
        )

        router_task = Task(
            description=f"""Analyze the following user query and determine which agent swarm is best suited to handle it.
            Query: "{query}"

            Available Swarms:
            1. ml: Machine Learning analysis, Random Forest models, training, evaluation
            2. research: General research, trends, broad topics
            3. research_academic: Academic papers, literature reviews, scholarly sources
            4. research_content: Content strategy, blog outlines, writing
            5. business_intelligence: Market analysis, competitors, finance, strategy
            6. dev_code: Writing code, python scripts, software development
            7. documentation: Technical documentation, manuals, guides

            Return ONLY the key of the chosen swarm (e.g., 'ml', 'research', 'business_intelligence'). Do not add any other text.""",
            expected_output="A single string representing the chosen crew type.",
            agent=router_agent
        )

        crew = Crew(
            agents=[router_agent],
            tasks=[router_task],
            verbose=False
        )

        result = crew.kickoff()
        return str(result).strip().lower()

