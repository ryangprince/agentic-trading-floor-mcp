# Agentic Trading Floor (MCP-Powered)

An autonomous, multi-agent financial simulation where AI "Traders" operate on a virtual trading floor. Each agent follows a unique investment strategy, performs deep market research via the **Model Context Protocol (MCP)**, and executes trades within a persistent sandbox environment.

## 🏗 System Architecture

### 1. The Trading Floor & Dashboard
* **`app.py` & `trading_floor.py`**: The core orchestration layer. It manages a roster of agents (e.g., Warren, George, Ray, Cathie) and powers a **Gradio-based UI**.
* **Real-time Monitoring**: The dashboard displays portfolio value charts (via Plotly), live-updating holdings tables, and color-coded logs of agent activities.
* **Multi-Model Support**: The floor can run heterogeneous agents using different LLMs (GPT-4o, Gemini, Claude, Grok, or DeepSeek) to compare trading philosophies.

### 2. The MCP Ecosystem
The system leverages a modular architecture where capabilities are decoupled into specialized MCP servers:
* **Market Server (`market_server.py`)**: Fetches real-time and EOD share prices using Polygon.io via the Massive SDK.
* **Accounts Server (`accounts_server.py`)**: Manages the persistent SQLite "ledger." It handles trades, balance checks, and strategy updates.
* **Researcher Server**: A specialized agentic tool that grants Traders access to **Brave Search**, web-fetching, and a **Knowledge Graph** (libSQL).
* **Push Server (`push_server.py`)**: Forwards trade summaries and alerts via **Pushover**.

### 3. Persistence & Logic
* **`accounts.py`**: Defines the `Account` and `Transaction` schemas using Pydantic. It handles the math for PnL, portfolio valuation, and trade execution.
* **`database.py`**: Manages the SQLite backend for accounts, market history, and a centralized logging system.
* **`tracers.py`**: A custom `LogTracer` that generates unique trace IDs for every session, allowing the UI to map specific agent actions back to the underlying logs.

## ✨ Core Features
* **Autonomous Decision Loops**: Agents run on a schedule (e.g., every 60 minutes) to either seek new opportunities or rebalance existing holdings.
* **Strategic Evolution**: Traders can choose to autonomously update or evolve their investment strategy if they feel their current approach is underperforming.
* **Knowledge Graph Memory**: The Researcher agent builds expertise over time, storing info on companies and market conditions in a persistent graph.
* **Simulated Market Rules**: Supports market-open checks, share-price caching, and realistic transaction logging with spread simulation.

## 🛠 Tech Stack
* **Core:** Model Context Protocol (MCP), FastMCP
* **UI:** Gradio, Plotly, Pandas
* **LLMs:** OpenAI (GPT-4o), Gemini, DeepSeek, and Grok
* **Database:** SQLite3
* **Market Data:** Polygon.io (via Massive SDK)
* **Search:** Brave Search API

## 🚀 Installation & Setup

### 1. Configuration
Create a `.env` file in the root directory with your credentials:

```bash
# API Keys
OPENAI_API_KEY=your_key
MASSIVE_API_KEY=your_polygon_key
BRAVE_API_KEY=your_brave_key

# Notifications
PUSHOVER_USER=your_user_key
PUSHOVER_TOKEN=your_app_token

# Simulation Settings
RUN_EVERY_N_MINUTES=60
USE_MANY_MODELS=true
```

### 2. Launching the Floor
The easiest way to start the entire system (including the UI and the automated trading loop) is:

```bash
uv run app.py
```

## 📝 Logic Flow
* **Wake up:** The `trading_floor` triggers a run for all active Traders based on the set interval (e.g., every 60 minutes).
* **Context Retrieval:** The Trader reads its unique strategy and current account state (balance, holdings) from the `accounts_server` resources.
* **Research:** The Trader delegates complex inquiries to the `Researcher` agent, which performs live web searches via Brave and queries its persistent Knowledge Graph for historical context.
* **Action:** Based on the gathered research and its core strategy, the Trader decides to buy, sell, or hold specific assets.
* **Traceability:** Every step, tool call, and internal reasoning chain is logged to `accounts.db` via the `LogTracer` and streamed directly to the Gradio UI for real-time monitoring.
