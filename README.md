# MS Teams H2O.ai Chatbot

A Microsoft Teams bot that integrates [H2O.ai's h2oGPTe](https://h2o.ai/) generative AI platform into Teams conversations. Users can chat with the bot in channels, group chats, or direct messages and receive AI-generated responses powered by h2oGPTe.

## Architecture

```
teams-h2o-bot/
├── bot/                    # Main Teams bot application
│   ├── app.py             # aiohttp web server & Bot Framework adapter
│   ├── h2o_bot.py         # Message handler & h2oGPTe session logic
│   ├── config.py          # Configuration via environment variables
│   └── requirements.txt
└── teams-app/             # Teams app package
    ├── manifest.json
    ├── color.png
    └── outline.png
```

**How it works:**
1. User sends a message in Teams
2. Teams → Bot Framework → `POST /api/messages`
3. Bot extracts message text and looks up (or creates) an h2oGPTe session for that conversation
4. h2oGPTe generates a response
5. Bot replies in the Teams thread

Conversation history is preserved per Teams conversation ID via h2oGPTe sessions (in-memory; resets on restart).

## Prerequisites

- Python 3.10+
- Microsoft Azure Bot registration (App ID, Password, Tenant ID)
- Access to an h2oGPTe Enterprise instance

## Setup

### 1. Configure environment variables

```bash
export MicrosoftAppId=<your-bot-app-id>
export MicrosoftAppPassword=<your-bot-app-password>
export MicrosoftAppTenantId=<your-azure-tenant-id>
export H2OGPTE_URL=<your-h2ogpte-instance-url>
export H2OGPTE_API_KEY=<your-h2ogpte-api-key>
export PORT=8000  # optional, default 8000
```

### 2. Install dependencies

```bash
cd bot/
pip install -r requirements.txt
```

### 3. Run the bot

```bash
python app.py
```

The server starts on `http://0.0.0.0:8000`:
- `GET /` — Health check
- `POST /api/messages` — Teams webhook endpoint

### 4. Expose to the internet

Teams requires a publicly accessible HTTPS URL to deliver messages. Deploy to Azure Web Apps or use a tunnel (e.g. ngrok) for local development.

```bash
az webapp up --runtime python:3.11 --name <your-app-name>
```

## Teams App Package

The `teams-app/` directory contains the manifest and icons needed to sideload or publish the bot in Microsoft Teams Admin Center.

## Key Dependencies

| Package | Purpose |
|---------|---------|
| `botbuilder-core` | Microsoft Bot Framework |
| `aiohttp` | Async HTTP server |
| `h2ogpte` | H2O.ai GPTe SDK |
