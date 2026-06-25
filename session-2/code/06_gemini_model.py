# Code Block 6 · Gemini via OpenAI Chat Completions Model (Slide 10)
# Same Agent, same Runner, same tools. Different model underneath.

import os                                        # to read environment variables (the API key)
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel  # SDK + OpenAI-compatible client wrappers
from agents.run import RunConfig                 # RunConfig lets us override the model/provider for a run
from dotenv import load_dotenv                   # loads variables from a .env file into the environment
import asyncio

load_dotenv()                                    # read .env so os.getenv() can see GEMINI_API_KEY

api_key = os.getenv("GEMINI_API_KEY")            # fetch the Gemini API key from the environment

external_client = AsyncOpenAI(                    # an OpenAI-style client, but pointed at Gemini's endpoint
    api_key=api_key,                             # authenticate with the Gemini key
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",  # Gemini's OpenAI-compatible URL
)                                                # now this client talks to Google instead of OpenAI

model = OpenAIChatCompletionsModel(              # wrap that client so the SDK can use it as a model
    model="gemini-2.5-flash",                    # the specific Gemini model to call
    openai_client=external_client,               # the client created above
)                                                # model object the Agent/Runner understand

config = RunConfig(                              # per-run configuration overrides
    model=model,                                 # use the Gemini-backed model for this run
    model_provider=external_client,              # tell the runner which provider/client to use
    tracing_disabled=True,                       # disable OpenAI tracing (we're not on OpenAI's platform)
)                                                # config passed into Runner.run() below

agent = Agent(                                   # define the agent
    name="GeminiAssistant",                      # name for tracing
    instructions="You only respond in haikus.",  # system prompt (5-7-5 styled replies)
    model=model,                                 # attach the Gemini-backed model directly to the agent
)   

                                             # same Agent class as every other example
async def main():                                # wrap the run in an async function
    result = await Runner.run(                    # run the loop
        agent,                                   # the Gemini assistant
        "Tell me about recursion.",              # user prompt
        run_config=config,                       # apply the RunConfig (model + provider + tracing off)
    )                                            # everything else is identical to the OpenAI examples
    print(result.final_output)                   # print the haiku response


if __name__ == "__main__":                       # script guard — at MODULE level, not inside main()
    asyncio.run(main())                          # this is what actually calls main() and drives the loop
# How this works:
#   Gemini exposes an OpenAI-compatible endpoint at googleapis.com.
#   We point AsyncOpenAI at that endpoint instead of OpenAI's servers.
#   OpenAIChatCompletionsModel wraps it for the SDK.
#   RunConfig passes the model + provider and disables OpenAI tracing.
#   Everything else is identical: same Agent, same Runner, same tools.
#
# NOT LOCKED IN: your agents aren't tied to OpenAI. In production you might use
# GPT for orchestration and Gemini for cheap classification.
#
# NOTE: This snippet uses top-level `await` (as shown on the slide), which works in
# Jupyter or an async REPL. To run as a plain script, wrap it in an async main():
#
#   import asyncio
#   async def main():
#       result = await Runner.run(agent, "Tell me about recursion.", run_config=config)
#       print(result.final_output)
#   asyncio.run(main())
