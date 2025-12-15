# Kubernetes Deployment Guide

This guide outlines deploying JJB Gallery projects to a Kubernetes cluster.

## Prerequisites

- Running Kubernetes cluster
- `kubectl` configured
- Container registry (Docker Hub, ECR, GCR)

## Deployment Manifests

Create a `deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: chatui
spec:
  replicas: 3
  selector:
    matchLabels:
      app: chatui
  template:
    metadata:
      labels:
        app: chatui
    spec:
      containers:
      - name: chatui
        image: myregistry/chatui:latest
        ports:
        - containerPort: 3000
        envFrom:
        - configMapRef:
            name: chatui-config
        - secretRef:
            name: chatui-secrets
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
```

## Service Configuration

Expose the application:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: chatui-service
spec:
  selector:
    app: chatui
  ports:
    - protocol: TCP
      port: 80
      targetPort: 3000
  type: LoadBalancer
```

## Scaling

Autoscale based on CPU usage:

```yaml
apiVersion: autoscaling/v1
kind: HorizontalPodAutoscaler
metadata:
  name: chatui-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: chatui
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70
```

## Secrets Management

Use Kubernetes Secrets for sensitive data:

```bash
kubectl create secret generic chatui-secrets --from-env-file=.env.production
```

---

<div align="center">

**Copyright © Existential Ventures LLC, 2025. All Rights Reserved.**

</div>
