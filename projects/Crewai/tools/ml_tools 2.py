"""
Custom ML Tools for CrewAI agents.
Provides specialized tools for machine learning operations.
"""

from crewai.tools.base_tool import BaseTool  # type: ignore
from typing import Any, Type
from pydantic import BaseModel, Field  # type: ignore
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import cross_val_score
from sklearn.metrics import classification_report, mean_squared_error, r2_score
import json
import os
from pathlib import Path


class DatasetAnalyzerTool(BaseTool):
    """Tool for analyzing datasets and providing statistical summaries."""

    name: str = "Dataset Analyzer"
    description: str = "Analyzes datasets to provide statistical summaries, missing value reports, and data quality insights."

    def _run(self, dataset_path: str = None, dataset_summary: str = None) -> str:
        """Analyze a dataset and return comprehensive statistics."""
        try:
            # Try to load actual data if path is provided and exists
            if dataset_path and os.path.exists(dataset_path):
                try:
                    df = pd.read_csv(dataset_path)
                    
                    # Basic analysis
                    analysis = {
                        "dataset_source": dataset_path,
                        "dataset_shape": str(df.shape),
                        "columns": list(df.columns),
                        "missing_values": df.isnull().sum().to_dict(),
                        "data_types": {col: str(dtype) for col, dtype in df.dtypes.items()},
                        "numerical_stats": df.describe().to_dict(),
                        "recommendations": [
                            "Check missing value patterns",
                            "Inspect categorical variable cardinality",
                            "Visualize distributions of numerical columns"
                        ]
                    }
                    return json.dumps(analysis, indent=2, default=str)
                except Exception as e:
                     return json.dumps({"error": f"Failed to load CSV: {str(e)}", "path": dataset_path}, indent=2)

            # Template fallback if no file
            analysis = {
                "dataset_shape": "Unknown (provide valid csv path)",
                "missing_values": "Analysis requires actual dataset",
                "feature_types": "Analysis requires actual dataset",
                "class_distribution": "Analysis requires actual dataset",
                "correlations": "Analysis requires actual dataset",
                "recommendations": [
                    "Load actual dataset for detailed analysis",
                    "Check for missing values and outliers",
                    "Examine feature distributions",
                    "Assess class balance for classification tasks"
                ]
            }

            return json.dumps(analysis, indent=2)

        except Exception as e:
            return f"Error analyzing dataset: {str(e)}"


class ModelEvaluatorTool(BaseTool):
    """Tool for evaluating Random Forest model performance."""

    name: str = "Model Evaluator"
    description: str = "Evaluates Random Forest model performance with comprehensive metrics and analysis."

    def _run(self, model_metrics: str = None, evaluation_type: str = "classification") -> str:
        """Evaluate model performance based on provided metrics."""
        try:
            # Template evaluation response
            evaluation = {
                "evaluation_type": evaluation_type,
                "metrics_summary": "Analysis requires actual model results",
                "performance_analysis": "Provide actual model predictions and true values",
                "recommendations": [
                    "Compare with baseline models",
                    "Analyze confusion matrix patterns",
                    "Check for overfitting indicators",
                    "Consider cross-validation stability"
                ]
            }

            return json.dumps(evaluation, indent=2)

        except Exception as e:
            return f"Error evaluating model: {str(e)}"


class FeatureImportanceTool(BaseTool):
    """Tool for analyzing feature importance in Random Forest models."""

    name: str = "Feature Importance Analyzer"
    description: str = "Analyzes feature importance rankings and provides engineering recommendations."

    def _run(self, feature_importance_data: str = None) -> str:
        """Analyze feature importance and provide recommendations."""
        try:
            # Template feature importance analysis
            analysis = {
                "top_features": "Analysis requires actual feature importance data",
                "redundant_features": "Identify features with very low importance",
                "engineering_opportunities": [
                    "Consider feature interactions",
                    "Evaluate categorical encoding strategies",
                    "Assess feature scaling impact",
                    "Look for domain-specific feature engineering"
                ],
                "selection_recommendations": [
                    "Remove features with importance < 0.01",
                    "Consider recursive feature elimination",
                    "Evaluate feature correlation matrix"
                ]
            }

            return json.dumps(analysis, indent=2)

        except Exception as e:
            return f"Error analyzing feature importance: {str(e)}"


class HyperparameterOptimizerTool(BaseTool):
    """Tool for hyperparameter optimization recommendations."""

    name: str = "Hyperparameter Optimizer"
    description: str = "Provides hyperparameter optimization strategies and recommendations for Random Forest models."

    def _run(self, current_params: str = None, performance_metrics: str = None) -> str:
        """Provide hyperparameter optimization recommendations."""
        try:
            # Template hyperparameter recommendations
            recommendations = {
                "parameter_ranges": {
                    "n_estimators": "100-500 (start with 100, increase if needed)",
                    "max_depth": "10-30 (None for unlimited, but risk of overfitting)",
                    "min_samples_split": "2-10 (higher values reduce overfitting)",
                    "min_samples_leaf": "1-5 (higher values reduce overfitting)",
                    "max_features": "'sqrt' for classification, '1/3' for regression"
                },
                "optimization_strategy": [
                    "Use RandomizedSearchCV for initial exploration",
                    "Follow with GridSearchCV on promising regions",
                    "Consider Bayesian optimization for efficiency",
                    "Always use cross-validation (5-fold minimum)"
                ],
                "performance_targets": {
                    "accuracy_improvement": "2-5% expected with optimization",
                    "overfitting_reduction": "Monitor train/test performance gap",
                    "computation_tradeoffs": "More trees = better performance but slower"
                }
            }

            return json.dumps(recommendations, indent=2)

        except Exception as e:
            return f"Error providing hyperparameter recommendations: {str(e)}"
