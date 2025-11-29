
# Tool availability mapping for UI
CREW_TOOLS = {
    "ml": ["DatasetAnalyzerTool", "ModelEvaluatorTool", "FeatureImportanceTool", "HyperparameterOptimizerTool"],
    "research": ["DataGatheringTool", "CitationManagerTool", "TrendAnalyzerTool", "ResearchSynthesisTool"],
    "research_academic": ["PaperAnalyzerTool", "CitationNetworkTool", "MethodologyEvaluatorTool", "LiteratureGapIdentifierTool"],
    "research_content": ["SEOAnalyzerTool", "ContentAnalyzerTool", "KeywordResearchTool", "CompetitorContentAnalyzerTool"],
    "business_intelligence": ["MarketAnalyzerTool", "FinancialModelingTool", "DataProcessingTool", "CompetitiveIntelligenceTool"],
    "dev_code": ["CodeExecutorTool", "FileManagerTool", "CodeAnalyzerTool", "TestGeneratorTool", "ArchitectureAnalyzerTool"],
    "documentation": ["DocumentStructureTool", "MarkdownFormatterTool", "DocumentationValidatorTool", "CodeExampleGeneratorTool"]
}

