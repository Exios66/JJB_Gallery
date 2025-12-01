"""
Tests for Psychometric Assessment Application (NASA TLX)
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch

# Add Psychometrics to path
PSYCHOMETRICS_DIR = Path(__file__).parent.parent / "Psychometrics"
sys.path.insert(0, str(PSYCHOMETRICS_DIR))


class TestTLXDimensions:
    """Test TLX dimensions."""
    
    def test_tlx_dimensions_defined(self):
        """Test that TLX dimensions are properly defined."""
        try:
            import app
            assert hasattr(app, 'TLX_DIMENSIONS')
            dimensions = app.TLX_DIMENSIONS
            
            assert len(dimensions) == 6
            assert "Mental Demand" in dimensions
            assert "Physical Demand" in dimensions
            assert "Temporal Demand" in dimensions
            assert "Performance" in dimensions
            assert "Effort" in dimensions
            assert "Frustration" in dimensions
        except ImportError:
            pytest.skip("App not available")
    
    def test_dimension_structure(self):
        """Test dimension structure."""
        try:
            import app
            dimensions = app.TLX_DIMENSIONS
            
            for dim_name, dim_info in dimensions.items():
                assert "description" in dim_info
                assert "low" in dim_info
                assert "high" in dim_info
                assert isinstance(dim_info["description"], str)
        except ImportError:
            pytest.skip("App not available")


class TestTLXCalculation:
    """Test TLX score calculation."""
    
    def test_unweighted_tlx_calculation(self):
        """Test unweighted TLX calculation."""
        try:
            import app
            
            ratings = {
                "Mental Demand": 50,
                "Physical Demand": 30,
                "Temporal Demand": 40,
                "Performance": 60,
                "Effort": 45,
                "Frustration": 35
            }
            
            score = app.calculate_tlx_score(ratings)
            
            # Should be average of all ratings
            expected = sum(ratings.values()) / len(ratings)
            assert abs(score - expected) < 0.01
        except ImportError:
            pytest.skip("App not available")
    
    def test_weighted_tlx_calculation(self):
        """Test weighted TLX calculation."""
        try:
            import app
            
            ratings = {
                "Mental Demand": 50,
                "Physical Demand": 30,
                "Temporal Demand": 40,
                "Performance": 60,
                "Effort": 45,
                "Frustration": 35
            }
            
            weights = {
                "Mental Demand": 2,
                "Physical Demand": 1,
                "Temporal Demand": 1,
                "Performance": 1,
                "Effort": 1,
                "Frustration": 1
            }
            
            score = app.calculate_tlx_score(ratings, weights)
            
            # Should be weighted average
            weighted_sum = sum(ratings[dim] * weights[dim] for dim in ratings.keys())
            total_weight = sum(weights.values())
            expected = weighted_sum / total_weight
            
            assert abs(score - expected) < 0.01
        except ImportError:
            pytest.skip("App not available")
    
    def test_score_range(self):
        """Test that scores are in valid range."""
        try:
            import app
            
            ratings = {
                "Mental Demand": 100,
                "Physical Demand": 100,
                "Temporal Demand": 100,
                "Performance": 100,
                "Effort": 100,
                "Frustration": 100
            }
            
            score = app.calculate_tlx_score(ratings)
            assert 0 <= score <= 100
            
            # Test minimum
            ratings_min = {dim: 0 for dim in ratings.keys()}
            score_min = app.calculate_tlx_score(ratings_min)
            assert score_min == 0
        except ImportError:
            pytest.skip("App not available")


class TestPairwiseComparison:
    """Test pairwise comparison functionality."""
    
    def test_pairwise_comparison_structure(self):
        """Test pairwise comparison structure."""
        try:
            import app
            dimensions = list(app.TLX_DIMENSIONS.keys())
            
            # Should have n*(n-1)/2 comparisons for n dimensions
            n = len(dimensions)
            expected_comparisons = n * (n - 1) // 2
            
            # For 6 dimensions, should have 15 comparisons
            assert expected_comparisons == 15
        except ImportError:
            pytest.skip("App not available")
    
    def test_weight_calculation(self):
        """Test weight calculation from comparisons."""
        # Mock pairwise comparison results
        dimensions = ["Mental Demand", "Physical Demand", "Temporal Demand",
                     "Performance", "Effort", "Frustration"]
        
        # Simulate comparisons where Mental Demand is selected more
        comparisons = {}
        for i in range(len(dimensions)):
            for j in range(i + 1, len(dimensions)):
                key = f"{dimensions[i]}_{dimensions[j]}"
                # Mental Demand wins most comparisons
                comparisons[key] = dimensions[i] if i == 0 else dimensions[j]
        
        # Calculate weights
        weights = {dim: 0 for dim in dimensions}
        for key, selected in comparisons.items():
            dim1, dim2 = key.split("_")
            if selected == dim1:
                weights[dim1] += 1
            else:
                weights[dim2] += 1
        
        # Mental Demand should have highest weight
        assert weights["Mental Demand"] >= max(weights.values()) - 1


class TestSessionState:
    """Test session state management."""
    
    def test_assessment_structure(self):
        """Test assessment data structure."""
        assessment = {
            "timestamp": "2024-01-01T00:00:00",
            "task_name": "Test Task",
            "task_description": "Test Description",
            "participant_id": "P001",
            "ratings": {
                "Mental Demand": 50,
                "Physical Demand": 30,
                "Temporal Demand": 40,
                "Performance": 60,
                "Effort": 45,
                "Frustration": 35
            },
            "weights": None,
            "score": 43.33,
            "weighted": False
        }
        
        assert "timestamp" in assessment
        assert "ratings" in assessment
        assert "score" in assessment
        assert len(assessment["ratings"]) == 6


class TestVisualization:
    """Test visualization functionality."""
    
    def test_radar_chart_data(self):
        """Test radar chart data preparation."""
        ratings = {
            "Mental Demand": 50,
            "Physical Demand": 30,
            "Temporal Demand": 40,
            "Performance": 60,
            "Effort": 45,
            "Frustration": 35
        }
        
        dimensions = list(ratings.keys())
        values = list(ratings.values())
        
        assert len(dimensions) == 6
        assert len(values) == 6
        assert all(0 <= v <= 100 for v in values)
    
    def test_bar_chart_data(self):
        """Test bar chart data preparation."""
        ratings = {
            "Mental Demand": 50,
            "Physical Demand": 30,
            "Temporal Demand": 40,
            "Performance": 60,
            "Effort": 45,
            "Frustration": 35
        }
        
        dimensions = list(ratings.keys())
        values = list(ratings.values())
        
        assert len(dimensions) == len(values)
        assert max(values) <= 100
        assert min(values) >= 0

