"""
LangChain Master Agent with Sub-Agents

This script creates a master agent that coordinates two sub-agents:
1. Verification_agent - Handles weather queries (with hardcoded data)
2. sanction_agent - Handles multiplication calculations

Requirements:
- Set OPENAI_API_KEY environment variable
- LangChain v1.1.0+
"""

from langchain.agents import create_agent
from langchain.tools import Tool
from langchain_openai import ChatOpenAI
import json

# Model configuration - change to "gpt-5-nano" if available, or use "gpt-4o-mini" as fallback
MODEL_NAME = "gpt-4o-mini"  # Note: "gpt-5-nano" doesn't exist yet, using gpt-4o-mini


# Dummy weather data (hardcoded)
WEATHER_DATA = {
    "New York": {"temperature": 72, "condition": "Sunny", "humidity": 65},
    "London": {"temperature": 58, "condition": "Cloudy", "humidity": 80},
    "Tokyo": {"temperature": 68, "condition": "Rainy", "humidity": 75},
    "Paris": {"temperature": 64, "condition": "Partly Cloudy", "humidity": 70},
}


def get_weather(location: str) -> str:
    """Get weather information for a location. Returns hardcoded weather data."""
    location = location.strip()
    if location in WEATHER_DATA:
        data = WEATHER_DATA[location]
        return json.dumps({
            "location": location,
            "temperature": data["temperature"],
            "condition": data["condition"],
            "humidity": data["humidity"]
        }, indent=2)
    else:
        # Return default data for unknown locations
        return json.dumps({
            "location": location,
            "temperature": 70,
            "condition": "Unknown",
            "humidity": 60,
            "note": "Location not in database, returning default values"
        }, indent=2)


def calculate_multiplication(input_str: str) -> str:
    """Calculate the multiplication of two numbers. Input should be two numbers separated by comma."""
    try:
        # Parse input: "5, 3" or "5,3" or "10.5, 2"
        parts = [p.strip() for p in input_str.split(",")]
        if len(parts) != 2:
            return json.dumps({"error": "Please provide exactly two numbers separated by comma"}, indent=2)
        
        a = float(parts[0])
        b = float(parts[1])
        result = a * b
        
        return json.dumps({
            "operation": "multiplication",
            "a": a,
            "b": b,
            "result": result
        }, indent=2)
    except ValueError as e:
        return json.dumps({"error": f"Invalid input: {str(e)}. Please provide two numbers separated by comma."}, indent=2)


# Create tools for Verification Agent
verification_tools = [
    Tool(
        name="get_weather",
        func=get_weather,
        description="Get weather information for a given location. Input should be a location name (e.g., 'New York', 'London', 'Tokyo', 'Paris'). Returns temperature, condition, and humidity."
    )
]

# Create tools for Sanction Agent
sanction_tools = [
    Tool(
        name="calculate_multiplication",
        func=calculate_multiplication,
        description="Calculate the multiplication of two numbers. Input should be a string with two numbers separated by comma (e.g., '5, 3' or '10.5, 2')."
    )
]


def create_sub_agent(name: str, tools: list, model_name: str = MODEL_NAME):
    """Create a sub-agent with specified tools."""
    system_prompt = f"You are the {name}. You have access to the following tools. Use them to help answer questions."
    
    agent = create_agent(
        model=ChatOpenAI(model=model_name, temperature=0),
        tools=tools,
        system_prompt=system_prompt
    )
    return agent


# Create sub-agents
verification_agent = create_sub_agent("Verification_agent", verification_tools, model_name=MODEL_NAME)
sanction_agent = create_sub_agent("sanction_agent", sanction_tools, model_name=MODEL_NAME)


def call_verification_agent(query: str) -> str:
    """Call the Verification agent to handle verification-related tasks."""
    result = verification_agent.invoke({"role": "user", "content": query})
    # The result is a list of messages, get the last AI message
    if isinstance(result, list) and len(result) > 0:
        return result[-1].content if hasattr(result[-1], 'content') else str(result[-1])
    return str(result)


def call_sanction_agent(query: str) -> str:
    """Call the Sanction agent to handle sanction-related tasks."""
    result = sanction_agent.invoke({"role": "user", "content": query})
    # The result is a list of messages, get the last AI message
    if isinstance(result, list) and len(result) > 0:
        return result[-1].content if hasattr(result[-1], 'content') else str(result[-1])
    return str(result)


# Create tools for Master Agent (sub-agents as tools)
master_agent_tools = [
    Tool(
        name="Verification_agent",
        func=call_verification_agent,
        description="Use this agent for verification tasks, weather queries, and location-based information. Input should be a clear question or request."
    ),
    Tool(
        name="sanction_agent",
        func=call_sanction_agent,
        description="Use this agent for sanction-related tasks and mathematical calculations, especially multiplications. Input should be a clear question or request."
    )
]


# Create Master Agent
def create_master_agent():
    """Create the master agent that can route to sub-agents."""
    system_prompt = """You are a Master Agent that coordinates between two specialized sub-agents:
1. Verification_agent: Handles verification tasks and weather queries
2. sanction_agent: Handles sanction-related tasks and mathematical calculations

Your role is to understand the user's request and route it to the appropriate sub-agent. 
If a request involves weather or verification, use Verification_agent.
If a request involves calculations or sanctions, use sanction_agent.
You can also use both agents if needed."""
    
    agent = create_agent(
        model=ChatOpenAI(model=MODEL_NAME, temperature=0),
        tools=master_agent_tools,
        system_prompt=system_prompt
    )
    return agent


# Initialize Master Agent
master_agent = create_master_agent()


if __name__ == "__main__":
    print("=" * 60)
    print("Master Agent with Sub-Agents")
    print("=" * 60)
    print("\nAvailable sub-agents:")
    print("1. Verification_agent - Weather and verification tasks")
    print("2. sanction_agent - Calculations and sanction tasks")
    print("\n" + "=" * 60 + "\n")
    
    # Example interactions
    examples = [
        "What's the weather in New York?",
        "Calculate 15 multiplied by 7",
        "What's the weather in Tokyo and calculate 3 times 4?",
    ]
    
    for example in examples:
        print(f"User: {example}")
        print("-" * 60)
        response = master_agent.invoke({"role": "user", "content": example})
        # The response is a list of messages, get the last AI message
        if isinstance(response, list) and len(response) > 0:
            output = response[-1].content if hasattr(response[-1], 'content') else str(response[-1])
        else:
            output = str(response)
        print(f"Response: {output}")
        print("\n" + "=" * 60 + "\n")
