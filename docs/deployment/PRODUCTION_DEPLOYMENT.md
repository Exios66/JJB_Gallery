# Production Deployment Guide

This guide provides a comprehensive overview of deploying JJB Gallery projects to production environments.

## Deployment Strategies

We support three main deployment strategies:

1. **Docker Containers (Recommended)**
    * **Pros**: Consistent environment, easy scaling, portable.
    * **Cons**: Requires Docker runtime.
    * **Best for**: ChatUi, iOS Chatbot, LiteLLM.

2. **Kubernetes**
    * **Pros**: High availability, auto-scaling, service discovery.
    * **Cons**: High complexity.
    * **Best for**: Large-scale deployments of CrewAI swarms or RAG systems.

3. **Bare Metal / VM**
    * **Pros**: Maximum performance, direct hardware access.
    * **Cons**: Harder to manage dependencies and updates.
    * **Best for**: Performance-critical RAG inference or local LLM hosting.

## General Prerequisites

* **Operating System**: Linux (Ubuntu 22.04 LTS recommended)
* **Runtime**: Docker Engine 24.0+ or Python 3.9+
* **Hardware**:
  * Minimum: 2 vCPU, 4GB RAM
  * Recommended (with LLMs): GPU support (NVIDIA), 16GB+ RAM

## Environment Configuration

All projects use environment variables for configuration. Create a `.env.production` file based on the project's `.env.example`.

**Critical Variables:**

* `NODE_ENV=production` (for JS projects)
* `FLASK_ENV=production` (for Python web apps)
* `LOG_LEVEL=INFO`
* API Keys (`OPENAI_API_KEY`, `DATABASE_URL`, etc.)

## Health Checks

Ensure your load balancer is configured to check these endpoints:

* **ChatUi**: `/health` or `/`
* **LiteLLM**: `/health`
* **iOS Chatbot**: `/api/health`

## Rollback Procedures

Always tag your Docker images or git releases. To rollback:

1. **Docker**: `docker service update --image <previous_image> <service_name>`
2. **Git**: `git checkout <previous_tag> && ./deploy.sh`

## References

* [Docker Deployment](./DOCKER.md)
* [Kubernetes Deployment](./KUBERNETES.md)
* [Security Hardening](../security/PRODUCTION_HARDENING.md)

---

<div align="center">

**Copyright © Existential Ventures LLC, 2025. All Rights Reserved.**

</div>
