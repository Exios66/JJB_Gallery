# Security Policy

Welcome to this repository! Security is a **top priority** for all contributors, maintainers, and users. This SECURITY.md document describes security practices, responsible disclosure, and guidance for keeping the repository safe for everyone.

---

## Supported Versions

| Version  | Supported         | Maintenance         |
|----------|-------------------|--------------------|
|  Latest  | :white_check_mark: | :white_check_mark: |
|  Previous| :white_check_mark: | :x:                |

_Only the latest version is actively maintained and receives security updates._

---

## Reporting a Vulnerability

**If you discover a security vulnerability, please follow these steps:**

1. **Privately disclose the issue.**  
   Email us at [security@opencode.ai](mailto:security@opencode.ai) or contact a maintainer directly. Avoid creating public GitHub issues for vulnerabilities.

2. **Include details:**
   - Affected files and versions
   - Steps to reproduce
   - Any relevant logs or screenshots
   - Your suggested mitigation or patch (if available)

3. **We will:**
   - Respond within 2 business days
   - Triage and validate the report
   - Release a fix as quickly as possible
   - Credit you (with permission) after a public disclosure

---

## Security Best Practices

### For Users

- **Keep up-to-date**: Always use the latest release from GitHub or [official sites](https://opencode.ai).
- **Verify downloads**: Check for sha256 signatures when available.
- **Never share sensitive credentials** in issues, PRs, or chat logs.
- **Review third-party dependencies**: This repo uses several. Monitor for CVEs and update dependencies regularly.

### For Contributors

- **Sign your commits** ([Guide](https://docs.github.com/en/authentication/managing-commit-signature-verification/signing-commits)):
  - `git config --global commit.gpgsign true`
- **Do not include secrets** (API keys, tokens) in code, configs, or docs.
- **Add unit/integration tests** for all security fixes.
- **Run static analysis** and linters before submitting code.
- **Lockdown GitHub Actions**: Reference only trusted actions, pin to a specific commit SHA.
- **Follow the Principle of Least Privilege** in all scripts and integrations.
- **Keep dependencies updated**; submit a PR if you spot an outdated or vulnerable one.

---

## Third-Party Dependencies

This repository makes use of open-source tools and packages (see `requirements.txt` and `package.json` if available).

- Review the dependencies for newly announced vulnerabilities
- Use `pip list --outdated` and `npm audit` (where applicable)
- Managed dependencies are periodically updated by maintainers

---

## Build & Runtime Security

- **Default settings avoid privilege escalation** and limit shell command execution.
- **Do not run scripts with elevated privileges (sudo/root)** unless explicitly required.
- **Kill unnecessary or idle processes** and remove temporary files after execution (see `scripts/free_ram.sh` for an example).
- **Monitor for unauthorized access** or unexpected network traffic during use.
- Use secure communication methods (e.g., SSH, HTTPS).

---

## Responsible Disclosure

We adhere to [responsible disclosure principles](https://www.disclose.io/).  
All security concerns will be kept confidential until a patch is available and users have reasonable time to upgrade.

---

## Security Contact

- Email: [security@opencode.ai](mailto:security@opencode.ai)
- Discord: [https://opencode.ai/discord](https://opencode.ai/discord)
- Or contact a maintainer privately

---

Thank you for helping keep the project and its users secure!
