# Code Block 4 · Inspecting RunResult (Slide 8)
# RunResult tells you everything. This is how you debug production agents.

import asyncio                                   # async runtime
from agents import Agent, Runner, function_tool, enable_verbose_stdout_logging  # SDK primitives + tool decorator


enable_verbose_stdout_logging()

@function_tool                                   # a single tool so the run has something to trace
def get_weather(city: str) -> str:               # string in, string out
    """Returns the current weather for a given city."""  # tool description
    weather_data = {"london": "Cloudy, 14C", "karachi": "Hot, 38C"}  # mock data
    return weather_data.get(city.lower(), f"No data for {city}")  # lookup with fallback


agent = Agent(                                   # define the agent we'll inspect
    name="Weather Bot",                          # this name shows up as result.last_agent.name
    instructions="Help users check the weather. Use get_weather when asked.",  # system prompt
    tools=[get_weather],                         # one tool registered
)                                                # ready to run


async def main():                                # async entry coroutine
    result = await Runner.run(                    # run the loop and capture the RunResult
        agent,                                   # the weather bot
        "What's the weather in London?",         # user input
    )                                            # result now holds the full trace of the run

    # What the model produced
    print("Final output:", result.final_output)  # final_output = the model's final text answer

    # Which agent finished the run
    print("Last agent:", result.last_agent.name)  # last_agent = the agent active at the end (matters with handoffs)

    # Everything that happened during the run
    # for item in result.new_items:                # new_items = ordered list of every step (calls, outputs, messages)
    #     print(f"  [{item.type}] {item}")         # item.type labels each step; printing item shows its payload


if __name__ == "__main__":                       # script guard
    asyncio.run(main())                          # run it

# What this prints (roughly):
#   Final output: The weather in London is currently cloudy, 14C.
#   Last agent: Weather Bot
#     [tool_call]     get_weather(city="London")
#     [tool_output]   "Cloudy, 14C"
#     [message]       The weather in London is currently cloudy...
#
# WHY THIS MATTERS: In production your agent will do something weird at 2 AM.
# new_items is how you find out what happened — every tool call, result, and model message.
# This is observability (deep dive in Week 7); for now, just know it's there.
