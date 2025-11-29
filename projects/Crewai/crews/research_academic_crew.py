"""
Academic Research Crew Orchestration.
Manages scholarly research, literature reviews, and academic synthesis.
"""

from crewai import Crew, Process, Agent, Task  # type: ignore
from crewai_tools import SerperDevTool  # type: ignore
from typing import Dict, Any, Optional, List
from config import config
from tools.academic_tools import PaperAnalyzerTool, CitationNetworkTool, MethodologyEvaluatorTool, LiteratureGapIdentifierTool
from tools.research_tools import CitationManagerTool


class ResearchAcademicCrew:
    """Main crew class for academic research workflows."""

    def __init__(self, process: str = "sequential"):
        self.process = Process.sequential if process == "sequential" else Process.hierarchical
        self.agents = self._create_agents()
        self.tasks = self._create_tasks()
        self.crew = self._create_crew()

    def _create_agents(self) -> Dict[str, Any]:
        search_tool = SerperDevTool() if config.SERPER_API_KEY else None
        base_tools = [search_tool] if search_tool else []
        
        # Academic research tools
        paper_analyzer = PaperAnalyzerTool()
        citation_network = CitationNetworkTool()
        methodology_evaluator = MethodologyEvaluatorTool()
        gap_identifier = LiteratureGapIdentifierTool()
        citation_manager = CitationManagerTool()

        return {
            "literature_reviewer": Agent(
                role='Literature Review Specialist',
                goal='Find and summarize seminal and recent academic papers',
                backstory="""You are a Ph.D. candidate with a talent for finding the most relevant papers in a vast sea of
                publications. You use Google Scholar, arXiv, and other databases effectively. You quickly grasp the
                main contributions of a paper.""",
                verbose=config.VERBOSE,
                tools=base_tools + [paper_analyzer, citation_network, citation_manager],
                allow_delegation=False
            ),
            "methodology_analyst": Agent(
                role='Methodology Critic',
                goal='Critically analyze research methods and experimental designs',
                backstory="""You are meticulous about scientific rigor. You examine the 'Methods' section of papers to ensure
                experiments are valid, reproducible, and statistically sound. You identify flaws and limitations that
                authors might try to hide.""",
                verbose=config.VERBOSE,
                tools=[methodology_evaluator, paper_analyzer],
                allow_delegation=False
            ),
            "academic_synthesizer": Agent(
                role='Academic Review Writer',
                goal='Write comprehensive literature reviews and meta-analyses',
                backstory="""You are a published academic writer. You know how to structure a literature review to tell a
                story of scientific progress. You synthesize conflicting findings and identify gaps in the current body
                of knowledge.""",
                verbose=config.VERBOSE,
                tools=[gap_identifier, citation_manager, citation_network],
                allow_delegation=False
            )
        }

    def _create_tasks(self) -> List[Any]:
        literature_reviewer = self.agents["literature_reviewer"]
        methodology_analyst = self.agents["methodology_analyst"]
        academic_synthesizer = self.agents["academic_synthesizer"]

        task_lit_search = Task(
            description="""Conduct a systematic literature search on: {topic}
            1. Identify 5-10 seminal papers (historical foundation).
            2. Identify 5-10 state-of-the-art papers (last 2-3 years).
            3. Summarize the key contribution of each paper.
            4. Extract citation counts and venue impact factors.""",
            expected_output="Annotated bibliography of key papers.",
            agent=literature_reviewer,
            output_file=config.get_output_path("annotated_bibliography.md")
        )

        task_method_analysis = Task(
            description="""Analyze the methodologies used in the identified papers for: {topic}
            1. Compare experimental setups and datasets used.
            2. Evaluate the statistical validity of the results.
            3. Identify common limitations or assumptions.
            4. Contrast different theoretical approaches.""",
            expected_output="Critical methodology analysis report.",
            agent=methodology_analyst,
            context=[task_lit_search],
            output_file=config.get_output_path("methodology_analysis.md")
        )

        task_review_writing = Task(
            description="""Write a comprehensive academic literature review on: {topic}
            1. Introduction defining the scope.
            2. Thematic organization of the literature.
            3. Critical discussion of methodologies (incorporating analyst findings).
            4. Identification of research gaps and future directions.
            5. Standard academic citation format.""",
            expected_output="Full academic literature review paper.",
            agent=academic_synthesizer,
            context=[task_lit_search, task_method_analysis],
            output_file=config.get_output_path("literature_review_paper.md")
        )

        return [task_lit_search, task_method_analysis, task_review_writing]

    def _create_crew(self) -> Crew:
        return Crew(
            agents=list(self.agents.values()),
            tasks=self.tasks,
            verbose=config.VERBOSE,
            process=self.process,
        )

    def kickoff(self, inputs: Optional[Dict[str, Any]] = None) -> Any:
        crew_inputs = inputs or {"topic": "Machine Learning Theory"}
        return self.crew.kickoff(inputs=crew_inputs)

    @staticmethod
    def get_status() -> Dict[str, Any]:
        return {"agents_available": 3}
    
    @staticmethod
    def validate_environment() -> Dict[str, bool]:
        """Validate environment configuration (delegates to config)."""
        from config import config
        return config.validate_environment()
