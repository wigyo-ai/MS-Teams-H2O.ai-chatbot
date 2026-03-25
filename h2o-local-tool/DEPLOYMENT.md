# Deployment Guide — H2O Data Utility MCP Tool

> Based on the official h2oGPTe documentation:
> https://docs.h2o.ai/enterprise-h2ogpte/guide/agents/mcp-servers/create-local-mcp-tool

## Overview

This guide walks through building, testing, and deploying the `h2o-data-utility` MCP server to Enterprise h2oGPTe as a Local MCP Tool.

---

## Prerequisites

| Requirement | Notes |
|---|---|
| Python 3.10+ | Required by the `mcp` SDK |
| `pip` | For local testing |
| `zip` CLI | For building the bundle (`build.sh`) |
| h2oGPTe Enterprise access | Role with permission to create tools under **Agents > Tools** |

---

## Step 1 — Local Smoke Test (Recommended)

Before uploading to h2oGPTe, verify the server starts correctly on your machine.

```bash
# From the h2o-local-tool directory

# 1. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start the server (it will block, waiting on stdin — that is correct)
python server.py
```

You should see no errors. The process waits for MCP JSON-RPC messages on stdin.
Press `Ctrl+C` to stop it. If it exits cleanly without a traceback, the server is healthy.

---

## Step 2 — Build the ZIP Bundle

h2oGPTe expects the ZIP to contain a **named directory** with your files inside it.

```bash
# From the *parent* directory (one level above h2o-local-tool/)
chmod +x h2o-local-tool/build.sh
./h2o-local-tool/build.sh
```

This produces `h2o-local-tool.zip` in the current directory.

**Verify the zip structure** — files must appear inside a named directory:

```bash
unzip -l h2o-local-tool.zip
```

Expected output:

```
Archive:  h2o-local-tool.zip
  Length      Date    Time    Name
---------  ---------- -----   ----
     ...   ...         ...    h2o-local-tool/server.py
     ...   ...         ...    h2o-local-tool/description.md
     ...   ...         ...    h2o-local-tool/requirements.txt
---------                     -------
```

---

## Step 3 — Upload to Enterprise h2oGPTe

1. Log in to your h2oGPTe Enterprise instance.
2. Navigate to **Agents** → **Tools**.
3. Click **+ New Tool**.
4. From the tool type dropdown, select **Local MCP Tools**.
5. Upload `h2o-local-tool.zip` via the file upload dialog.
6. h2oGPTe will unpack the ZIP, install `requirements.txt`, and register `server.py` as the entry point.

---

## Step 4 — Configure the Tool

After uploading, you will be presented with configuration options before clicking **Add Tool**:

| Option | Description |
|---|---|
| **MCP Usage Mode** | Select **Runner** (default) — the tool executes MCP calls on behalf of the agent. Choose **Creator** only if this tool is meant to generate other tools. |
| **Enable by Default** | Toggle on to automatically make this tool available in all new chat sessions without manual activation each time. |

Click **Add Tool** to finalize registration.

---

## Step 5 — Activate the Tool in a Chat Session

1. Open a new chat session with your preferred agent.
2. Click the **settings / gear icon** to open Agent Configuration.
3. Find **h2o-data-utility** under the **Custom Tools** section.
4. Enable the tool.

The following tools are now available to the model:

| Tool name | Input | Output |
|---|---|---|
| `generate_uuid` | _(none)_ | A UUID v4 string, e.g. `"a3f1c2d4-..."` |
| `random_choice` | `options`: list of strings | One randomly selected string |

---

## Step 6 — Verify in h2oGPTe

Use the chat interface to confirm the tools are wired up correctly. Example prompts:

```
Generate a UUID for me.
```
```
Pick one of these at random: ["alpha", "beta", "gamma", "delta"]
```

Confirm the model invokes the tools and returns real values rather than hallucinating them.

---

## Updating the Tool

1. Edit `server.py` (and `requirements.txt` if dependencies changed).
2. Re-run `./build.sh` to produce a fresh ZIP.
3. In h2oGPTe, navigate to **Agents** → **Tools**, find the tool entry, and replace it with the new ZIP.
4. h2oGPTe will restart the server process automatically.

> **Note:** You do not need to change the server name `"h2o-data-utility"` between updates unless you want h2oGPTe to treat it as a distinct new tool.

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Upload rejected | ZIP structure incorrect | Verify with `unzip -l`; files must be inside a named directory |
| Tool not listed after upload | Wrong tool type selected | Re-upload and choose **Local MCP Tools** from the dropdown |
| Tool status shows **Error** | Missing or incompatible dependency | Check `requirements.txt`; ensure `mcp>=1.0.0` is present |
| Server exits immediately | Python syntax error or import failure | Run `python server.py` locally and read the traceback |
| Tool not visible in chat | "Enable by Default" was off | Enable manually via Agent Configuration → Custom Tools |
| `random_choice` raises an error | Empty `options` list passed | Ensure the caller always provides at least one item |

---

## File Reference

```
h2o-local-tool/
├── server.py          # MCP stdio server — main entry point (required)
├── description.md     # Human-readable tool description (optional)
├── requirements.txt   # Python dependencies
└── build.sh           # Packaging script → produces h2o-local-tool.zip
```
