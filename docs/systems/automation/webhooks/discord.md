# Discord Webhooks

Discord webhooks are easy to set up and allow you to send automated messages and data updates to any text channel in your server.

## 0. How to get the Webhook URL

1.  Open **Discord** and go to your **Server Settings**.
2.  Navigate to **Integrations** -> **Webhooks**.
3.  Click **Create Webhook** (or **New Webhook**).
4.  Give the webhook a name and select the **Channel** it should post to.
5.  Click **Copy Webhook URL**.
6.  The URL will look like `https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN`.

## 1. Bash Example (using `curl`)

```bash
#!/bin/bash

# Environment variables
DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN"

# JSON Payload (supports embeds)
PAYLOAD='{
  "content": "Hello from Bash! :rocket:",
  "embeds": [{
    "title": "System Update",
    "description": "The script has finished executing successfully.",
    "color": 3447003
  }]
}'

# Send the request
curl -X POST -H 'Content-Type: application/json' --data "$PAYLOAD" "$DISCORD_WEBHOOK_URL"
```

## 2. Python Example (using `requests`)

```python
import requests
import json
import os

def send_discord_message(content, embed_title=None, embed_description=None):
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        print("DISCORD_WEBHOOK_URL environment variable is not set.")
        return

    payload = {
        "content": content
    }

    if embed_title and embed_description:
        payload["embeds"] = [{
            "title": embed_title,
            "description": embed_description,
            "color": 3447003
        }]

    try:
        response = requests.post(
            webhook_url, 
            data=json.dumps(payload),
            headers={'Content-Type': 'application/json'}
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error sending message to Discord: {e}")

if __name__ == "__main__":
    send_discord_message("Hello from Python! :python:", "Discord Embed", "This is a detailed message.")
```

## 3. Docker Example

Using a Python-based Docker image to send a message.

### Dockerfile (Python)
```dockerfile
FROM python:3.9-slim
RUN pip install requests
COPY notify.py /app/notify.py
CMD ["python", "/app/notify.py"]
```

### Docker Run (Bash)
```bash
docker run --rm 
  -e DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN" 
  curlimages/curl:latest 
  -X POST -H 'Content-Type: application/json' 
  --data '{"content": "Direct message from Docker!"}' 
  ${DISCORD_WEBHOOK_URL}
```
