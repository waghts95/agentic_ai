## Weather Assistant - LLM-Powered Tool-Using Agent with Google ADK


import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import FunctionTool
from google.genai import types


# Load environment variables
load_dotenv()

# Validate API key
if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("GOOGLE_API_KEY not found in environment variables")

MODEL_NAME = "gemini-2.0-flash"
APP_NAME = "weather_app"
USER_ID = "user_001"
SESSION_ID = "session_001"


# --- 1. Define the Tool Function ---
async def get_weather_report(city: str) -> dict:
    """
    Retrieves the current weather report for a specified city.
    Use this tool when the user asks for the current weather.
    
    Args:
        city: The name of the city (e.g., 'New York', 'London').
        
    Returns:
        Dictionary containing weather information including status, temperature, and humidity.
    """
    city_lower = city.lower()
    print(f"--- TOOL CALLED: Getting weather for {city.title()} ---")
    
    # Mocking the actual API response
    if "tokyo" in city_lower:
        report = {"status": "sunny", "temperature": "25°C", "humidity": "60%"}
    elif "pune" in city_lower:
        report = {"status": "cloudy", "temperature": "22°C", "humidity": "85%"}
    else:
        report = {
            "status": "unknown",
            "message": f"Sorry, I don't have the current weather data for {city.title()}."
        }
    
    return report


# --- 2. Wrap the function with FunctionTool ---
weather_tool = FunctionTool(get_weather_report)


# --- 3. Define the Agent ---
weather_agent = LlmAgent(
    name="WeatherAssistant",
    model=MODEL_NAME,
    instruction=(
        "You are a helpful and polite weather assistant. "
        "Use the 'get_weather_report' tool whenever the user asks about the weather."
    ),
    tools=[weather_tool]
)


# --- 4. Create Session Service ---
session_service = InMemorySessionService()


# --- 5. Define the Runner (agent, not agents) ---
runner = Runner(
    agent=weather_agent,  # Single agent, NOT agents=[]
    app_name=APP_NAME,
    session_service=session_service
)


# --- 6. Main function to run the agent locally ---
async def main():
    print("Weather Assistant is ready. Type 'exit' to quit.\n")
    
    # Create a session
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID
    )
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        
        # Create message content
        content = types.Content(
            role='user',
            parts=[types.Part(text=user_input)]
        )

        # Stream the agent's response
        print("Agent: ", end="", flush=True)
        async for event in runner.run_async(
            user_id=USER_ID,
            session_id=SESSION_ID,
            new_message=content
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        print(part.text, end="", flush=True)
        
        print()  # Newline after response


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())