# MCP Server Project

## What is this?

This project builds a complete MCP (Model Context Protocol) setup from scratch. MCP is a standard that lets AI assistants like Claude use external tools — a calculator, a weather checker, an animation engine — by connecting to small programs called **MCP servers**.

## Project Structure

```
D:\BJIT\MCP\
├── main.py               ← Local server (stdio transport, for Claude Desktop)
├── production_run.py      ← Deployment server (http transport, for Prefect Horizon)
├── client.py              ← Streamlit chat client (connects to all servers)
├── requirements.txt       ← Python package dependencies
├── .env                   ← API keys (never pushed to GitHub)
├── .gitignore             ← Files excluded from Git
├── README.md              ← This file
└── venv/                  ← Virtual environment (excluded from Git)
```

## Requirements Overview

| # | Requirement | Status |
|---|-------------|--------|
| 1 | Custom Tools MCP Server (Age Calculator + Random Number) | In Progress |
| 2 | Manim MCP Server Integration | Pending |
| 3 | Weather MCP Server Integration | Pending |
| 4 | Additional MCP Server (Optional) | Pending |
| 5 | Deploy Custom Server to Prefect Horizon | Pending |
| 6 | Build Custom Streamlit MCP Client | Pending |

## Architecture

```
USER (typing in Claude Desktop or Streamlit Client)
  │
  ▼
LLM (Claude — decides which tool to use)
  │
  ├──► Server 1: Custom Tools (Horizon URL) ──► age calculator, random number
  │         deployed on the internet via Prefect Horizon
  │
  ├──► Server 2: Weather (local stdio) ──► weather forecast (AccuWeather API)
  │         runs on your machine, from github.com/adhikasp/mcp-weather
  │
  └──► Server 3: Manim (local stdio) ──► animations and videos
              runs on your machine, from github.com/abhiemj/manim-mcp-server
```

### Why this architecture?

- **Free tier constraint:** Claude's free tier allows only **one** custom deployed MCP server.
- **Solution:** Bundle all custom tools into one server, deploy that to Horizon. Run the weather and Manim servers locally — they don't count against the limit.

## Setup Instructions

### Prerequisites

- Python 3.10+ (`python --version`)
- Git (`git --version`)
- pip (`pip --version`)
- Claude Desktop installed on Windows

### Step 1: Create the project and virtual environment

```bash
# Navigate to your project folder
cd D:\BJIT\MCP

# Create virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# Install FastMCP
pip install fastmcp
```

### Step 2: Build the local server (main.py)

`main.py` contains your custom tools and runs with **stdio transport** — meant for local use with Claude Desktop.

**Tools included:**

- `calculate_age(date_of_birth)` — Takes a date in YYYY-MM-DD format, returns current age in years, months, and days.
- `random_number(min_value, max_value)` — Returns a random integer in the given range. *(to be added)*

**Testing a tool:**

```bash
# List all tools in the server
fastmcp list main.py

# Call a specific tool
fastmcp call main.py --target calculate_age date_of_birth=2000-01-15
```

### Step 3: Build the deployment server (production_run.py)

*(Coming next)* — Same tools as `main.py`, but runs with `transport="http"` on port 8000 for deployment to Prefect Horizon.

### Step 4: Deploy to Prefect Horizon

*(Coming next)* — Push to GitHub, connect to horizon.prefect.io, deploy to get a live URL.

### Step 5: Set up Weather MCP Server

*(Coming next)* — Uses `adhikasp/mcp-weather` with a free AccuWeather API key.

### Step 6: Set up Manim MCP Server

*(Coming next)* — Clone `abhiemj/manim-mcp-server`, install Manim + FFmpeg + LaTeX.

### Step 7: Connect to Claude Desktop

Edit `%APPDATA%\Claude\claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "my-tools": {
      "transport": "streamable_http",
      "url": "https://your-server-name.fastmcp.app/mcp"
    },
    "weather": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/adhikasp/mcp-weather.git", "mcp-weather"],
      "env": {
        "ACCUWEATHER_API_KEY": "your_key_here"
      }
    },
    "manim": {
      "command": "python",
      "args": ["D:\\path\\to\\manim_server.py"],
      "env": {
        "MANIM_EXECUTABLE": "D:\\path\\to\\manim"
      }
    }
  }
}
```

### Step 8: Build Streamlit Client (client.py)

*(Coming next)* — A custom chat UI that connects to all servers simultaneously using LangChain.

## Key Concepts for Beginners

### What is an MCP Server?
A small program that holds tools and waits for an AI to ask it to use them. Think of it as a toolbox that the AI can reach into.

### What is a Tool?
A Python function decorated with `@mcp.tool`. The AI reads the function's name, type hints, and docstring to decide when and how to use it.

### What is a Resource?
Information the AI can read for context (like a reference document), as opposed to a tool which performs an action.

### Stdio vs HTTP Transport
- **Stdio (local):** The server runs as a process on your computer. Claude Desktop starts it and talks to it directly. Fast, simple, no internet needed.
- **HTTP (remote):** The server runs on the internet and listens for requests over a URL. This is what "deploying" means.

### What is Prefect Horizon?
A hosting platform for MCP servers. You give it a GitHub repo, it deploys your server and gives you a live URL.

### What is FastMCP?
A Python library that makes building MCP servers easy. It handles all the protocol details — you just write normal Python functions.

## Environment

- **OS:** Windows
- **Python:** 3.11
- **FastMCP:** 4.0.5
- **Git:** 2.55

## Constraints

- Claude free tier: 1 custom deployed server only
- No paid API keys (no Twitter developer account)
- Weather server needs a free AccuWeather API key (free registration)