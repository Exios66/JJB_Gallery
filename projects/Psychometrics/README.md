# Psychometric Assessment Applications

A comprehensive psychometric assessment toolkit implementing the NASA Task Load Index (TLX) and related workload measurement tools.

## Overview

This project provides tools for conducting psychometric assessments, particularly focused on workload measurement using the NASA Task Load Index (TLX). The TLX is a widely-used tool for assessing the subjective workload experienced by users when performing tasks.

## Features

- **NASA TLX Implementation**: Complete implementation of the NASA Task Load Index
- **Raw TLX Scores**: Unweighted average of six workload dimensions
- **Weighted TLX Scores**: Weighted scores based on pairwise comparisons
- **Interactive CLI**: Command-line interface for data collection
- **Data Export**: JSON export for analysis
- **Statistical Analysis**: Aggregate statistics across multiple assessments

## NASA Task Load Index (TLX)

The NASA TLX measures workload across six dimensions:

1. **Mental Demand**: How mentally demanding was the task?
2. **Physical Demand**: How physically demanding was the task?
3. **Temporal Demand**: How hurried or rushed was the pace?
4. **Performance**: How successful were you in accomplishing the task?
5. **Effort**: How hard did you have to work?
6. **Frustration**: How insecure, discouraged, or annoyed were you?

Each dimension is rated on a scale of 1-20, where:

- 1 = Very Low
- 20 = Very High

(Note: Performance is inverted - 1 = Perfect, 20 = Failure)

## Installation

### Basic Installation

```bash
pip install -r requirements.txt
```

Note: The core functionality uses only Python standard library. Optional dependencies are for advanced analysis.

## Usage

### Command-Line Interface

Run the interactive assessment tool:

```bash
python main.py
```

The tool will guide you through:

1. Entering task and participant information
2. Rating each of the six dimensions (1-20)
3. Optional pairwise comparisons for weighted scores
4. Viewing results
5. Saving and exporting data

### Programmatic Usage

```python
from nasa_tlx import NASATLX

# Initialize system
tlx = NASATLX()

# Create assessment
result = tlx.create_assessment(
    task_name="User Interface Evaluation",
    participant_id="P001"
)

# Add ratings
tlx.add_rating(
    result,
    mental_demand=15,
    physical_demand=3,
    temporal_demand=12,
    performance=5,  # Inverted: lower is better
    effort=14,
    frustration=8
)

# Calculate raw TLX score
tlx.calculate_scores(result)
print(f"Raw TLX Score: {result.raw_tlx_score:.2f}")

# Add pairwise comparisons for weighted score
tlx.add_pairwise_comparison(
    result,
    mental_vs_physical=3,  # Mental much more important
    mental_vs_temporal=1,  # Mental slightly more important
    # ... other comparisons
)

# Calculate weighted TLX score
tlx.calculate_scores(result)
print(f"Weighted TLX Score: {result.weighted_tlx_score:.2f}")
print(f"Weights: {result.weights}")

# Save result
tlx.save_result(result)

# Get statistics
stats = tlx.get_statistics("User Interface Evaluation")
print(f"Mean Raw TLX: {stats['raw_tlx']['mean']:.2f}")
```

### Export Results

```python
# Export to JSON
json_output = result.to_json()
with open("assessment.json", "w") as f:
    f.write(json_output)

# Or export as dictionary
result_dict = result.to_dict()
```

## Scoring Methods

### Raw TLX Score

The raw TLX score is the unweighted average of all six dimension ratings:

```text
Raw TLX = (Mental + Physical + Temporal + Performance + Effort + Frustration) / 6
```

Range: 1-20

### Weighted TLX Score

The weighted TLX score uses pairwise comparisons to determine the relative importance of each dimension:

1. Compare each pair of dimensions (15 total comparisons)
2. Count "wins" for each dimension
3. Normalize to weights (0-1, sum to 1)
4. Calculate weighted average:

```text

Weighted TLX = Σ(Weight_i × Rating_i)
```

Range: 1-20

## Pairwise Comparisons

When collecting weighted TLX scores, participants compare each pair of dimensions:

- **+3**: First dimension much more important
- **+2**: First dimension moderately more important
- **+1**: First dimension slightly more important
- **0**: Equal importance (or skip)
- **-1**: Second dimension slightly more important
- **-2**: Second dimension moderately more important
- **-3**: Second dimension much more important

## Data Structure

### TLXResult

```python
{
    "task_name": "Task Name",
    "participant_id": "P001",
    "timestamp": "2024-01-15T10:30:00",
    "rating": {
        "mental_demand": 15,
        "physical_demand": 3,
        "temporal_demand": 12,
        "performance": 5,
        "effort": 14,
        "frustration": 8
    },
    "raw_tlx_score": 9.5,
    "weighted_tlx_score": 10.2,
    "dimension_scores": {
        "mental_demand": 2.5,
        "physical_demand": 0.3,
        ...
    },
    "weights": {
        "mental_demand": 0.25,
        "physical_demand": 0.10,
        ...
    }
}
```

## Statistical Analysis

Get aggregate statistics across multiple assessments:

```python
stats = tlx.get_statistics(task_name="User Interface Evaluation")

# Returns:
{
    "count": 10,
    "raw_tlx": {
        "mean": 9.5,
        "median": 9.2,
        "stdev": 1.8,
        "min": 7.0,
        "max": 12.5
    },
    "weighted_tlx": {
        "mean": 10.2,
        "median": 10.0,
        "stdev": 2.1,
        "min": 7.5,
        "max": 13.0
    }
}
```

## Use Cases

- **User Experience Research**: Measure workload in UI/UX studies
- **Human Factors Engineering**: Assess task difficulty and cognitive load
- **Product Testing**: Compare workload across different product versions
- **Training Evaluation**: Measure learning curve and task complexity
- **Ergonomic Assessment**: Evaluate physical and mental demands

## Interpretation Guidelines

### Raw TLX Scores

- **1-5**: Very Low workload
- **6-10**: Low to Moderate workload
- **11-15**: Moderate to High workload
- **16-20**: Very High workload

### Dimension Analysis

High scores in specific dimensions indicate:

- **Mental Demand**: Complex cognitive tasks
- **Physical Demand**: Physically strenuous tasks
- **Temporal Demand**: Time pressure or rushed pace
- **Performance**: Low success rate (inverted scale)
- **Effort**: High exertion required
- **Frustration**: Negative emotional response

## Best Practices

1. **Consistent Administration**: Use same instructions and scale for all participants
2. **Post-Task Rating**: Collect ratings immediately after task completion
3. **Clear Instructions**: Explain each dimension clearly
4. **Multiple Assessments**: Collect multiple data points for reliability
5. **Context Documentation**: Record task details and conditions

## References

- Hart, S. G., & Staveland, L. E. (1988). Development of NASA-TLX (Task Load Index): Results of empirical and theoretical research. *Advances in psychology*, 52, 139-183.
- [NASA TLX Official Documentation](https://humansystems.arc.nasa.gov/groups/tlx/)

## License

See main repository LICENSE file.

## Related Projects

This project is part of the [JJB Gallery](https://github.com/Exios66/JJB_Gallery) portfolio. Related projects include:

- [RAG Model](../RAG_Model/README.md) - Retrieval-Augmented Generation
- [CrewAI](../CrewAI/README.md) - Multi-Agent System
- [ChatUi](../ChatUi/README.md) - Modern Chat Interface

## Additional Resources

- 📚 [Project Wiki](https://github.com/Exios66/JJB_Gallery/wiki) - Comprehensive documentation
- 📖 [Psychometrics Wiki Page](https://github.com/Exios66/JJB_Gallery/wiki/Psychometrics) - Detailed project documentation
- 🔧 [Installation Guide](https://github.com/Exios66/JJB_Gallery/wiki/Installation-Guide) - Setup instructions
- 🐛 [Troubleshooting](https://github.com/Exios66/JJB_Gallery/wiki/Troubleshooting) - Common issues and solutions

## Contributing

Contributions welcome! Please see the main repository [Contributing Guidelines](https://github.com/Exios66/JJB_Gallery/wiki/Contributing-Guidelines).

For issues, questions, or suggestions, please use the [GitHub Issues](https://github.com/Exios66/JJB_Gallery/issues) page.
