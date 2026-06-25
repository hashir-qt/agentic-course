# Code Block 2 · Single Tool (Slide 6)
# @function_tool turns a Python function into something the model can call.

import asyncio                                   # async runtime for the event loop and asyncio.run()
from agents import Agent, Runner, function_tool  # function_tool = decorator that exposes a Python function to the model


@function_tool                                   # registers the function as a callable tool for the agent
def get_weather(city: str) -> str:               # the type hints (city: str) BECOME the parameter schema
    """Returns the current weather for a given city."""  # the docstring BECOMES the tool description the model sees
    weather_data = {                             # a tiny mock "database" standing in for a real weather API
        "london": "Cloudy, 14C",                 # key is lowercase city, value is the weather string
        "karachi": "Hot, 38C",                   # second mock entry
    }                                            # end of mock data
    return weather_data.get(                     # dict.get() returns the value if present, else the fallback
        city.lower(),                            # normalize input to lowercase so "London" matches "london"
        f"No data for {city}",                   # fallback returned when the city is not in our mock data
    )                                            # this returned string is fed back to the model


agent = Agent(                                   # define the agent
    name="Weather Assistant",                    # name for tracing
    instructions="Help users check the weather. Use get_weather when asked.",  # tells the model when to use the tool
    tools=[get_weather],                         # register the tool(s) the model is allowed to call
)                                                # now it's a real agent: the model can act, not just talk


async def main():                                # async entry coroutine
    result = await Runner.run(                    # run the loop; this time it may take multiple turns
        agent,                                   # the weather agent
        "What's the weather in London?",         # user message that should trigger the tool
    )                                            # Runner: send msg -> model calls tool -> run tool -> feed result -> final answer
    print(result.final_output)                   # the model's final natural-language response


if __name__ == "__main__":                       # standard script guard
    asyncio.run(main())                          # drive the async main()

# Under the hood:
#   1. Runner sends the user message + tool descriptions to the model.
#   2. Model sees get_weather (name, docstring, type hints) and decides to call it.
#   3. Runner executes get_weather(city="London") and gets "Cloudy, 14C".
#   4. Runner sends that result back to the model.
#   5. Model generates a final response using the weather data.
# The docstring IS the description. The type hints ARE the schema. Bad docstrings = bad tool calls.
