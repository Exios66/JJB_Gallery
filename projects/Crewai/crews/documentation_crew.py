"""
Documentation Crew Orchestration.
Manages technical writing, editing, and documentation architecture.
"""

from crewai import Crew, Process, Agent, Task  # type: ignore
from typing import Dict, Any, Optional, List
from ..config import config


class DocumentationCrew:
    """Main crew class for documentation workflows."""

    def __init__(self, process: str = "sequential"):
        self.process = Process.sequential if process == "sequential" else Process.hierarchical
        self.agents = self._create_agents()
        self.tasks = self._create_tasks()
        self.crew = self._create_crew()

    def _create_agents(self) -> Dict[str, Any]:
        return {
            "doc_architect": Agent(
                role='Documentation Architect',
                goal='Plan the structure and hierarchy of documentation sets',
                backstory="""You organize information into logical structures. You understand how users navigate documentation
                and design hierarchies that are intuitive. You define the table of contents and style guides.""",
                verbose=config.VERBOSE,
                allow_delegation=False
            ),
            "technical_writer": Agent(
                role='Senior Technical Writer',
                goal='Write clear, accurate, and user-focused documentation',
                backstory="""You translate engineering-speak into human-speak. You write guides, API references, and manuals
                that users actually want to read. You focus on clarity, brevity, and accuracy.""",
                verbose=config.VERBOSE,
                allow_delegation=False
            ),
            "doc_editor": Agent(
                role='Technical Editor',
                goal='Ensure consistency, correctness, and high-quality writing',
                backstory="""You have an eagle eye for typos and inconsistencies. You ensure all documentation adheres to
                the style guide. You verify that instructions are clear and step-by-step guides actually work.""",
                verbose=config.VERBOSE,
                allow_delegation=False
            )
        }

    def _create_tasks(self) -> List[Any]:
        doc_architect = self.agents["doc_architect"]
        technical_writer = self.agents["technical_writer"]
        doc_editor = self.agents["doc_editor"]

        task_planning = Task(
            description="""Plan the documentation structure for: {topic}
            1. Identify the target audience (devs, users, admins).
            2. Define the required sections (e.g., Getting Started, API Ref, Tutorials).
            3. Create a detailed Table of Contents.
            4. Define terminology and conventions.""",
            expected_output="Documentation plan and table of contents.",
            agent=doc_architect,
            output_file=config.get_output_path("docs_plan.md")
        )

        task_writing = Task(
            description="""Write the core documentation based on the plan for: {topic}
            1. Draft content for each section.
            2. Include code examples and prerequisites.
            3. Use clear headings and lists.
            4. Address common user pain points.""",
            expected_output="Draft documentation content.",
            agent=technical_writer,
            context=[task_planning],
            output_file=config.get_output_path("docs_draft.md")
        )

        task_editing = Task(
            description="""Review and polish the documentation for: {topic}
            1. Check for clarity, flow, and tone.
            2. Verify technical accuracy (where possible).
            3. Fix grammar and style issues.
            4. Format for final publication (Markdown).""",
            expected_output="Final, polished technical documentation.",
            agent=doc_editor,
            context=[task_planning, task_writing],
            output_file=config.get_output_path("final_documentation.md")
        )

        return [task_planning, task_writing, task_editing]

    def _create_crew(self) -> Crew:
        return Crew(
            agents=list(self.agents.values()),
            tasks=self.tasks,
            verbose=config.VERBOSE,
            process=self.process,
        )

    def kickoff(self, inputs: Optional[Dict[str, Any]] = None) -> Any:
        crew_inputs = inputs or {"topic": "System Architecture"}
        return self.crew.kickoff(inputs=crew_inputs)

    @staticmethod
    def get_status() -> Dict[str, Any]:
        return {"agents_available": 3}
