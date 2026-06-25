# Code Block 1 · Bare Minimum Agent (Slide 5)
# No tools. The loop runs once. Functionally identical to a raw API call.

import asyncio                                   # async runtime; provides the event loop and asyncio.run() entry point
from agents import Agent, Runner                 # Agent = the definition; Runner = the loop that executes it

agent = Agent(                                   # create the agent definition (not the loop itself)
    name="Assistant",                            # name is used for tracing/observability, not by the model's logic
    instructions="You are a helpful assistant. Be concise.",  # the system prompt that steers the model
)                                                # no tools passed, so the model can only generate text


# async def main():                                # async because the SDK is async-native
result =  Runner.run_sync(                    # start the agent loop; await because it does network I/O
        agent,                                   # which agent to run
        "What is the capital of France?",        # the user input for this run
    )                                            # with no tools, the loop runs exactly once: generate text, done
print(result.final_output)                   # final_output is the string the model produced


# if __name__ == "__main__":                       # only run when executed directly, not when imported
#     asyncio.run(main())                          # asyncio.run() is the entry point that drives the coroutine

# SHORTCUT: Runner.run_sync(agent, "...") skips the async boilerplate.
# Fine for scripts, but it won't work inside FastAPI or Jupyter (they already run an event loop).
