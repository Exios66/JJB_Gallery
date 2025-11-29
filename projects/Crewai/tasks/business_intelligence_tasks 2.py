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
        1. Use the Market Analyzer Tool and Competitive Intelligence Tool.
        2. Analyze the target market size, growth trends, and dynamics
        3. Identify key competitors and assess their market positioning
        4. Evaluate competitive strengths, weaknesses, and strategies
        5. Analyze market segmentation and customer demographics
        6. Assess market opportunities and threats
        7. Review industry trends and emerging market forces
        8. Provide competitive intelligence and market insights

        Focus on actionable market intelligence that informs strategic decision-making.""",
        expected_output="Comprehensive market research report with competitive analysis, market trends, and strategic insights.",
        agent=agent,
        output_file=config.get_output_path("market_research_report.md"),
    )


def create_data_analysis_task(agent) -> Task:
    """Create data analysis task for business insights."""
    return Task(
        description="""Analyze business data and generate actionable insights regarding: {topic}
        1. Use the Data Processing Tool to analyze data sets.
        2. Process and analyze relevant business data sets
        3. Identify key performance indicators and metrics
        4. Discover patterns, trends, and anomalies in the data
        5. Generate data-driven insights and recommendations
        6. Create visualizations and summaries of findings
        7. Assess data quality and reliability
        8. Provide actionable recommendations based on data analysis

        Focus on transforming data into strategic business insights.""",
        expected_output="Data analysis report with insights, visualizations, and data-driven recommendations.",
        agent=agent,
        output_file=config.get_output_path("data_analysis_report.md"),
    )


def create_strategy_consulting_task(agent) -> Task:
    """Create strategy consulting task for strategic planning."""
    return Task(
        description="""Develop strategic recommendations and business roadmap for: {topic}
        1. Use the Market Analyzer Tool to inform strategy.
        2. Synthesize market research and data analysis findings
        3. Identify strategic opportunities and challenges
        4. Develop strategic recommendations and action plans
        5. Create business roadmap with milestones and timelines
        6. Assess resource requirements and implementation considerations
        7. Evaluate risks and mitigation strategies
        8. Provide strategic guidance for achieving business objectives

        Focus on creating actionable strategic plans that drive business success.""",
        expected_output="Strategic plan with recommendations, roadmap, and implementation guidance.",
        agent=agent,
        output_file=config.get_output_path("strategic_plan_report.md"),
    )


def create_financial_analysis_task(agent) -> Task:
    """Create financial analysis task for financial modeling."""
    return Task(
        description="""Perform financial analysis and modeling related to: {topic}
        1. Use the Financial Modeling Tool and Data Processing Tool.
        2. Analyze financial performance and key financial metrics
        3. Create financial models and projections
        4. Assess financial health and viability
        5. Evaluate investment requirements and returns
        6. Analyze cost structures and profitability
        7. Provide financial recommendations and risk assessment
        8. Create financial summaries and forecasts

        Focus on financial insights that support strategic decision-making.""",
        expected_output="Financial analysis report with models, forecasts, and financial recommendations.",
        agent=agent,
        output_file=config.get_output_path("financial_analysis_report.md"),
    )


def create_business_reporting_task(agent) -> Task:
    """Create business reporting task for executive summary."""
    return Task(
        description="""Create comprehensive executive business report on: {topic}
        1. Use the Business Report Generator Tool.
        2. Synthesize all analysis findings (market, data, strategy, financial)
        3. Create executive summary with key insights and recommendations
        4. Structure report for executive audience
        5. Highlight critical findings and strategic priorities
        6. Provide clear action items and next steps
        7. Ensure report is clear, concise, and actionable
        8. Create presentation-ready format

        Write in clear, executive-level language suitable for C-level decision-makers.""",
        expected_output="Comprehensive executive business report with integrated insights, recommendations, and action plans.",
        agent=agent,
        output_file=config.get_output_path("executive_business_report.md"),
    )


def get_business_intelligence_workflow_tasks(agents: Dict[str, Any]) -> List[Task]:
    """Get the complete business intelligence workflow task list in execution order.

    Args:
        agents: Dictionary mapping agent roles to agent instances

    Returns:
        List of tasks in execution order
    """
    # Create tasks in order
    task_market_research = create_market_research_task(agents["market_researcher"])
    task_data_analysis = create_data_analysis_task(agents["data_analyst"])
    task_strategy = create_strategy_consulting_task(agents["strategy_consultant"])
    task_financial = create_financial_analysis_task(agents["financial_analyst"])
    task_reporting = create_business_reporting_task(agents["business_reporter"])
    
    # Update context with actual task objects
    task_data_analysis.context = [task_market_research]
    task_strategy.context = [task_market_research, task_data_analysis]
    task_financial.context = [task_market_research, task_data_analysis]
    task_reporting.context = [task_market_research, task_data_analysis, task_strategy, task_financial]
    
    return [
        task_market_research,
        task_data_analysis,
        task_strategy,
        task_financial,
        task_reporting,
    ]
