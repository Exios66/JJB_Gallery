"""
Psychometric Assessment Application
NASA Task Load Index (TLX) Assessment Tool
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from typing import Dict, List, Optional
import json

# Page configuration
st.set_page_config(
    page_title="NASA TLX Assessment",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    .score-display {
        font-size: 2.5rem;
        font-weight: bold;
        color: #667eea;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# NASA TLX Dimensions
TLX_DIMENSIONS = {
    "Mental Demand": {
        "description": "How much mental and perceptual activity was required?",
        "low": "Very Low",
        "high": "Very High"
    },
    "Physical Demand": {
        "description": "How much physical activity was required?",
        "low": "Very Low",
        "high": "Very High"
    },
    "Temporal Demand": {
        "description": "How much time pressure did you feel?",
        "low": "Very Low",
        "high": "Very High"
    },
    "Performance": {
        "description": "How successful were you in accomplishing the task?",
        "low": "Perfect",
        "high": "Failure"
    },
    "Effort": {
        "description": "How hard did you have to work to accomplish your level of performance?",
        "low": "Very Low",
        "high": "Very High"
    },
    "Frustration": {
        "description": "How insecure, discouraged, irritated, stressed, and annoyed were you?",
        "low": "Very Low",
        "high": "Very High"
    }
}

# Initialize session state
if "assessments" not in st.session_state:
    st.session_state.assessments = []
if "current_assessment" not in st.session_state:
    st.session_state.current_assessment = {}
if "pairwise_comparisons" not in st.session_state:
    st.session_state.pairwise_comparisons = {}

def calculate_tlx_score(ratings: Dict[str, int], weights: Optional[Dict[str, int]] = None) -> float:
    """Calculate NASA TLX score from ratings and optional weights."""
    if weights:
        # Weighted TLX
        weighted_sum = sum(ratings[dim] * weights.get(dim, 1) for dim in TLX_DIMENSIONS.keys())
        total_weight = sum(weights.get(dim, 1) for dim in TLX_DIMENSIONS.keys())
        return weighted_sum / total_weight if total_weight > 0 else 0
    else:
        # Unweighted TLX (simple average)
        return sum(ratings.values()) / len(ratings)

def pairwise_comparison():
    """Perform pairwise comparison for weighted TLX."""
    dimensions = list(TLX_DIMENSIONS.keys())
    comparisons = {}
    
    st.subheader("Pairwise Comparison (Optional)")
    st.info("For each pair, select which dimension contributed more to workload.")
    
    comparison_count = 0
    for i in range(len(dimensions)):
        for j in range(i + 1, len(dimensions)):
            dim1, dim2 = dimensions[i], dimensions[j]
            key = f"{dim1}_{dim2}"
            
            selected = st.radio(
                f"Which contributed more: {dim1} or {dim2}?",
                [dim1, dim2],
                key=key,
                horizontal=True
            )
            comparisons[key] = selected
            comparison_count += 1
    
    # Calculate weights from comparisons
    weights = {dim: 0 for dim in dimensions}
    for key, selected in comparisons.items():
        dim1, dim2 = key.split("_")
        if selected == dim1:
            weights[dim1] += 1
        else:
            weights[dim2] += 1
    
    return weights

def main():
    st.markdown('<div class="main-header"><h1>🚀 NASA Task Load Index (TLX) Assessment</h1></div>', unsafe_allow_html=True)
    
    # Sidebar navigation
    page = st.sidebar.selectbox(
        "Navigation",
        ["New Assessment", "View Results", "Historical Data"]
    )
    
    if page == "New Assessment":
        new_assessment()
    elif page == "View Results":
        view_results()
    else:
        historical_data()

def new_assessment():
    """Create a new TLX assessment."""
    st.header("New Assessment")
    
    # Task information
    with st.expander("Task Information", expanded=True):
        task_name = st.text_input("Task Name", value="Task Assessment")
        task_description = st.text_area("Task Description", height=100)
        participant_id = st.text_input("Participant ID (optional)")
    
    # Rating scales
    st.header("Rating Scales")
    st.info("Rate each dimension on a scale from 0 to 100, where 0 = Low and 100 = High")
    
    ratings = {}
    
    for dimension, info in TLX_DIMENSIONS.items():
        st.subheader(dimension)
        st.caption(info["description"])
        
        rating = st.slider(
            f"{info['low']} (0) ← → {info['high']} (100)",
            min_value=0,
            max_value=100,
            value=50,
            key=f"rating_{dimension}",
            step=5
        )
        ratings[dimension] = rating
        
        # Visual indicator
        col1, col2, col3 = st.columns([1, 4, 1])
        with col2:
            st.progress(rating / 100)
    
    # Optional pairwise comparison
    use_weighted = st.checkbox("Use Weighted TLX (Pairwise Comparison)", value=False)
    weights = None
    
    if use_weighted:
        weights = pairwise_comparison()
        st.subheader("Dimension Weights")
        weights_df = pd.DataFrame(list(weights.items()), columns=["Dimension", "Weight"])
        st.dataframe(weights_df, use_container_width=True)
    
    # Calculate and display score
    if st.button("Calculate TLX Score", type="primary"):
        score = calculate_tlx_score(ratings, weights)
        
        # Save assessment
        assessment = {
            "timestamp": datetime.now().isoformat(),
            "task_name": task_name,
            "task_description": task_description,
            "participant_id": participant_id,
            "ratings": ratings,
            "weights": weights,
            "score": score,
            "weighted": use_weighted
        }
        
        st.session_state.assessments.append(assessment)
        
        # Display results
        st.success("Assessment saved!")
        display_score(score, ratings, weights)
        
        # Visualization
        visualize_assessment(ratings, weights)

def display_score(score: float, ratings: Dict[str, int], weights: Optional[Dict[str, int]]):
    """Display the calculated TLX score."""
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="score-display">{score:.1f}</div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem;">NASA TLX Score</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Interpretation
    if score < 30:
        interpretation = "Low Workload"
        color = "green"
    elif score < 50:
        interpretation = "Moderate Workload"
        color = "orange"
    elif score < 70:
        interpretation = "High Workload"
        color = "red"
    else:
        interpretation = "Very High Workload"
        color = "darkred"
    
    st.markdown(f'<p style="text-align: center; color: {color}; font-weight: bold;">{interpretation}</p>', unsafe_allow_html=True)

def visualize_assessment(ratings: Dict[str, int], weights: Optional[Dict[str, int]]):
    """Create visualizations for the assessment."""
    # Radar chart
    fig = go.Figure()
    
    dimensions = list(ratings.keys())
    values = list(ratings.values())
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=dimensions,
        fill='toself',
        name='Workload',
        line_color='rgb(102, 126, 234)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True,
        title="NASA TLX Radar Chart"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Bar chart
    fig2 = px.bar(
        x=dimensions,
        y=values,
        labels={'x': 'Dimension', 'y': 'Rating'},
        title="Dimension Ratings",
        color=values,
        color_continuous_scale="Viridis"
    )
    st.plotly_chart(fig2, use_container_width=True)

def view_results():
    """View assessment results."""
    st.header("Assessment Results")
    
    if not st.session_state.assessments:
        st.info("No assessments yet. Create a new assessment to see results.")
        return
    
    # Latest assessment
    latest = st.session_state.assessments[-1]
    
    st.subheader("Latest Assessment")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Task", latest["task_name"])
    with col2:
        st.metric("TLX Score", f"{latest['score']:.1f}")
    with col3:
        st.metric("Type", "Weighted" if latest["weighted"] else "Unweighted")
    
    display_score(latest["score"], latest["ratings"], latest.get("weights"))
    visualize_assessment(latest["ratings"], latest.get("weights"))

def historical_data():
    """View historical assessment data."""
    st.header("Historical Data")
    
    if not st.session_state.assessments:
        st.info("No historical data available.")
        return
    
    # Create DataFrame
    data = []
    for assessment in st.session_state.assessments:
        row = {
            "Timestamp": assessment["timestamp"],
            "Task": assessment["task_name"],
            "TLX Score": assessment["score"],
            "Type": "Weighted" if assessment["weighted"] else "Unweighted"
        }
        row.update(assessment["ratings"])
        data.append(row)
    
    df = pd.DataFrame(data)
    
    # Display table
    st.dataframe(df, use_container_width=True)
    
    # Trend chart
    if len(df) > 1:
        fig = px.line(
            df,
            x="Timestamp",
            y="TLX Score",
            title="TLX Score Over Time",
            markers=True
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Export option
    if st.button("Export to CSV"):
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"tlx_assessments_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()

