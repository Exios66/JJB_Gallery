# Monitoring & Observability Setup

Effective monitoring is crucial for production systems. This guide covers setting up observability for JJB Gallery projects.

## Logging

### Structured Logging

All services are configured to emit JSON-formatted logs for easy parsing.

```json
{"timestamp": "2024-01-20T10:00:00Z", "level": "INFO", "service": "chatui", "message": "Request received", "path": "/api/chat"}
```

### Log Aggregation

We recommend using a centralized log aggregator like **ELK Stack (Elasticsearch, Logstash, Kibana)** or **Grafana Loki**.

**Docker Compose Configuration for Loki:**

```yaml
  loki:
    image: grafana/loki:latest
    ports:
      - "3100:3100"
```

## Metrics

### Prometheus

Services expose metrics at `/metrics` endpoints (where supported).

**Key Metrics to Monitor:**

- **Request Latency**: P95 and P99 response times.
- **Error Rate**: Percentage of 5xx responses.
- **Request Volume**: Requests per second (RPS).
- **Resource Usage**: CPU and Memory consumption.

### Grafana Dashboards

Visualize metrics using Grafana. Create dashboards for:

1. **System Health**: CPU/RAM of all containers.
2. **LLM Performance**: Token generation speed, API latency.
3. **Application Traffic**: Active users, chat sessions.

## Alerting

Set up alerts for critical conditions:

- **Service Down**: Any container exiting unexpectedly.
- **High Error Rate**: > 1% error rate for 5 minutes.
- **High Latency**: P99 latency > 2 seconds.
- **Disk Space**: Storage usage > 80%.

## Health Checks

Implement active health checks using tools like **Uptime Kuma** or AWS Route53 Health Checks against the service endpoints.

---

<div align="center">

**Copyright © Existential Ventures LLC, 2025. All Rights Reserved.**

</div>
