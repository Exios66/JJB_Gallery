"""
Business Intelligence Task Definitions for CrewAI.
Contains tasks for complete business intelligence analysis workflow.
"""

from crewai import Task  # type: ignore
from typing import List, Dict, Any
from config import config


def create_market_research_task(agent) -> Task:
    """Create market research task for competitive intelligence."""
    return Task(
        description="""Conduct comprehensive market research and competitive analysis on topic: {topic}
        1. Analyze the target market size, growth trends, and dynamics
        2. Identify key competitors and assess their market positioning
        3. Evaluate competitive strengths, weaknesses, and strategies
        4. Analyze market segmentation and customer demographics
        5. Assess market opportunities and threats
        6. Review industry trends and emerging market forces
        7. Provide competitive intelligence and market insights

        Focus on actionable market intelligence that informs strategic decision-making.""",
        expected_output="Comprehensive market research report with competitive analysis, market trends, and strategic insights.",
        agent=agent,
        output_file=config.get_output_path("market_research_report.md"),
    )


def create_data_analysis_task(agent) -> Task:
    """Create data analysis task for business insights."""
    return Task(
        description="""Analyze business data and generate actionable insights regarding: {topic}
        1. Process and analyze relevant business data sets
        2. Identify key performance indicators and metrics
        3. Discover patterns, trends, and anomalies in the data
        4. Generate data-driven insights and recommendations
        5. Create visualizations and summaries of findings
        6. Assess data quality and reliability
        7. Provide actionable recommendations based on data analysis

        Focus on transforming data into strategic business insights.""",
        expected_output="Data analysis report with insights, visualizations, and data-driven recommendations.",
        agent=agent,
        output_file=config.get_output_path("data_analysis_report.md"),
        context=[create_market_research_task.__name__],
    )


def create_strategy_consulting_task(agent) -> Task:
    """Create strategy consulting task for strategic planning."""
    return Task(
        description="""Develop strategic recommendations and business roadmap for: {topic}
        1. Synthesize market research and data analysis findings
        2. Identify strategic opportunities and challenges
        3. Develop strategic recommendations and action plans
        4. Create business roadmap with milestones and timelines
        5. Assess resource requirements and implementation considerations
        6. Evaluate risks and mitigation strategies
        7. Provide strategic guidance for achieving business objectives

        Focus on creating actionable strategic plans that drive business success.""",
        expected_output="Strategic plan with recommendations, roadmap, and implementation guidance.",
        agent=agent,
        output_file=config.get_output_path("strategic_plan_report.md"),
        context=[
            create_market_research_task.__name__,
            create_data_analysis_task.__name__,
        ],
    )


def create_financial_analysis_task(agent) -> Task:
    """Create financial analysis task for financial modeling."""
    return Task(
        description="""Perform financial analysis and modeling related to: {topic}
        1. Analyze financial performance and key financial metrics
        2. Create financial models and projections
        3. Assess financial health and viability
        4. Evaluate investment requirements and returns
        5. Analyze cost structures and profitability
        6. Provide financial recommendations and risk assessment
        7. Create financial summaries and forecasts

        Focus on financial insights that support strategic decision-making.""",
        expected_output="Financial analysis report with models, forecasts, and financial recommendations.",
        agent=agent,
        output_file=config.get_output_path("financial_analysis_report.md"),
        context=[
            create_market_research_task.__name__,
            create_data_analysis_task.__name__,
        ],
    )


def create_business_reporting_task(agent) -> Task:
    """Create business reporting task for executive summary."""
    return Task(
        description="""Create comprehensive executive business report on: {topic}
        1. Synthesize all analysis findings (market, data, strategy, financial)
        2. Create executive summary with key insights and recommendations
        3. Structure report for executive audience
        4. Highlight critical findings and strategic priorities
        5. Provide clear action items and next steps
        6. Ensure report is clear, concise, and actionable
        7. Create presentation-ready format

        Write in clear, executive-level language suitable for C-level decision-makers.""",
        expected_output="Comprehensive executive business report with integrated insights, recommendations, and action plans.",
        agent=agent,
        output_file=config.get_output_path("executive_business_report.md"),
        context=[
            create_market_research_task.__name__,
            create_data_analysis_task.__name__,
            create_strategy_consulting_task.__name__,
            create_financial_analysis_task.__name__,
        ],
    )


def get_business_intelligence_workflow_tasks(agents: Dict[str, Any]) -> List[Task]:
    """Get the complete business intelligence workflow task list in execution order.

    Args:
        agents: Dictionary mapping agent roles to agent instances

    Returns:
        List of tasks in execution order
    """
    return [
        create_market_research_task(agents["market_researcher"]),
        create_data_analysis_task(agents["data_analyst"]),
        create_strategy_consulting_task(agents["strategy_consultant"]),
        create_financial_analysis_task(agents["financial_analyst"]),
        create_business_reporting_task(agents["business_reporter"]),
    ]
