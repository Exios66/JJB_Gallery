# Docker Deployment Guide

This guide details how to deploy JJB Gallery projects using Docker.

## Prerequisites

- Docker Engine installed
- Docker Compose (optional, but recommended)

## Building Images

Navigate to the project directory and build the image:

```bash
# Example for ChatUi
cd projects/ChatUi
docker build -t chatui:latest .
```

## Running Containers

```bash
docker run -d \
  -p 3000:3000 \
  --env-file .env.production \
  --name chatui \
  --restart always \
  chatui:latest
```

## Docker Compose (Recommended)

Create a `docker-compose.yml` for your stack:

```yaml
version: '3.8'
services:
  chatui:
    build: ./projects/ChatUi
    ports:
      - "3000:3000"
    env_file: .env.production
    restart: always

  litellm:
    build: ./projects/litellm
    ports:
      - "4000:4000"
    env_file: .env.production
    restart: always
```

Run with:

```bash
docker-compose up -d --build
```

## Optimization

1. **Multi-stage builds**: Ensure Dockerfiles use multi-stage builds to minimize image size.
2. **Non-root user**: Run containers as a non-root user for security.
3. **Volume mounting**: Mount volumes for persistent data (e.g., vector stores, databases).

```yaml
    volumes:
      - ./data:/app/data
```
