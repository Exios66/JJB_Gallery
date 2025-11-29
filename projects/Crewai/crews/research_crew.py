"""
Research Crew Orchestration.
Manages general research tasks, trend analysis, and synthesis.
"""

from crewai import Crew, Process, Agent, Task  # type: ignore
from crewai_tools import SerperDevTool  # type: ignore
from typing import Dict, Any, Optional, List
from config import config
from tools.research_tools import DataGatheringTool, CitationManagerTool, TrendAnalyzerTool, ResearchSynthesisTool


class ResearchCrew:
    """Main crew class for research workflows."""

    def __init__(self, process: str = "sequential"):
        self.process = Process.sequential if process == "sequential" else Process.hierarchical
        self.agents = self._create_agents()
        self.tasks = self._create_tasks()
        self.crew = self._create_crew()

    def _create_agents(self) -> Dict[str, Any]:
        search_tool = SerperDevTool() if config.SERPER_API_KEY else None
        base_tools = [search_tool] if search_tool else []
        
        # Research-specific tools
        data_gathering_tool = DataGatheringTool()
        citation_tool = CitationManagerTool()
        trend_tool = TrendAnalyzerTool()
        synthesis_tool = ResearchSynthesisTool()

        return {
            "lead_researcher": Agent(
                role='Lead Research Analyst',
                goal='Conduct deep, comprehensive research on technical topics',
                backstory="""You are a meticulous researcher with a knack for finding hard-to-get information.
                You are not satisfied with surface-level answers; you dig deep into reports, articles, and whitepapers
                to find the truth. You are expert at vetting sources for credibility.""",
                verbose=config.VERBOSE,
                tools=base_tools + [data_gathering_tool, citation_tool],
                allow_delegation=False
            ),
            "trend_analyst": Agent(
                role='Market Trend Analyst',
                goal='Identify emerging trends and future directions',
                backstory="""You focus on the 'next big thing'. You analyze patterns in data and news to predict
                where the industry is heading. You connect dots that others miss, linking technological shifts
                to market outcomes.""",
                verbose=config.VERBOSE,
                tools=base_tools + [trend_tool, data_gathering_tool],
                allow_delegation=False
            ),
            "research_writer": Agent(
                role='Research Synthesizer',
                goal='Compile disparate research into a cohesive narrative',
                backstory="""You are an expert editor and writer. You take raw research notes and trend analysis
                and weave them into a compelling, easy-to-read report. You organize information logically and
                highlight the most impactful findings.""",
                verbose=config.VERBOSE,
                tools=[synthesis_tool, citation_tool],
                allow_delegation=False
            )
        }

    def _create_tasks(self) -> List[Any]:
        lead_researcher = self.agents["lead_researcher"]
        trend_analyst = self.agents["trend_analyst"]
        research_writer = self.agents["research_writer"]

        task_deep_dive = Task(
            description="""Conduct a deep-dive research investigation into: {topic}
            1. Use the Data Gathering Tool to collect information from multiple sources.
            2. Define the core concepts and key players.
            3. Identify the major challenges and current solutions.
            4. Gather statistics and concrete data points.
            5. List authoritative sources and references.""",
            expected_output="Detailed research dossier with verified facts and sources.",
            agent=lead_researcher,
            output_file=config.get_output_path("research_dossier.md")
        )

        task_trends = Task(
            description="""Analyze current and future trends related to: {topic}
            1. Use the Trend Analyzer Tool to identify patterns and shifts.
            2. Identify recent shifts (last 12 months).
            3. Predict near-term developments (next 6-18 months).
            4. Analyze the impact of these trends on the broader ecosystem.
            5. Highlight opportunities and risks.""",
            expected_output="Trend analysis report with market predictions.",
            agent=trend_analyst,
            output_file=config.get_output_path("trend_analysis.md")
        )

        task_synthesis = Task(
            description="""Synthesize the research dossier and trend analysis into a final report on: {topic}
            1. Use the Research Synthesis Tool to compile findings.
            2. Create an executive summary.
            3. Integrate the deep-dive facts with the forward-looking trends.
            4. Ensure a logical flow and professional tone.
            5. Conclude with actionable insights.""",
            expected_output="Comprehensive research report suitable for strategic planning.",
            agent=research_writer,
            context=[task_deep_dive, task_trends],
            output_file=config.get_output_path("final_research_report.md")
        )

        return [task_deep_dive, task_trends, task_synthesis]

    def _create_crew(self) -> Crew:
        return Crew(
            agents=list(self.agents.values()),
            tasks=self.tasks,
            verbose=config.VERBOSE,
            process=self.process,
        )

    def kickoff(self, inputs: Optional[Dict[str, Any]] = None) -> Any:
        crew_inputs = inputs or {"topic": "General ML Trends"}
        return self.crew.kickoff(inputs=crew_inputs)

    @staticmethod
    def get_status() -> Dict[str, Any]:
        return {"agents_available": 3}
    
    @staticmethod
    def validate_environment() -> Dict[str, bool]:
        """Validate environment configuration (delegates to config)."""
        from config import config
        return config.validate_environment()
