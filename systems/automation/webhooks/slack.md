# Slack Webhooks

Slack's Incoming Webhooks provide a simple way to post messages from apps into Slack. They use standard HTTP POST requests with a JSON payload.

## 0. How to get the Webhook URL

1.  Go to the [Slack API App Dashboard](https://api.slack.com/apps).
2.  Click **Create New App** (or select an existing one).
3.  Under **Add features and functionality**, click **Incoming Webhooks**.
4.  Toggle **Activate Incoming Webhooks** to **On**.
5.  Click **Add New Webhook to Workspace**.
6.  Select the channel you want to post to and click **Allow**.
7.  Copy the **Webhook URL** (it looks like `https://hooks.slack.com/services/T.../B.../XXXX...`).

## 1. Bash Example (using `curl`)

```bash
#!/bin/bash

# Environment variables
SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR_WORKSPACE_ID/YOUR_CHANNEL_ID/YOUR_WEBHOOK_TOKEN"

# JSON Payload
PAYLOAD="{"text": "Hello from Bash! :rocket:"}"

# Send the request
curl -X POST -H 'Content-type: application/json' --data "$PAYLOAD" "$SLACK_WEBHOOK_URL"
```

## 2. Python Example (using `requests`)

```python
import requests
import json
import os

def send_slack_message(message):
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    if not webhook_url:
        print("SLACK_WEBHOOK_URL environment variable is not set.")
        return

    payload = {
        "text": message
    }

    try:
        response = requests.post(
            webhook_url, 
            data=json.dumps(payload),
            headers={'Content-Type': 'application/json'}
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error sending message to Slack: {e}")

if __name__ == "__main__":
    send_slack_message("Hello from Python! :python:")
```

## 3. Docker Example

Use a lightweight container like `curlimages/curl` for Bash or `python:3.9-slim` for Python scripts.

### Docker Compose
```yaml
version: '3.8'
services:
  notifier:
    image: curlimages/curl:latest
    environment:
      - SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
    command: >
      -X POST -H 'Content-type: application/json' 
      --data '{"text": "Notification from Docker Compose!"}' 
      ${SLACK_WEBHOOK_URL}
```

### Docker Run (Python)
```bash
# Build a simple image or run a script with environment variables
docker run --rm 
  -e SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL" 
  python:3.9-slim 
  bash -c "pip install requests && python -c \"import requests, os; requests.post(os.environ['SLACK_WEBHOOK_URL'], json={'text': 'Dockerized Python message!'})\""
```
