import os
from dotenv import load_dotenv
from agents import Agent, Runner, trace, Tool
from agents.mcp import MCPServerStdio
from IPython.display import Markdown, display
from datetime import datetime
from accounts_client import read_accounts_resource, read_strategy_resource, read_account_and_strategy
from accounts import Account

load_dotenv(override=True)

massive_api_key = os.getenv("MASSIVE_API_KEY")

market_mcp = ({"command": "uv", "args": ["run", "market_server.py"]})

trader_mcp_server_params = [
    {"command": "uv", "args": ["run", "accounts_server.py"]},
    {"command": "uv", "args": ["run", "push_server.py"]},
    market_mcp,
]

brave_env = {"BRAVE_API_KEY": os.getenv("BRAVE_API_KEY")}

researcher_mcp_server_params = [
    {"command": "uvx", "args": ["mcp-server-fetch"]},
    {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-brave-search"], "env": brave_env}
]

researcher_mcp_servers = [MCPServerStdio(params, client_session_timeout_seconds=30) for params in researcher_mcp_server_params]
trader_mcp_servers = [MCPServerStdio(params, client_session_timeout_seconds=30) for params in trader_mcp_server_params]
mcp_servers = trader_mcp_servers + researcher_mcp_servers


async def get_researcher(mcp_servers) -> Agent:
    instructions = f"""You are a financial researcher. You are able to search the web for interesting financial news,
    look for possible trading opportunities, and help with research.
    Based on the request, you carry out necessary research and respond with your findings.
    Take time to make multiple searches and get a comprehensive overview, then summarize your findings.
    If there isn't a specific request, then just respond with investment opportunities based on searching the latest news.
    The current datetime is {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    """
    researcher = Agent(
        name="Researcher",
        instructions=instructions,
        model="gpt-4.1-mini",
        mcp_servers=mcp_servers,
    )
    return researcher
    
    
async def get_researcher_tool(mcp_servers) -> Tool:
    researcher = await get_researcher(mcp_servers)
    return researcher.as_tool(
        tool_name="Researcher",
        tool_description="This tool researches online for news and opportunities, \
            either based on your specific request to look into a certain stock, \
            or generally for notable financial news and opportunities. \
            Describe what kind of research you are looking for."
    )


ryan_initial_strategy = "You are a day trader that aggressively buys and sells shares based on news and market conditions."
Account.get("Ryan").reset(ryan_initial_strategy)

display(Markdown(await read_accounts_resource("Ryan")))
display(Markdown(await read_strategy_resource("Ryan")))