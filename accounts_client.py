import mcp
from mcp.client.stdio import stdio_client
from mcp import StdioServerParameters
from agents import FunctionTool
import json

params = StdioServerParameters(command="uv", args=["run", "accounts_server.py"], env=None)

async def list_accounts_tools():
    async with stdio_client(params) as streams:
        async with mcp.ClientSession(*streams) as session:
            await session.initialize()
            tools_result = await session.list_tools()
            return tools_result.tools
        
async def call_accounts_tool(tool_name, tool_args):
    async with stdio_client(params) as streams:
        async with mcp.ClientSession(*streams) as session:
            await session.initialize()
            result = await session.call_tool(tool_name, tool_args)
            return result
        
async def read_accounts_resource(name):
    async with stdio_client(params) as streams:
        async with mcp.ClientSession(*streams) as session:
            await session.initialize()
            result = await session.read_resource(f"accounts://accounts_server/{name}")
            return result.contents[0].text
        
async def read_strategy_resource(name):
    async with stdio_client(params) as streams:
        async with mcp.ClientSession(*streams) as session:
            await session.initialize()
            result = await session.read_resource(f"accounts://strategy/{name}")
            return result.contents[0].text
        
"""
ISSUE: The read_accounts_resource and read_strategy_resource functions are giving me an error when I run them in testing.ipynb.
Each function is creating a new MCP client connection, and when I am calling them back to back in testing.ipynb 
there's a race condition with closing connections. The error happens because the connection cleanup from the first 
call interferes with the second call starting up.

SOLUTION: Create a combined function that reuses a single connection for both reads, 
which is more efficient and avoids the connection cleanup race condition entirely.
So, I am adding a new function below that has the combined functionality of the 
read_accounts_resource and read_strategy_resource functions.

Side note: A race condition is when the outcome of your code depends on the 
timing of events that aren't fully under your control.
"""

async def read_account_and_strategy(name):
    """Read both account and strategy in a single session"""
    async with stdio_client(params) as streams:
        async with mcp.ClientSession(*streams) as session:
            await session.initialize()
            account = await session.read_resource(f"accounts://accounts_server/{name}")
            strategy = await session.read_resource(f"accounts://strategy/{name}")
            return account.contents[0].text, strategy.contents[0].text
        
async def get_accounts_tools_openai():
    openai_tools = []
    for tool in await list_accounts_tools():
        schema = {**tool.inputSchema, "additionalProperties": False}
        openai_tool = FunctionTool(
            name=tool.name,
            description=tool.description,
            params_json_schema=schema,
            on_invoke_tool=lambda ctx, args, toolname=tool.name: call_accounts_tool(toolname, json.loads(args))
                
        )
        openai_tools.append(openai_tool)
    return openai_tools
