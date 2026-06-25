# Code Block 3 · Multiple Tools (Slide 7)
# Three tools. The model decides which to call, and when.

import asyncio                                   # async runtime
from agents import Agent, Runner, function_tool  # SDK primitives + the tool decorator


@function_tool                                   # expose get_weather as a tool
def get_weather(city: str) -> str:               # city is a string parameter (schema inferred from the hint)
    """Returns the current weather for a given city."""  # description shown to the model
    weather_data = {"london": "Cloudy, 14C", "karachi": "Hot, 38C"}  # mock weather lookup
    return weather_data.get(city.lower(), f"No data for {city}")  # return match or fallback string


@function_tool                                   # expose get_time as a separate tool
def get_time(city: str) -> str:                  # same signature shape as get_weather
    """Returns the current local time in a given city."""  # description for the model
    time_data = {"london": "3:00 PM GMT", "karachi": "8:00 PM PKT"}  # mock time lookup
    return time_data.get(city.lower(), f"No data for {city}")  # return match or fallback string


@function_tool                                   # expose save_note as a tool with a side effect
def save_note(content: str) -> str:              # takes the note text to store
    """Saves a note for the user."""             # description for the model
    print(f"[SAVED NOTE]: {content}")            # simulate persistence by printing (real version would write to disk/DB)
    return f"Note saved: {content}"              # confirmation string fed back to the model


agent = Agent(                                   # one agent that owns all three tools
    name="Personal Assistant",                   # name for tracing
    instructions=(                               # multi-line system prompt
        "You can check weather, check time, and save notes. "  # tell the model its capabilities
        "When asked about a city, check both weather and time."  # encourage calling two tools together
    ),                                           # end of instructions
    tools=[get_weather, get_time, save_note],    # give the model all three tools to choose from
)                                                # the model now decides which tool(s) fit the request


async def main():                                # async entry coroutine
    result = await Runner.run(                    # run the loop
        agent,                                   # the personal assistant
        "What's it like in London right now?",   # ambiguous-ish prompt that may trigger multiple tools
    )                                            # model may call get_weather AND get_time in one turn (parallel calls)
    print(result.final_output)                   # print the final combined answer


if __name__ == "__main__":                       # script guard
    asyncio.run(main())                          # run it

# WHAT TO WATCH FOR:
#   The model might call BOTH get_weather and get_time in a single turn (parallel tool calls),
#   or call one, see the result, then decide to call the other. The model decides.
#   That's what makes it agentic.
