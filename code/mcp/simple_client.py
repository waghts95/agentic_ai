import asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client

async def main():
    # Connect to server - use /sse endpoint
    url = "http://localhost:8000/sse"
    
    async with sse_client(url) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            result = await session.call_tool("add_numbers", {"a": 10, "b": 20})
            print(f"Result: {result.content[0].text}")

asyncio.run(main())