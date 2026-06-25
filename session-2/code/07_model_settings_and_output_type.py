# Slide 11 · Agent Configuration: ModelSettings + output_type
# Control how the model behaves (ModelSettings) and what it returns (output_type).

import asyncio                                   # async runtime, so we can run the agent below

# ----------------------------------------------------------------------------
# PART A · MODEL SETTINGS — control how the model behaves
# ----------------------------------------------------------------------------
from agents import Agent, Runner, ModelSettings  # Runner runs the loop; ModelSettings holds generation parameters

classifier_agent = Agent(                        # an agent tuned for deterministic classification
    name="Classifier",                           # name for tracing
    instructions="Classify customer intent.",    # system prompt describing the task
    model="gpt-4o-mini",                         # a small, cheap model is fine for classification
    model_settings=ModelSettings(                # bundle of decoding parameters
        temperature=0,                           # 0 = deterministic (no randomness) for stable labels
    ),                                           # end of model settings
)                                                # this agent will classify intent consistently

# What you can control via ModelSettings:
#   temperature — randomness (0 = deterministic)
#   max_tokens  — cap on output length
#   tool_choice — "auto", "required", or a specific tool name


# ----------------------------------------------------------------------------
# PART B · OUTPUT TYPE — force structured agent output
# ----------------------------------------------------------------------------
from pydantic import BaseModel                   # Pydantic model = the schema the output must match


class WeatherReport(BaseModel):                  # define the exact shape we want back
    city: str                                    # which city the report is for
    temperature: str                             # the temperature value (as a string here)
    conditions: str                              # e.g. "Cloudy", "Sunny"
    recommendation: str                          # e.g. "Bring an umbrella"


reporter_agent = Agent(                          # an agent that returns structured data, not free text
    name="Weather Reporter",                     # name for tracing
    instructions="Provide weather reports.",     # system prompt
    output_type=WeatherReport,                   # forces output to match the WeatherReport schema
)                                                # result.final_output will be a WeatherReport instance


async def main():                                # async entry coroutine
    result = await Runner.run(                    # run the loop until output matches the schema
        reporter_agent,                          # the structured-output agent
        "Weather report for London: it's cloudy and 14C.",  # user prompt to turn into a report
    )                                            # result.final_output is now a WeatherReport instance, not a string

    print(result.final_output)                 # grab the typed object the agent produced
    # print(type(report))                          # proves it's a WeatherReport, not a plain str
    # print("City:", report.city)                  # access fields with dot notation, like any object
    # print("Temperature:", report.temperature)    # each attribute is guaranteed to exist by the schema
    # print("Conditions:", report.conditions)      # no JSON parsing or key-guessing needed
    # print("Recommendation:", report.recommendation)  # safe to use directly in downstream code


if __name__ == "__main__":                       # script guard
    asyncio.run(main())                          # drive the async main()

# CONNECTION TO SESSION 1:
#   output_type is the agent-level version of response_format from Session 1.
#   The loop keeps running until the model produces something matching this Pydantic schema.
#   Same concept, now wired into the agent loop.
