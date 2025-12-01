#!/usr/bin/env python3
"""
NASA Task Load Index (TLX) Assessment Tool
Interactive command-line interface for psychometric assessments.
"""

import sys
from nasa_tlx import NASATLX, TLXResult


def print_header(text: str):
    """Print formatted header."""
    print("\n" + "=" * 60)
    print(text)
    print("=" * 60 + "\n")


def get_rating(prompt: str, dimension: str) -> int:
    """Get rating from user (1-20)."""
    description = NASATLX.DIMENSION_DESCRIPTIONS[dimension]
    print(f"\n{prompt}")
    print(f"Description: {description}")
    print("Scale: 1 (Very Low) to 20 (Very High)")
    
    while True:
        try:
            value = int(input("Rating (1-20): ").strip())
            if 1 <= value <= 20:
                return value
            else:
                print("Please enter a value between 1 and 20.")
        except ValueError:
            print("Please enter a valid number.")
        except KeyboardInterrupt:
            print("\n\nAssessment cancelled.")
            sys.exit(0)


def collect_ratings(tlx: NASATLX, task_name: str) -> TLXResult:
    """Collect TLX ratings from user."""
    result = tlx.create_assessment(task_name)
    
    print_header("NASA TLX Rating Collection")
    print("Please rate each dimension on a scale of 1-20.\n")
    
    mental = get_rating("1. Mental Demand", 'mental_demand')
    physical = get_rating("2. Physical Demand", 'physical_demand')
    temporal = get_rating("3. Temporal Demand", 'temporal_demand')
    performance = get_rating("4. Performance", 'performance')
    effort = get_rating("5. Effort", 'effort')
    frustration = get_rating("6. Frustration", 'frustration')
    
    tlx.add_rating(
        result,
        mental_demand=mental,
        physical_demand=physical,
        temporal_demand=temporal,
        performance=performance,
        effort=effort,
        frustration=frustration
    )
    
    return result


def collect_pairwise_comparisons(tlx: NASATLX, result: TLXResult) -> TLXResult:
    """Collect pairwise comparisons (optional)."""
    print_header("Pairwise Comparison (Optional)")
    print("Compare dimensions. Enter 0 to skip, -3 to +3 for preference.")
    print("Positive = first dimension more important, negative = second more important")
    print("Magnitude indicates strength (1=slight, 2=moderate, 3=strong)\n")
    
    comparisons = {}
    pairs = [
        ('mental_demand', 'physical_demand', 'mental_vs_physical'),
        ('mental_demand', 'temporal_demand', 'mental_vs_temporal'),
        ('mental_demand', 'performance', 'mental_vs_performance'),
        ('mental_demand', 'effort', 'mental_vs_effort'),
        ('mental_demand', 'frustration', 'mental_vs_frustration'),
        ('physical_demand', 'temporal_demand', 'physical_vs_temporal'),
        ('physical_demand', 'performance', 'physical_vs_performance'),
        ('physical_demand', 'effort', 'physical_vs_effort'),
        ('physical_demand', 'frustration', 'physical_vs_frustration'),
        ('temporal_demand', 'performance', 'temporal_vs_performance'),
        ('temporal_demand', 'effort', 'temporal_vs_effort'),
        ('temporal_demand', 'frustration', 'temporal_vs_frustration'),
        ('performance', 'effort', 'performance_vs_effort'),
        ('performance', 'frustration', 'performance_vs_frustration'),
        ('effort', 'frustration', 'effort_vs_frustration'),
    ]
    
    for dim1, dim2, key in pairs:
        while True:
            try:
                prompt = f"{dim1.replace('_', ' ').title()} vs {dim2.replace('_', ' ').title()} (-3 to +3, 0 to skip): "
                value = input(prompt).strip()
                if value == '' or value == '0':
                    comparisons[key] = 0
                    break
                value = int(value)
                if -3 <= value <= 3:
                    comparisons[key] = value
                    break
                else:
                    print("Please enter a value between -3 and +3.")
            except ValueError:
                print("Please enter a valid number.")
            except KeyboardInterrupt:
                print("\n\nAssessment cancelled.")
                sys.exit(0)
    
    tlx.add_pairwise_comparison(result, **comparisons)
    return result


def display_results(result: TLXResult):
    """Display assessment results."""
    print_header("Assessment Results")
    
    print(f"Task: {result.task_name}")
    if result.participant_id:
        print(f"Participant: {result.participant_id}")
    print(f"Timestamp: {result.timestamp}\n")
    
    if result.rating:
        print("Ratings:")
        rating_dict = result.rating.to_dict()
        for dim, value in rating_dict.items():
            print(f"  {dim.replace('_', ' ').title()}: {value}/20")
        print()
    
    if result.raw_tlx_score:
        print(f"Raw TLX Score: {result.raw_tlx_score:.2f}/20")
        print(f"  (Unweighted average of all dimensions)\n")
    
    if result.weighted_tlx_score:
        print(f"Weighted TLX Score: {result.weighted_tlx_score:.2f}/20")
        print(f"  (Weighted average based on pairwise comparisons)\n")
        
        if result.weights:
            print("Dimension Weights:")
            for dim, weight in result.weights.items():
                print(f"  {dim.replace('_', ' ').title()}: {weight:.3f}")
            print()
        
        if result.dimension_scores:
            print("Weighted Dimension Scores:")
            for dim, score in result.dimension_scores.items():
                print(f"  {dim.replace('_', ' ').title()}: {score:.2f}")
            print()


def main():
    """Main entry point."""
    print_header("NASA Task Load Index (TLX) Assessment Tool")
    
    tlx = NASATLX()
    
    # Get task information
    task_name = input("Enter task name: ").strip()
    if not task_name:
        task_name = "Unnamed Task"
    
    participant_id = input("Enter participant ID (optional): ").strip()
    if not participant_id:
        participant_id = None
    
    # Collect ratings
    result = collect_ratings(tlx, task_name)
    if participant_id:
        result.participant_id = participant_id
    
    # Ask about pairwise comparisons
    print("\n" + "-" * 60)
    do_pairwise = input("Perform pairwise comparisons? (y/n): ").strip().lower()
    
    if do_pairwise == 'y':
        result = collect_pairwise_comparisons(tlx, result)
    
    # Calculate scores
    tlx.calculate_scores(result)
    
    # Display results
    display_results(result)
    
    # Save result
    save = input("\nSave this assessment? (y/n): ").strip().lower()
    if save == 'y':
        tlx.save_result(result)
        print("Assessment saved!")
        
        # Show statistics if multiple results
        if len(tlx.results) > 1:
            stats = tlx.get_statistics(task_name)
            if stats:
                print_header("Statistics for this task")
                if stats['raw_tlx']['mean']:
                    print(f"Raw TLX - Mean: {stats['raw_tlx']['mean']:.2f}, "
                          f"StdDev: {stats['raw_tlx']['stdev']:.2f if stats['raw_tlx']['stdev'] else 'N/A'}")
                if stats['weighted_tlx']['mean']:
                    print(f"Weighted TLX - Mean: {stats['weighted_tlx']['mean']:.2f}, "
                          f"StdDev: {stats['weighted_tlx']['stdev']:.2f if stats['weighted_tlx']['stdev'] else 'N/A'}")
    
    # Export option
    export = input("\nExport results to JSON? (y/n): ").strip().lower()
    if export == 'y':
        filename = f"tlx_{task_name.replace(' ', '_')}_{result.timestamp[:10]}.json"
        with open(filename, 'w') as f:
            f.write(result.to_json())
        print(f"Results exported to {filename}")
    
    print("\n✅ Assessment complete!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nAssessment cancelled.")
        sys.exit(0)

