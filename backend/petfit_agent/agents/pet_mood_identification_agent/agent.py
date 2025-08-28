from google.adk.agents import Agent
from .tools import identify_expression_meaning
from petfit_agent.setup import search_agent
from google.adk.tools.agent_tool import AgentTool

pet_mood_identification_agent = Agent(
    name="pet_mood_identification_agent",
    model="gemini-2.0-flash",
    description="Pet Mood Identification Agent",
    instruction="""
       You are an agent that identifies the mood of the pet when provided with the pet's expression's image.
       To identify what the mood of pet is in the provided image use the tool identify_expression_meaning.
       Once you get the identification about what the mood of the pet is, summarize it in short to the user.

       When user asks more information try to interact and answer as many questions as possible utilizing the search_agent tool. 

       For making the response more customized use the below pet's information:
       {pet_information}
    """,
    tools=[identify_expression_meaning, AgentTool(search_agent)],
    output_key="summary_expression_identification",
)