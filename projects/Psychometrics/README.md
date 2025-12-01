# Psychometric Assessment Application

A comprehensive NASA Task Load Index (TLX) assessment tool built with Streamlit. This application allows researchers and practitioners to measure subjective mental workload using the NASA TLX methodology.

## 🚀 Features

- **NASA TLX Implementation**: Complete implementation of the NASA Task Load Index
- **Weighted & Unweighted TLX**: Support for both weighted and unweighted TLX calculations
- **Interactive Rating Scales**: Easy-to-use sliders for all 6 TLX dimensions
- **Pairwise Comparison**: Built-in pairwise comparison for weighted TLX
- **Visual Analytics**: Radar charts and bar charts for workload visualization
- **Historical Tracking**: Save and track multiple assessments over time
- **Data Export**: Export assessment data to CSV

## 📋 Prerequisites

- Python 3.8+
- Streamlit

## 🛠️ Installation

1. **Navigate to the project:**
   ```bash
   cd projects/Psychometrics
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Usage

### Start the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📊 NASA TLX Dimensions

The NASA TLX measures workload across 6 dimensions:

1. **Mental Demand**: How much mental and perceptual activity was required?
2. **Physical Demand**: How much physical activity was required?
3. **Temporal Demand**: How much time pressure did you feel?
4. **Performance**: How successful were you in accomplishing the task?
5. **Effort**: How hard did you have to work to accomplish your level of performance?
6. **Frustration**: How insecure, discouraged, irritated, stressed, and annoyed were you?

Each dimension is rated on a scale from 0 (Low) to 100 (High).

## 🎯 Using the Application

### Creating a New Assessment

1. **Task Information**: Enter task name, description, and optional participant ID
2. **Rate Dimensions**: Use sliders to rate each of the 6 TLX dimensions
3. **Optional Weighting**: Enable pairwise comparison for weighted TLX
4. **Calculate Score**: Click "Calculate TLX Score" to get results

### TLX Score Interpretation

- **< 30**: Low Workload
- **30-50**: Moderate Workload
- **50-70**: High Workload
- **> 70**: Very High Workload

### Viewing Results

- **Latest Assessment**: View the most recent assessment with visualizations
- **Historical Data**: Track multiple assessments over time
- **Export Data**: Download assessment data as CSV

## 📈 Visualizations

### Radar Chart

A radar chart showing workload across all 6 dimensions, providing a visual representation of the workload profile.

### Bar Chart

A bar chart showing individual dimension ratings with color coding.

### Trend Analysis

For multiple assessments, view trends over time to track workload changes.

## 🔬 Methodology

### Unweighted TLX

Simple average of all 6 dimension ratings:

```
TLX = (Mental + Physical + Temporal + Performance + Effort + Frustration) / 6
```

### Weighted TLX

Weighted average based on pairwise comparisons:

```
TLX = Σ(Rating_i × Weight_i) / Σ(Weight_i)
```

The pairwise comparison determines which dimensions contribute more to overall workload.

## 📦 Project Structure

```
Psychometrics/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## 🎨 Customization

### Adding Custom Dimensions

To add custom dimensions, modify the `TLX_DIMENSIONS` dictionary in `app.py`:

```python
TLX_DIMENSIONS = {
    "Custom Dimension": {
        "description": "Description of the dimension",
        "low": "Low anchor",
        "high": "High anchor"
    }
}
```

### Changing Score Interpretation

Modify the score interpretation thresholds in the `display_score` function.

## 📊 Data Export

Assessment data can be exported to CSV with the following columns:

- Timestamp
- Task Name
- TLX Score
- Type (Weighted/Unweighted)
- Individual dimension ratings

## 🔬 Research Applications

This tool is useful for:

- **Usability Testing**: Measure workload in user interface studies
- **Task Analysis**: Evaluate workload in different task conditions
- **System Comparison**: Compare workload across different systems or interfaces
- **Longitudinal Studies**: Track workload changes over time

## 📚 References

- Hart, S. G., & Staveland, L. E. (1988). Development of NASA-TLX (Task Load Index): Results of empirical and theoretical research. *Advances in Psychology*, 52, 139-183.

## 🐛 Troubleshooting

### Data Not Saving

- Ensure you're using the same browser session
- Check browser storage permissions
- Data is stored in session state (cleared on refresh)

### Visualization Issues

- Ensure all dependencies are installed
- Check browser console for errors
- Try refreshing the page

## 🚀 Deployment

### Streamlit Cloud

1. Push code to GitHub
2. Connect to [Streamlit Cloud](https://streamlit.io/cloud)
3. Deploy!

### Docker

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

## 📄 License

This project is part of the JJB Gallery portfolio. See the main repository LICENSE file.

## 🔗 Related Projects

- [CrewAI](../Crewai/README.md) - Multi-agent system
- [RAG Model](../RAG_Model/README.md) - Document Q&A
- [iOS Chatbot](../ios_chatbot/README.md) - Chat interface

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues or questions, please open an issue in the main repository.
