"""
Research Task Definitions for CrewAI Research Swarm.
Contains tasks for complete ML research analysis workflow.
"""

from crewai import Task  # type: ignore
from typing import List, Dict, Any, Optional
from ..config import config


def create_literature_review_task(agent) -> Task:
    """Create literature review task for academic research."""
    return Task(
        description="""Conduct a comprehensive review of academic literature on Random Forest and ensemble methods:
        1. Identify seminal papers from Breiman and other key researchers
        2. Analyze recent advancements in ensemble learning (2001-present)
        3. Review theoretical foundations and mathematical formulations
        4. Examine extensions and variations of Random Forest algorithms
        5. Assess current research gaps and open problems
        6. Evaluate the impact of Random Forest on the broader ML field

        Provide detailed analysis with proper citations and critical evaluation.""",
        expected_output="Comprehensive literature review with key papers, theoretical analysis, and research synthesis.",
        agent=agent,
        output_file=config.get_output_path("literature_review_report.md"),
    )


def create_trend_analysis_task(agent) -> Task:
    """Create trend analysis task for ML industry developments."""
    return Task(
        description="""Analyze current and emerging trends in Random Forest and ensemble learning:
        1. Industry adoption patterns and use cases
        2. Integration with other ML techniques (XGBoost, LightGBM, etc.)
        3. Cloud platform support and tooling developments
        4. Performance optimization trends and benchmarks
        5. Emerging applications in new domains
        6. Competitive landscape and alternative approaches
        7. Future predictions and technology roadmap

        Focus on practical industry implications and market dynamics.""",
        expected_output="Industry trend analysis with market insights, adoption patterns, and future predictions.",
        agent=agent,
        output_file=config.get_output_path("trend_analysis_report.md"),
        context=[create_literature_review_task.__name__],
    )


def create_innovation_scouting_task(agent) -> Task:
    """Create innovation scouting task for novel applications."""
    return Task(
        description="""Discover innovative applications and breakthrough uses of Random Forest:
        1. Identify unconventional applications across different industries
        2. Analyze novel combinations with other AI technologies
        3. Examine creative problem-solving approaches using ensembles
        4. Review startup innovations and research lab breakthroughs
        5. Assess potential for interdisciplinary applications
        6. Evaluate scalability challenges and solutions
        7. Propose new research directions and applications

        Focus on creative and forward-thinking applications that expand the boundaries of Random Forest use.""",
        expected_output="Innovation analysis with novel applications, breakthrough ideas, and future research directions.",
        agent=agent,
        output_file=config.get_output_path("innovation_scouting_report.md"),
        context=[create_trend_analysis_task.__name__],
    )


def create_research_synthesis_task(agent) -> Task:
    """Create research synthesis task for comprehensive summary."""
    return Task(
        description="""Synthesize all research findings into a comprehensive, actionable report:
        1. Integrate academic literature with industry trends
        2. Connect theoretical foundations with practical applications
        3. Highlight key insights and breakthrough opportunities
        4. Provide clear recommendations for Random Forest development
        5. Identify research gaps and future directions
        6. Create an executive summary for stakeholders
        7. Suggest implementation priorities and next steps

        Write in clear, accessible language suitable for both researchers and practitioners.""",
        expected_output="Comprehensive research synthesis with integrated insights, recommendations, and actionable next steps.",
        agent=agent,
        output_file=config.get_output_path("research_synthesis_report.md"),
        context=[
            create_literature_review_task.__name__,
            create_trend_analysis_task.__name__,
            create_innovation_scouting_task.__name__,
        ],
    )


def get_research_workflow_tasks(agents: Dict[str, Any]) -> List[Task]:
    """Get the complete research workflow task list in execution order.

    Args:
        agents: Dictionary mapping agent roles to agent instances

    Returns:
        List of tasks in execution order
    """
    return [
        create_literature_review_task(agents["literature_reviewer"]),
        create_trend_analysis_task(agents["trend_analyzer"]),
        create_innovation_scouting_task(agents["innovation_scout"]),
        create_research_synthesis_task(agents["research_summarizer"]),
    ]