import os
from dotenv import load_dotenv

load_dotenv(override=True)

brave_env = {"BRAVE_API_KEY": os.getenv("BRAVE_API_KEY")}
massive_api_key = os.getenv("MASSIVE_API_KEY")

# MCP server for the Trader to read Market data

market_mcp = {"command": "uv", "args": ["run", "market_server.py"]}

# All MCP servers for the Trader: Accounts, Push notification, and the Market

trader_mcp_server_params = [
    {"command": "uv", "args": ["run", "accounts_server.py"]},
    {"command": "uv", "args": ["run", "push_server.py"]},
    market_mcp,
]

# All MCP servers for the Researcher: Fetch (web data), Brave search, and Memory

def researcher_mcp_server_params(name: str): 
    return [
        {"command": "uvx", "args": ["mcp-server-fetch"]},
        {
            "command": "npx", 
            "args": ["-y", "@modelcontextprotocol/server-brave-search"], 
            "env": brave_env,
        },
        {
            "command": "npx",
            "args": ["-y", "mcp-memory-libsql"],
            "env": {"LIBSQL_URL": f"file:./memory/{name}.db"},
        },
    ]