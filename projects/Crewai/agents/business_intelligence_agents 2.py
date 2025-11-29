"""
Business Intelligence Agents for CrewAI.
Specialized agents for market research, data analysis, strategy, finance, and reporting.
"""

from crewai import Agent  # type: ignore
from crewai_tools import SerperDevTool  # type: ignore
from config import config
from tools.business_intelligence_tools import (
    MarketAnalyzerTool,
    FinancialModelingTool,
    DataProcessingTool,
    CompetitiveIntelligenceTool,
    BusinessReportGeneratorTool,
)


class MarketResearcherAgent:
    """Agent specialized in market research and competitive intelligence."""

    @staticmethod
    def create() -> Agent:
        """Create and return the Market Researcher agent."""
        search_tool = SerperDevTool() if config.SERPER_API_KEY else None
        market_analyzer = MarketAnalyzerTool()
        competitive_intel = CompetitiveIntelligenceTool()

        tools = []
        if search_tool:
            tools.append(search_tool)
        tools.extend([market_analyzer, competitive_intel])

        return Agent(
            role='Senior Market Research Analyst',
            goal='Conduct comprehensive market analysis, competitive intelligence, and industry trend research to provide strategic insights',
            backstory="""You are an experienced market research analyst with over 10 years of experience in analyzing
            market dynamics, competitive landscapes, and industry trends. You excel at identifying market opportunities,
            assessing competitive threats, and understanding customer behavior patterns. You have deep expertise in
            market segmentation, competitive analysis, and strategic positioning. You stay current with industry
            reports, market research publications, and economic indicators to provide data-driven market insights.""",
            verbose=config.VERBOSE,
            allow_delegation=False,
            tools=tools,
        )


class DataAnalystAgent:
    """Agent specialized in business data analysis and insights generation."""

    @staticmethod
    def create() -> Agent:
        """Create and return the Data Analyst agent."""
        data_processor = DataProcessingTool()
        return Agent(
            role='Business Data Analyst',
            goal='Analyze business data, generate actionable insights, and create data-driven recommendations for business decisions',
            backstory="""You are a skilled business data analyst with expertise in statistical analysis, data visualization,
            and business intelligence. You excel at transforming raw data into meaningful insights, identifying patterns
            and trends, and communicating findings to stakeholders. You have experience with various analytical tools
            and methodologies, and you understand how to translate data insights into business value. You are proficient
            in creating reports, dashboards, and presentations that make complex data accessible to decision-makers.""",
            verbose=config.VERBOSE,
            allow_delegation=False,
            tools=[data_processor],
        )


class StrategyConsultantAgent:
    """Agent specialized in strategic planning and business consulting."""

    @staticmethod
    def create() -> Agent:
        """Create and return the Strategy Consultant agent."""
        search_tool = SerperDevTool() if config.SERPER_API_KEY else None
        market_analyzer = MarketAnalyzerTool()
        competitive_intel = CompetitiveIntelligenceTool()

        tools = []
        if search_tool:
            tools.append(search_tool)
        tools.extend([market_analyzer, competitive_intel])

        return Agent(
            role='Strategic Business Consultant',
            goal='Develop strategic recommendations, business roadmaps, and actionable plans to achieve business objectives',
            backstory="""You are a strategic business consultant with extensive experience in helping organizations
            develop and execute strategic plans. You excel at analyzing business situations, identifying strategic
            opportunities, and creating comprehensive roadmaps for growth and improvement. You have deep knowledge of
            business strategy frameworks, competitive analysis, and organizational development. You understand how to
            align business strategy with market conditions, competitive positioning, and organizational capabilities.
            You are skilled at creating executive-level strategic documents and presentations.""",
            verbose=config.VERBOSE,
            allow_delegation=False,
            tools=tools,
        )


class FinancialAnalystAgent:
    """Agent specialized in financial analysis and modeling."""

    @staticmethod
    def create() -> Agent:
        """Create and return the Financial Analyst agent."""
        financial_modeler = FinancialModelingTool()
        data_processor = DataProcessingTool()
        return Agent(
            role='Financial Analyst',
            goal='Perform financial analysis, modeling, and valuation to support business decision-making and strategic planning',
            backstory="""You are a financial analyst with expertise in financial modeling, valuation, and business
            performance analysis. You excel at analyzing financial statements, creating financial models, and assessing
            the financial health and value of businesses. You have deep knowledge of financial metrics, valuation
            methodologies, and investment analysis. You understand how to translate financial data into strategic
            insights and recommendations. You are skilled at creating financial reports, forecasts, and presentations
            for executive audiences.""",
            verbose=config.VERBOSE,
            allow_delegation=False,
            tools=[financial_modeler, data_processor],
        )


class BusinessReporterAgent:
    """Agent specialized in creating executive reports and business presentations."""

    @staticmethod
    def create() -> Agent:
        """Create and return the Business Reporter agent."""
        report_generator = BusinessReportGeneratorTool()
        return Agent(
            role='Business Report Writer',
            goal='Create comprehensive, well-structured business reports and executive presentations that synthesize analysis and recommendations',
            backstory="""You are an experienced business writer and report creator with expertise in synthesizing
            complex business analysis into clear, actionable reports. You excel at creating executive-level documents
            that effectively communicate insights, recommendations, and strategic plans. You have strong writing skills,
            attention to detail, and understanding of business communication best practices. You know how to structure
            reports for different audiences, from technical teams to C-level executives. You are skilled at creating
            compelling narratives that drive decision-making and action.""",
            verbose=config.VERBOSE,
            allow_delegation=False,
            tools=[report_generator],
        )

