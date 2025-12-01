"""
NASA Task Load Index (TLX) Assessment Tool
Implements the NASA TLX psychometric assessment for measuring workload.
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import json
import statistics


@dataclass
class TLXRating:
    """Individual TLX rating for a task."""
    mental_demand: int  # 1-20
    physical_demand: int  # 1-20
    temporal_demand: int  # 1-20
    performance: int  # 1-20 (inverted: 1=perfect, 20=failure)
    effort: int  # 1-20
    frustration: int  # 1-20
    
    def validate(self) -> bool:
        """Validate that all ratings are in valid range."""
        ratings = [
            self.mental_demand, self.physical_demand, self.temporal_demand,
            self.performance, self.effort, self.frustration
        ]
        return all(1 <= r <= 20 for r in ratings)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'mental_demand': self.mental_demand,
            'physical_demand': self.physical_demand,
            'temporal_demand': self.temporal_demand,
            'performance': self.performance,
            'effort': self.effort,
            'frustration': self.frustration
        }


@dataclass
class TLXPairwiseComparison:
    """Pairwise comparison weights for TLX dimensions."""
    mental_vs_physical: int  # -3 to +3
    mental_vs_temporal: int
    mental_vs_performance: int
    mental_vs_effort: int
    mental_vs_frustration: int
    physical_vs_temporal: int
    physical_vs_performance: int
    physical_vs_effort: int
    physical_vs_frustration: int
    temporal_vs_performance: int
    temporal_vs_effort: int
    temporal_vs_frustration: int
    performance_vs_effort: int
    performance_vs_frustration: int
    effort_vs_frustration: int
    
    def validate(self) -> bool:
        """Validate that all comparisons are in valid range."""
        comparisons = [
            self.mental_vs_physical, self.mental_vs_temporal,
            self.mental_vs_performance, self.mental_vs_effort,
            self.mental_vs_frustration, self.physical_vs_temporal,
            self.physical_vs_performance, self.physical_vs_effort,
            self.physical_vs_frustration, self.temporal_vs_performance,
            self.temporal_vs_effort, self.temporal_vs_frustration,
            self.performance_vs_effort, self.performance_vs_frustration,
            self.effort_vs_frustration
        ]
        return all(-3 <= c <= 3 for c in comparisons)
    
    def calculate_weights(self) -> Dict[str, float]:
        """Calculate dimension weights from pairwise comparisons."""
        dimensions = [
            'mental_demand', 'physical_demand', 'temporal_demand',
            'performance', 'effort', 'frustration'
        ]
        
        # Count wins for each dimension
        wins = {dim: 0 for dim in dimensions}
        
        # Mental demand comparisons
        if self.mental_vs_physical > 0:
            wins['mental_demand'] += abs(self.mental_vs_physical)
        else:
            wins['physical_demand'] += abs(self.mental_vs_physical)
        
        if self.mental_vs_temporal > 0:
            wins['mental_demand'] += abs(self.mental_vs_temporal)
        else:
            wins['temporal_demand'] += abs(self.mental_vs_temporal)
        
        if self.mental_vs_performance > 0:
            wins['mental_demand'] += abs(self.mental_vs_performance)
        else:
            wins['performance'] += abs(self.mental_vs_performance)
        
        if self.mental_vs_effort > 0:
            wins['mental_demand'] += abs(self.mental_vs_effort)
        else:
            wins['effort'] += abs(self.mental_vs_effort)
        
        if self.mental_vs_frustration > 0:
            wins['mental_demand'] += abs(self.mental_vs_frustration)
        else:
            wins['frustration'] += abs(self.mental_vs_frustration)
        
        # Physical demand comparisons
        if self.physical_vs_temporal > 0:
            wins['physical_demand'] += abs(self.physical_vs_temporal)
        else:
            wins['temporal_demand'] += abs(self.physical_vs_temporal)
        
        if self.physical_vs_performance > 0:
            wins['physical_demand'] += abs(self.physical_vs_performance)
        else:
            wins['performance'] += abs(self.physical_vs_performance)
        
        if self.physical_vs_effort > 0:
            wins['physical_demand'] += abs(self.physical_vs_effort)
        else:
            wins['effort'] += abs(self.physical_vs_effort)
        
        if self.physical_vs_frustration > 0:
            wins['physical_demand'] += abs(self.physical_vs_frustration)
        else:
            wins['frustration'] += abs(self.physical_vs_frustration)
        
        # Temporal demand comparisons
        if self.temporal_vs_performance > 0:
            wins['temporal_demand'] += abs(self.temporal_vs_performance)
        else:
            wins['performance'] += abs(self.temporal_vs_performance)
        
        if self.temporal_vs_effort > 0:
            wins['temporal_demand'] += abs(self.temporal_vs_effort)
        else:
            wins['effort'] += abs(self.temporal_vs_effort)
        
        if self.temporal_vs_frustration > 0:
            wins['temporal_demand'] += abs(self.temporal_vs_frustration)
        else:
            wins['frustration'] += abs(self.temporal_vs_frustration)
        
        # Performance comparisons
        if self.performance_vs_effort > 0:
            wins['performance'] += abs(self.performance_vs_effort)
        else:
            wins['effort'] += abs(self.performance_vs_effort)
        
        if self.performance_vs_frustration > 0:
            wins['performance'] += abs(self.performance_vs_frustration)
        else:
            wins['frustration'] += abs(self.performance_vs_frustration)
        
        # Effort vs frustration
        if self.effort_vs_frustration > 0:
            wins['effort'] += abs(self.effort_vs_frustration)
        else:
            wins['frustration'] += abs(self.effort_vs_frustration)
        
        # Normalize to weights (0-1)
        total_wins = sum(wins.values())
        if total_wins == 0:
            # Equal weights if no comparisons
            return {dim: 1/6 for dim in dimensions}
        
        return {dim: wins[dim] / total_wins for dim in dimensions}


@dataclass
class TLXResult:
    """Complete TLX assessment result."""
    task_name: str
    participant_id: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    rating: Optional[TLXRating] = None
    pairwise_comparison: Optional[TLXPairwiseComparison] = None
    raw_tlx_score: Optional[float] = None
    weighted_tlx_score: Optional[float] = None
    dimension_scores: Dict[str, float] = field(default_factory=dict)
    weights: Dict[str, float] = field(default_factory=dict)
    
    def calculate_raw_tlx(self) -> float:
        """Calculate raw TLX score (unweighted average)."""
        if not self.rating:
            raise ValueError("Rating required for raw TLX calculation")
        
        if not self.rating.validate():
            raise ValueError("Invalid rating values")
        
        scores = [
            self.rating.mental_demand,
            self.rating.physical_demand,
            self.rating.temporal_demand,
            self.rating.performance,
            self.rating.effort,
            self.rating.frustration
        ]
        
        self.raw_tlx_score = statistics.mean(scores)
        return self.raw_tlx_score
    
    def calculate_weighted_tlx(self) -> float:
        """Calculate weighted TLX score."""
        if not self.rating:
            raise ValueError("Rating required for weighted TLX calculation")
        
        if not self.rating.validate():
            raise ValueError("Invalid rating values")
        
        if not self.pairwise_comparison:
            raise ValueError("Pairwise comparison required for weighted TLX")
        
        if not self.pairwise_comparison.validate():
            raise ValueError("Invalid pairwise comparison values")
        
        # Calculate weights
        self.weights = self.pairwise_comparison.calculate_weights()
        
        # Calculate weighted score
        rating_dict = self.rating.to_dict()
        weighted_sum = sum(
            self.weights[dim] * rating_dict[dim]
            for dim in self.weights.keys()
        )
        
        self.weighted_tlx_score = weighted_sum
        
        # Store dimension scores
        self.dimension_scores = {
            dim: self.weights[dim] * rating_dict[dim]
            for dim in self.weights.keys()
        }
        
        return self.weighted_tlx_score
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        result = {
            'task_name': self.task_name,
            'participant_id': self.participant_id,
            'timestamp': self.timestamp,
            'raw_tlx_score': self.raw_tlx_score,
            'weighted_tlx_score': self.weighted_tlx_score,
            'dimension_scores': self.dimension_scores,
            'weights': self.weights
        }
        
        if self.rating:
            result['rating'] = self.rating.to_dict()
        
        return result
    
    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=2)


class NASATLX:
    """NASA Task Load Index assessment system."""
    
    DIMENSIONS = [
        'mental_demand', 'physical_demand', 'temporal_demand',
        'performance', 'effort', 'frustration'
    ]
    
    DIMENSION_DESCRIPTIONS = {
        'mental_demand': 'How mentally demanding was the task?',
        'physical_demand': 'How physically demanding was the task?',
        'temporal_demand': 'How hurried or rushed was the pace of the task?',
        'performance': 'How successful were you in accomplishing the task?',
        'effort': 'How hard did you have to work to accomplish your level of performance?',
        'frustration': 'How insecure, discouraged, irritated, stressed, or annoyed were you?'
    }
    
    def __init__(self):
        """Initialize NASA TLX system."""
        self.results: List[TLXResult] = []
    
    def create_assessment(
        self,
        task_name: str,
        participant_id: Optional[str] = None
    ) -> TLXResult:
        """Create a new TLX assessment."""
        result = TLXResult(
            task_name=task_name,
            participant_id=participant_id
        )
        return result
    
    def add_rating(
        self,
        result: TLXResult,
        mental_demand: int,
        physical_demand: int,
        temporal_demand: int,
        performance: int,
        effort: int,
        frustration: int
    ) -> TLXResult:
        """Add rating to assessment."""
        rating = TLXRating(
            mental_demand=mental_demand,
            physical_demand=physical_demand,
            temporal_demand=temporal_demand,
            performance=performance,
            effort=effort,
            frustration=frustration
        )
        
        if not rating.validate():
            raise ValueError("All ratings must be between 1 and 20")
        
        result.rating = rating
        return result
    
    def add_pairwise_comparison(
        self,
        result: TLXResult,
        mental_vs_physical: int = 0,
        mental_vs_temporal: int = 0,
        mental_vs_performance: int = 0,
        mental_vs_effort: int = 0,
        mental_vs_frustration: int = 0,
        physical_vs_temporal: int = 0,
        physical_vs_performance: int = 0,
        physical_vs_effort: int = 0,
        physical_vs_frustration: int = 0,
        temporal_vs_performance: int = 0,
        temporal_vs_effort: int = 0,
        temporal_vs_frustration: int = 0,
        performance_vs_effort: int = 0,
        performance_vs_frustration: int = 0,
        effort_vs_frustration: int = 0
    ) -> TLXResult:
        """Add pairwise comparison to assessment."""
        comparison = TLXPairwiseComparison(
            mental_vs_physical=mental_vs_physical,
            mental_vs_temporal=mental_vs_temporal,
            mental_vs_performance=mental_vs_performance,
            mental_vs_effort=mental_vs_effort,
            mental_vs_frustration=mental_vs_frustration,
            physical_vs_temporal=physical_vs_temporal,
            physical_vs_performance=physical_vs_performance,
            physical_vs_effort=physical_vs_effort,
            physical_vs_frustration=physical_vs_frustration,
            temporal_vs_performance=temporal_vs_performance,
            temporal_vs_effort=temporal_vs_effort,
            temporal_vs_frustration=temporal_vs_frustration,
            performance_vs_effort=performance_vs_effort,
            performance_vs_frustration=performance_vs_frustration,
            effort_vs_frustration=effort_vs_frustration
        )
        
        if not comparison.validate():
            raise ValueError("All comparisons must be between -3 and +3")
        
        result.pairwise_comparison = comparison
        return result
    
    def calculate_scores(self, result: TLXResult) -> TLXResult:
        """Calculate both raw and weighted TLX scores."""
        if result.rating:
            result.calculate_raw_tlx()
        
        if result.rating and result.pairwise_comparison:
            result.calculate_weighted_tlx()
        
        return result
    
    def save_result(self, result: TLXResult):
        """Save assessment result."""
        self.results.append(result)
    
    def get_statistics(self, task_name: Optional[str] = None) -> Dict:
        """Get statistics for all results or specific task."""
        results = [
            r for r in self.results
            if task_name is None or r.task_name == task_name
        ]
        
        if not results:
            return {}
        
        raw_scores = [r.raw_tlx_score for r in results if r.raw_tlx_score]
        weighted_scores = [r.weighted_tlx_score for r in results if r.weighted_tlx_score]
        
        stats = {
            'count': len(results),
            'raw_tlx': {
                'mean': statistics.mean(raw_scores) if raw_scores else None,
                'median': statistics.median(raw_scores) if raw_scores else None,
                'stdev': statistics.stdev(raw_scores) if len(raw_scores) > 1 else None,
                'min': min(raw_scores) if raw_scores else None,
                'max': max(raw_scores) if raw_scores else None
            },
            'weighted_tlx': {
                'mean': statistics.mean(weighted_scores) if weighted_scores else None,
                'median': statistics.median(weighted_scores) if weighted_scores else None,
                'stdev': statistics.stdev(weighted_scores) if len(weighted_scores) > 1 else None,
                'min': min(weighted_scores) if weighted_scores else None,
                'max': max(weighted_scores) if weighted_scores else None
            }
        }
        
        return stats

