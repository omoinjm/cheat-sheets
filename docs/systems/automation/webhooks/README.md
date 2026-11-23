# Webhook Automation

This directory contains cheat sheets and code examples for sending notifications to common collaboration platforms via Incoming Webhooks.

## Support Platforms
- [Slack](./slack.md)
- [Discord](./discord.md)
- [Microsoft Teams](./teams.md)

## Usage Summary
Each guide provides:
1. **Bash Examples**: Lightweight `curl` commands for quick scripting.
2. **Python Examples**: Using the `requests` library for more robust integrations.
3. **Docker Examples**: How to run these notifications in isolated environments or CI/CD pipelines.

## Security Note
Never hardcode your Webhook URLs in your scripts. Use environment variables to pass them securely.
