"""
ML Crew Orchestration for CrewAI.
Manages machine learning analysis and random forest evaluation with a specialized team.
"""

from crewai import Crew, Process, Agent, Task  # type: ignore
from typing import Dict, Any, Optional, List
from config import config
from tools.ml_tools import DatasetAnalyzerTool, ModelEvaluatorTool, FeatureImportanceTool, HyperparameterOptimizerTool


class MLCrew:
    """Main crew class for ML analysis workflows."""

    def __init__(self, process: str = "sequential"):
        self.process = Process.sequential if process == "sequential" else Process.hierarchical
        self.agents = self._create_agents()
        self.tasks = self._create_tasks()
        self.crew = self._create_crew()

    def _create_agents(self) -> Dict[str, Any]:
        """Create specialized ML agents."""
        return {
            "data_scientist": Agent(
                role='Senior Data Scientist',
                goal='Analyze datasets, clean data, and propose feature engineering strategies',
                backstory="""You are an expert data scientist with a Ph.D. in Statistics. You excel at exploratory data analysis,
                identifying data quality issues, and crafting meaningful features from raw data. You have deep knowledge of
                statistical distributions and correlation analysis.""",
                verbose=config.VERBOSE,
                tools=[DatasetAnalyzerTool()],
                allow_delegation=False
            ),
            "ml_engineer": Agent(
                role='Machine Learning Engineer',
                goal='Design, train, and optimize Random Forest models',
                backstory="""You are a production-focused ML Engineer. You specialize in building robust, scalable machine
                learning pipelines. You have extensive experience with Scikit-Learn and ensemble methods, particularly
                Random Forest. You know how to tune hyperparameters to squeeze out the last bit of performance.""",
                verbose=config.VERBOSE,
                tools=[HyperparameterOptimizerTool()],
                allow_delegation=False
            ),
            "model_evaluator": Agent(
                role='Model Evaluation Specialist',
                goal='Rigorously test models and analyze performance metrics',
                backstory="""You are a skeptic by nature. Your job is to find where models fail. You analyze confusion matrices,
                ROC curves, and feature importance plots to ensure the model isn't just memorizing the data. You focus on
                generalization and robustness.""",
                verbose=config.VERBOSE,
                tools=[ModelEvaluatorTool(), FeatureImportanceTool()],
                allow_delegation=False
            ),
             "ml_reporter": Agent(
                role='ML Technical Writer',
                goal='Synthesize technical results into comprehensive reports',
                backstory="""You bridge the gap between code and stakeholders. You take complex metrics and technical details
                and weave them into a clear, actionable narrative. You ensure the final report explains not just 'what' happened,
                but 'why' it matters.""",
                verbose=config.VERBOSE,
                allow_delegation=False
            )
        }

    def _create_tasks(self) -> List[Any]:
        """Create ML workflow tasks."""
        data_scientist = self.agents["data_scientist"]
        ml_engineer = self.agents["ml_engineer"]
        model_evaluator = self.agents["model_evaluator"]
        ml_reporter = self.agents["ml_reporter"]

        task_eda = Task(
            description="""Perform comprehensive Exploratory Data Analysis (EDA) on the dataset related to: {topic}
            1. Use the DatasetAnalyzerTool to analyze the data structure.
            2. Analyze data distribution, missing values, and outliers.
            3. Identify correlations and potential data quality issues.
            4. Propose specific feature engineering steps.
            5. assess class balance (if classification) or target distribution.""",
            expected_output="Detailed EDA report with data quality assessment and feature engineering plan.",
            agent=data_scientist,
            output_file=config.get_output_path("ml_eda_report.md")
        )

        task_training = Task(
            description="""Based on the EDA, design and train a Random Forest model for: {topic}
            1. Use the HyperparameterOptimizerTool to find optimal settings.
            2. Implement the proposed feature engineering.
            3. Select initial hyperparameters.
            4. Train the model using cross-validation.
            5. Explore hyperparameter optimization strategies.""",
            expected_output="Model training log with selected hyperparameters and cross-validation scores.",
            agent=ml_engineer,
            context=[task_eda],
            output_file=config.get_output_path("ml_training_log.md")
        )

        task_evaluation = Task(
            description="""Evaluate the trained model's performance:
            1. Use the ModelEvaluatorTool to generate metrics.
            2. Use the FeatureImportanceTool to explain model decisions.
            3. Analyze precision, recall, F1-score, or RMSE/MAE.
            4. Generate and interpret feature importance plots.
            5. Check for overfitting or underfitting.
            6. Provide recommendations for model improvement.""",
            expected_output="Comprehensive model evaluation report with metrics and feature importance analysis.",
            agent=model_evaluator,
            context=[task_training],
            output_file=config.get_output_path("ml_evaluation_report.md")
        )

        task_reporting = Task(
            description="""Synthesize all findings into a final ML project report for: {topic}
            1. Executive summary of the problem and solution.
            2. Key data insights from EDA.
            3. Model approach and configuration.
            4. Final performance metrics and what they mean for the business/use-case.
            5. Next steps and deployment recommendations.""",
            expected_output="Final ML project report suitable for technical stakeholders.",
            agent=ml_reporter,
            context=[task_eda, task_training, task_evaluation],
            output_file=config.get_output_path("ml_final_report.md")
        )

        return [task_eda, task_training, task_evaluation, task_reporting]

    def _create_crew(self) -> Crew:
        """Create the main crew."""
        return Crew(
            agents=list(self.agents.values()),
            tasks=self.tasks,
            verbose=config.VERBOSE,
            process=self.process,
        )

    def kickoff(self, inputs: Optional[Dict[str, Any]] = None) -> Any:
        """Execute the workflow."""
        crew_inputs = inputs or {"topic": "Random Forest Classification"}
        return self.crew.kickoff(inputs=crew_inputs)

    @staticmethod
    def get_status() -> Dict[str, Any]:
        return {"agents_available": 4}
    
    @staticmethod
    def validate_environment() -> Dict[str, bool]:
        """Validate environment configuration (delegates to config)."""
        from config import config
        return config.validate_environment()
