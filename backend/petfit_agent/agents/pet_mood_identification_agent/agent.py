from google.adk.agents import LlmAgent
from .tools import identify_expression_meaning
from google.adk.tools import google_search, AgentTool

pet_mood_identification_agent = LlmAgent(
    name="pet_mood_identification_agent",
    model="gemini-2.0-flash",
    description="Pet Mood Identification Agent",
    instruction="""
       You are an agent that identifies the mood of the pet when provided with the pet's expression's image.
       To identify what the mood of pet is in the provided image use the tool identify_expression_meaning.
       Once you get the identification about what the mood of the pet is, summarize it in short to the user.

       When user asks more information try to interact and answer as many questions as possible.

       For making the response more customized use the below pet's information:
       {pet_information}
    """,
    tools=[identify_expression_meaning],
    output_key="summary_expression_identification",
)