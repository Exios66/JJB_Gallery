"""
CrewAI Tasks Package.
Exports all available task definitions.
"""

from .business_intelligence_tasks import (
    create_market_research_task,
    create_data_analysis_task,
    create_strategy_consulting_task,
    create_financial_analysis_task,
    create_business_reporting_task,
    get_business_intelligence_workflow_tasks,
)

from .research_tasks import (
    create_literature_review_task,
    create_trend_analysis_task,
    create_research_synthesis_task,
    get_research_workflow_tasks,
)

__all__ = [
    # Business Intelligence Tasks
    "create_market_research_task",
    "create_data_analysis_task",
    "create_strategy_consulting_task",
    "create_financial_analysis_task",
    "create_business_reporting_task",
    "get_business_intelligence_workflow_tasks",
    # Research Tasks
    "create_literature_review_task",
    "create_trend_analysis_task",
    "create_research_synthesis_task",
    "get_research_workflow_tasks",
]

