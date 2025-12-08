# Production Security Hardening

This guide outlines security best practices for hardening JJB Gallery deployments.

## Network Security

1. **TLS/SSL**: Always serve applications over HTTPS. Use Let's Encrypt for free certificates.
2. **Firewall**: Configure `ufw` or cloud security groups to allow only necessary ports (e.g., 443, 80).
3. **Private Networks**: Run databases and internal services (like Vector DBs) in private subnets, not exposed to the public internet.

## Application Security

1. **API Keys**:
    - Never commit keys to version control.
    - Use environment variables or secrets management systems (Vault, AWS Secrets Manager).
    - Rotate keys periodically.

2. **Input Validation**:
    - Sanitize all user inputs to prevent injection attacks (SQLi, XSS).
    - Validate file uploads (check types and sizes) in RAG systems.

3. **Rate Limiting**:
    - Implement rate limiting (e.g., Nginx, Redis) to prevent DDoS and abuse of expensive LLM APIs.

## Container Security

1. **Non-Root User**: Ensure Docker containers run as a non-root user.

    ```dockerfile
    USER node
    ```

2. **Minimal Images**: Use Alpine or distroless images to reduce attack surface.
3. **Image Scanning**: Scan images for vulnerabilities using Trivy or Docker Scan.

## Dependency Management

1. **Regular Updates**: Run `npm audit` and `pip-audit` regularly.
2. **Pin Versions**: Pin dependency versions in `requirements.txt` and `package.json` to prevent supply chain attacks.

## LLM Specific Security

1. **Prompt Injection**: Implement guardrails to detect and block malicious prompts.
2. **Data Leakage**: Ensure private data sent to RAG systems is sanitized and encrypted at rest.
3. **Output Validation**: Sanitize LLM outputs before rendering to prevent XSS.
