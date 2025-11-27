import asyncio
from langchain_ollama import ChatOllama
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from mcp import ClientSession
from mcp.client.sse import sse_client

@tool
async def add(a: int, b: int) -> int:
    """Add two numbers"""
    async with sse_client("http://localhost:8000/sse") as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool("add", {"a": a, "b": b})
            return int(result.content[0].text)

async def main():
    llm = ChatOllama(model="mistral", base_url="http://localhost:11434")
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant."),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])
    
    agent = create_tool_calling_agent(llm, [add], prompt)
    executor = AgentExecutor(agent=agent, tools=[add])
    
    result = await executor.ainvoke({"input": "What is 15 + 27?"})
    print(result["output"])

asyncio.run(main())