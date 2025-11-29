"""
Content Research Crew Orchestration.
Manages content strategy, SEO research, outlining, and drafting.
"""

from crewai import Crew, Process, Agent, Task  # type: ignore
from crewai_tools import SerperDevTool  # type: ignore
from typing import Dict, Any, Optional, List
from config import config
from tools.content_tools import SEOAnalyzerTool, ContentAnalyzerTool, KeywordResearchTool, CompetitorContentAnalyzerTool


class ResearchContentCrew:
    """Main crew class for content research workflows."""

    def __init__(self, process: str = "sequential"):
        self.process = Process.sequential if process == "sequential" else Process.hierarchical
        self.agents = self._create_agents()
        self.tasks = self._create_tasks()
        self.crew = self._create_crew()

    def _create_agents(self) -> Dict[str, Any]:
        search_tool = SerperDevTool() if config.SERPER_API_KEY else None
        base_tools = [search_tool] if search_tool else []
        
        # Content and SEO tools
        seo_analyzer = SEOAnalyzerTool()
        keyword_researcher = KeywordResearchTool()
        content_analyzer = ContentAnalyzerTool()
        competitor_analyzer = CompetitorContentAnalyzerTool()

        return {
            "seo_strategist": Agent(
                role='SEO Content Strategist',
                goal='Identify high-value keywords and content gaps',
                backstory="""You are an expert in Search Engine Optimization. You know how to find keywords that have
                high traffic but low competition. You understand search intent and how to structure content to rank well.""",
                verbose=config.VERBOSE,
                tools=base_tools + [seo_analyzer, keyword_researcher, competitor_analyzer],
                allow_delegation=False
            ),
            "content_outliner": Agent(
                role='Content Architect',
                goal='Create detailed, logical outlines for long-form content',
                backstory="""You are a master of structure. You take a topic and break it down into logical headers,
                subheaders, and bullet points. You ensure the narrative flow makes sense and covers all necessary angles.""",
                verbose=config.VERBOSE,
                tools=[keyword_researcher, content_analyzer],
                allow_delegation=False
            ),
            "technical_writer": Agent(
                role='Technical Content Writer',
                goal='Draft high-quality, accurate, and engaging technical content',
                backstory="""You are a writer who loves technology. You can explain complex concepts in simple terms
                without dumbing them down. Your writing is crisp, clear, and free of fluff. You follow the provided outline
                rigorously.""",
                verbose=config.VERBOSE,
                tools=[content_analyzer, seo_analyzer],
                allow_delegation=False
            )
        }

    def _create_tasks(self) -> List[Any]:
        seo_strategist = self.agents["seo_strategist"]
        content_outliner = self.agents["content_outliner"]
        technical_writer = self.agents["technical_writer"]

        task_keyword_research = Task(
            description="""Perform SEO keyword research for the topic: {topic}
            1. Use the Keyword Researcher Tool and SEO Analyzer Tool.
            2. Identify primary and secondary keywords.
            3. Analyze search intent (informational vs transactional).
            4. Identify questions people are asking (PAA).
            5. Analyze top-ranking competitors for this topic.""",
            expected_output="SEO strategy document with keyword list and competitor analysis.",
            agent=seo_strategist,
            output_file=config.get_output_path("seo_strategy.md")
        )

        task_outlining = Task(
            description="""Create a comprehensive content outline for: {topic}
            1. Use the Content Analyzer Tool to structure the outline.
            2. Use H2/H3 headers based on the SEO strategy.
            3. Include key talking points for each section.
            4. Specify where to include diagrams or code snippets.
            5. Ensure a logical flow from introduction to conclusion.""",
            expected_output="Detailed content outline.",
            agent=content_outliner,
            context=[task_keyword_research],
            output_file=config.get_output_path("content_outline.md")
        )

        task_drafting = Task(
            description="""Draft a complete technical article based on the outline for: {topic}
            1. Use the Content Analyzer Tool to check readability and flow.
            2. Write engaging, clear prose.
            3. Incorporate the target keywords naturally.
            4. Include placeholder code blocks where appropriate.
            5. Write a compelling introduction and conclusion.""",
            expected_output="First draft of the technical article.",
            agent=technical_writer,
            context=[task_keyword_research, task_outlining],
            output_file=config.get_output_path("content_draft.md")
        )

        return [task_keyword_research, task_outlining, task_drafting]

    def _create_crew(self) -> Crew:
        return Crew(
            agents=list(self.agents.values()),
            tasks=self.tasks,
            verbose=config.VERBOSE,
            process=self.process,
        )

    def kickoff(self, inputs: Optional[Dict[str, Any]] = None) -> Any:
        crew_inputs = inputs or {"topic": "AI Content Trends"}
        return self.crew.kickoff(inputs=crew_inputs)

    @staticmethod
    def get_status() -> Dict[str, Any]:
        return {"agents_available": 3}
    
    @staticmethod
    def validate_environment() -> Dict[str, bool]:
        """Validate environment configuration (delegates to config)."""
        from config import config
        return config.validate_environment()
