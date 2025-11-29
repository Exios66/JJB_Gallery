"""
CrewAI Swarms Package.
Exports all available specialized crews.
"""

from .ml_crew import MLCrew
from .research_crew import ResearchCrew
from .research_academic_crew import ResearchAcademicCrew
from .research_content_crew import ResearchContentCrew
from .business_intelligence_crew import BusinessIntelligenceCrew
from .dev_code_crew import DevCodeCrew
from .documentation_crew import DocumentationCrew

__all__ = [
    "MLCrew",
    "ResearchCrew",
    "ResearchAcademicCrew",
    "ResearchContentCrew",
    "BusinessIntelligenceCrew",
    "DevCodeCrew",
    "DocumentationCrew",
]

