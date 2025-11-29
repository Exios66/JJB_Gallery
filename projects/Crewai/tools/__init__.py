"""
CrewAI Tools Module
Contains custom tools for all specialized swarms.
"""

# ML Tools
from .ml_tools import (
    DatasetAnalyzerTool,
    ModelEvaluatorTool,
    FeatureImportanceTool,
    HyperparameterOptimizerTool,
)

# Research Tools
from .research_tools import (
    DataGatheringTool,
    CitationManagerTool,
    TrendAnalyzerTool,
    ResearchSynthesisTool,
)

# Business Intelligence Tools
from .business_intelligence_tools import (
    MarketAnalyzerTool,
    FinancialModelingTool,
    DataProcessingTool,
    CompetitiveIntelligenceTool,
    BusinessReportGeneratorTool,
)

# Development Tools
from .dev_tools import (
    CodeExecutorTool,
    FileManagerTool,
    CodeAnalyzerTool,
    TestGeneratorTool,
    ArchitectureAnalyzerTool,
)

# Documentation Tools
from .documentation_tools import (
    DocumentStructureTool,
    MarkdownFormatterTool,
    DocumentationValidatorTool,
    CodeExampleGeneratorTool,
)

# Content Tools
from .content_tools import (
    SEOAnalyzerTool,
    ContentAnalyzerTool,
    KeywordResearchTool,
    CompetitorContentAnalyzerTool,
)

# Academic Tools
from .academic_tools import (
    PaperAnalyzerTool,
    CitationNetworkTool,
    MethodologyEvaluatorTool,
    LiteratureGapIdentifierTool,
)

__all__ = [
    # ML Tools
    "DatasetAnalyzerTool",
    "ModelEvaluatorTool",
    "FeatureImportanceTool",
    "HyperparameterOptimizerTool",
    # Research Tools
    "DataGatheringTool",
    "CitationManagerTool",
    "TrendAnalyzerTool",
    "ResearchSynthesisTool",
    # Business Intelligence Tools
    "MarketAnalyzerTool",
    "FinancialModelingTool",
    "DataProcessingTool",
    "CompetitiveIntelligenceTool",
    "BusinessReportGeneratorTool",
    # Development Tools
    "CodeExecutorTool",
    "FileManagerTool",
    "CodeAnalyzerTool",
    "TestGeneratorTool",
    "ArchitectureAnalyzerTool",
    # Documentation Tools
    "DocumentStructureTool",
    "MarkdownFormatterTool",
    "DocumentationValidatorTool",
    "CodeExampleGeneratorTool",
    # Content Tools
    "SEOAnalyzerTool",
    "ContentAnalyzerTool",
    "KeywordResearchTool",
    "CompetitorContentAnalyzerTool",
    # Academic Tools
    "PaperAnalyzerTool",
    "CitationNetworkTool",
    "MethodologyEvaluatorTool",
    "LiteratureGapIdentifierTool",
]
