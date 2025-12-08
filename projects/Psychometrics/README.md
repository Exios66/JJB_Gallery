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
- **REST API**: Production-ready API for remote assessment collection

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

### Production Setup

```bash
# Install with production dependencies (gunicorn, postgres driver)
pip install -r requirements.txt psycopg2-binary gunicorn
```

## Usage

### Command-Line Interface

Run the interactive assessment tool:

```bash
python main.py
```

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
    performance=5,
    effort=14,
    frustration=8
)

# Calculate scores
tlx.calculate_scores(result)
print(f"Raw TLX Score: {result.raw_tlx_score:.2f}")
```

## 🏭 Production Deployment

### Deployment Strategy

Deploy as a REST API service to collect assessments from web or mobile clients.

### Docker Deployment

1. **Dockerfile**:

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt gunicorn
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "api:app"]
```

2. **Run Container**:

```bash
docker run -d -p 8000:8000 \
  -e DATABASE_URL=postgresql://user:pass@db:5432/psychometrics \
  psychometrics-api:latest
```

### Data Privacy & Compliance

- **GDPR/HIPAA**: Store participant IDs as anonymized hashes. Do not store PII (Personally Identifiable Information) in the assessment database.
- **Data Retention**: Configure automated deletion policies for raw data after the retention period expires.
- **Access Control**: Restrict database access to authorized researchers only.

### Database Setup

For production, use PostgreSQL instead of SQLite:

```sql
CREATE TABLE assessments (
    id UUID PRIMARY KEY,
    participant_hash VARCHAR(64),
    task_name VARCHAR(255),
    ratings JSONB,
    scores JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Monitoring

- **Application Metrics**: Track API latency and error rates.
- **Business Metrics**: Track number of completed assessments per day.
- **Data Quality**: Monitor for anomalies in rating distributions (e.g., all 1s or all 20s).

## API Documentation

### `POST /api/v1/assessments`

Submit a new assessment.

**Request:**

```json
{
  "task_name": "Task A",
  "participant_id": "P001",
  "ratings": {
    "mental_demand": 15,
    "physical_demand": 5,
    "temporal_demand": 10,
    "performance": 2,
    "effort": 12,
    "frustration": 6
  }
}
```

**Response:**

```json
{
  "id": "uuid",
  "raw_tlx": 8.33,
  "status": "success"
}
```

### `GET /api/v1/stats/{task_name}`

Get aggregate statistics for a task.

## Scoring Methods

### Raw TLX Score

`Raw TLX = (Mental + Physical + Temporal + Performance + Effort + Frustration) / 6`

### Weighted TLX Score

Uses pairwise comparisons to determine dimension weights.

## References

- Hart, S. G., & Staveland, L. E. (1988). Development of NASA-TLX.
- [NASA TLX Official Documentation](https://humansystems.arc.nasa.gov/groups/tlx/)

## License

See main repository LICENSE file.
