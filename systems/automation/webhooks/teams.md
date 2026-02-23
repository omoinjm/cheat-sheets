# Microsoft Teams Webhooks

Microsoft Teams uses Incoming Webhooks (or newer Power Automate "Workflows") to send messages to a specific channel. These support Office 365 Connector cards or Adaptive Cards.

## 1. Bash Example (using `curl`)

```bash
#!/bin/bash

# Environment variables
TEAMS_WEBHOOK_URL="https://outlook.office.com/webhook/YOUR_WEBHOOK_ID@YOUR_TENANT_ID/IncomingWebhook/YOUR_TOKEN" # or Power Automate URL

# JSON Payload (Office 365 Connector Card)
PAYLOAD='{
  "@type": "MessageCard",
  "@context": "http://schema.org/extensions",
  "themeColor": "0076D7",
  "summary": "Build Status Update",
  "sections": [{
    "activityTitle": "Deployment Completed",
    "activitySubtitle": "Automated Deployment Script",
    "facts": [
      { "name": "Environment", "value": "Production" },
      { "name": "Status", "value": "Success" }
    ],
    "markdown": true
  }]
}'

# Send the request
curl -X POST -H 'Content-Type: application/json' --data "$PAYLOAD" "$TEAMS_WEBHOOK_URL"
```

## 2. Python Example (using `requests`)

```python
import requests
import json
import os

def send_teams_message(text, title="System Alert"):
    webhook_url = os.getenv("TEAMS_WEBHOOK_URL")
    if not webhook_url:
        print("TEAMS_WEBHOOK_URL environment variable is not set.")
        return

    payload = {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "themeColor": "0076D7",
        "summary": "Notification",
        "sections": [{
            "activityTitle": title,
            "text": text
        }]
    }

    try:
        response = requests.post(
            webhook_url, 
            data=json.dumps(payload),
            headers={'Content-Type': 'application/json'}
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error sending message to Microsoft Teams: {e}")

if __name__ == "__main__":
    send_teams_message("The server is running low on disk space!", "Disk Space Alert")
```

## 3. Docker Example

Running a Python script with environment variables.

### Docker Run (Python)
```bash
docker run --rm 
  -e TEAMS_WEBHOOK_URL="https://outlook.office.com/webhook/YOUR_WEBHOOK_URL" 
  python:3.9-slim 
  bash -c "pip install requests && python -c \"import requests, os; requests.post(os.environ['TEAMS_WEBHOOK_URL'], json={'@type': 'MessageCard', 'text': 'Teams message from Docker container!'})\""
```

### Docker Compose
```yaml
version: '3.8'
services:
  alert-service:
    image: curlimages/curl:latest
    environment:
      - TEAMS_WEBHOOK_URL=https://outlook.office.com/webhook/YOUR_WEBHOOK_URL
    command: >
      -X POST -H 'Content-Type: application/json' 
      --data '{"text": "Service started successfully!"}' 
      ${TEAMS_WEBHOOK_URL}
```
